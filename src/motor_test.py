from machine import Pin
import time, utime

print("Starting")

# Next thing - get the motor driver working to step the hands
motor_en = Pin(27, Pin.OUT)
motor_A  = Pin(26, Pin.OUT)
motor_B  = Pin(25, Pin.OUT)

motor_en.value(0)
motor_A.value(0)
motor_B.value(0)

import utime

# Let's start off with 200ms pulses once per second
pulse_duration = 300  # Motor turning
pause_duration = 0    # Motor off
stop_duration  = 100  # Motor actively stopped

print("Using pins", motor_A, motor_B, motor_en)

while True:
    # Pulse polarity positive
    print("Positive pulse")
    motor_A.value(1)
    motor_en.value(1)
    utime.sleep_ms(pulse_duration)
    motor_B.value(1)
    utime.sleep_ms(stop_duration)
    motor_en.value(0) # Keep the driver disabled as much as possible to save power/heat

    # Wait
    print("Pause")
    utime.sleep_ms(pause_duration)

    # Pulse polarity negative
    print("Negative pulse")
    motor_A.value(0)
    motor_en.value(1)
    utime.sleep_ms(pulse_duration)
    motor_B.value(0)
    utime.sleep_ms(stop_duration)
    motor_en.value(0) # Keep the driver disabled as much as possible to save power/heat

    # Wait
    print("Pause again")
    utime.sleep_ms(pause_duration)