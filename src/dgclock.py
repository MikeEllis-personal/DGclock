from utime import sleep_ms
from machine import Pin

import pulseclock
import settings

class DGClock:
    def __init__(self, config_filename, hands):
        """ Constructor

        Args:
            config_filename (string): Name of the file to read
            hands           (int)   : The current hand position as seconds from 12:00:00
        """        
        # Read the config file describing the pulse clock setup
        clock_settings = settings.load_settings(config_filename)

        # Initialise the actual pulse clock
        self.pc = pulseclock.PulseClock(clock_settings, hands % 60)

        # Keep a copy of where the hands are pointing
        #print("Initialising hands to {}".format(hands))
        self.hands = hands
        self.mode  = "Wait"


    def __repr__(self):
        pass

    def adjust(self, new_hands):
        self.hands = new_hands

    @property
    def hands(self):
        return self._hands

    @property
    def hands_tm(self):
        value = (0,0,0, (self._hands // 3600) % 24, (self._hands // 60) % 60, self._hands % 60, 0, 0) # TM structure YMDHMS00
        return value

    @hands.setter
    def hands(self, value):
        self._hands       = int(value % 43200)    # Must be an integer in the range 00:00:00 to 11:59:59
        
    @hands_tm.setter
    def hands_tm(self, value):
        self.hands = value[3] * 3600 + value[4] * 60 + value[5]

    def hands_reset(self, value):
        # Just like setting the hands, but also tell the pulseclock that we've moved them
        self.hands         = value
        self.pc.sec_pos    = self.hands % 60
        self.pc.edgecount  = 0

    def move(self, wanted_time):
        wanted_time %= 43200 # Only care about the 12-hour portion of the time

        diff = (wanted_time - self._hands) % 43200

        #print("Want:{} Show:{} Diff:{}".format(wanted_time, self._hands, diff))

        if diff == 0:                                 # Hands are correct
            self.mode = "Run"
        elif diff == 1:                               # Just need a single step
            self.mode   = "Run"
            self.pc.step()
            self.hands += 1
        elif diff > 43140:                            # Small backward error - don't set hand to 12
            self.mode = "Wait"
        elif diff > 36000 and self._hands % 60 == 0:  # >10hr difference and second hand on 12 - just wait!
            self.mode = "Wait"
        else:                                         # Need to move fast to catch up
            self.mode   = "Fast"
            self.pc.faststep()
            self.hands += 1

        # Check the second hand position at the bottom of the minute to avoid fence-post errors
        if (self.hands % 60) == 30 and self.pc.read_secondhand() != 30:
            print("Second hand adjusted from {} to {}".format(self.hands % 60, self.pc.read_secondhand()))
            self.hands = (self.hands // 60) * 60 + self.pc.read_secondhand()