#!/usr/bin/python3

import os
import time
import threading

import RPi.GPIO as GPIO

lock = threading.Lock()
run = True

def toggle():
    frequency = 25
    toggle_pin = 14
    GPIO.setup(toggle_pin, GPIO.OUT)
    state = True
    my_run = True
    while my_run:
        GPIO.output(toggle_pin, state)
        state = not state
        time.sleep(1/frequency/2)
        with lock:
            my_run = run
    GPIO.cleanup(toggle_pin)

if __name__ == '__main__':
    shutdown_pin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    t = threading.Thread(name='toggle', target=toggle)
    t.start()

    while True:
        try:
            if not GPIO.input(shutdown_pin):
                time.sleep(0.1)
                if not GPIO.input(shutdown_pin):
                    break
            time.sleep(0.5)
        except Exception as e:
            pass
    with lock:
        run = False
    time.sleep(1)
        
    GPIO.cleanup(shutdown_pin)
    os.system(f'sudo shutdown now')

