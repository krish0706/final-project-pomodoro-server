"""
******************************************************************************
* Name        : Bhakti Ramani
* Subject     : ECEN 5713 - Advanced Embedded Systems Development (AESD)
* Institution : University of Colorado Boulder
* File        : buzzer_driver.py
* Description : 
*   This file implements the Buzzer driver for the Pomodoro hardware project
*   using the RPi.GPIO library. It provides different tunes for system 
*   states such as start, end, reset, and pause.
*
*   Features:
*     - Play simple tones at different frequencies
*     - Predefined sequences for various system events
*     - PWM-based control for buzzer sound generation
* Notes : This code works with Buildroot and Raspberry Pi 4B for passive buzzer.
* 	  Simply connect + to GPIO pin defined as BUZZER_PIN and - to GND.
*
******************************************************************************
"""

import RPi.GPIO as GPIO
import time

class Buzzer:
    BUZZER_PIN = 4

    def __init__(self):
        """
        Initialize the Buzzer class by setting up the GPIO pin.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        self.pwm = None
        
    def _start_pwm(self, freq):
        """
        Start PWM on the buzzer pin at a given frequency.
        """
        self.pwm = GPIO.PWM(self.BUZZER_PIN, freq)
        self.pwm.start(50)

    def play_tone(self, freq, duration):
        """
        Play a single tone at the specified frequency and duration.

        Args:
            freq (float): Frequency in Hz.
            duration (float): Duration in seconds.
        """
        if self.pwm is None:
            self._start_pwm(freq)
        self.pwm.ChangeFrequency(freq)
        self.pwm.start(50)
        time.sleep(duration)
        self.pwm.stop()
        time.sleep(0.05)

    def system_start(self):
        """
        Play the tune that indicates system start.
        """
        notes = [392, 523.25, 587.33, 659.25, 523.25]
        duration = [0.15, 0.15, 0.15, 0.2, 0.3]
        self._play_sequence(notes, duration)

    def system_end(self):
        """
        Play the tune that indicates system shutdown.
        """
        notes = [783.99, 659.25, 587.33, 523.25, 493.88, 392.00]
        duration = [0.15, 0.15, 0.15, 0.2, 0.3, 0.3]
        self._play_sequence(notes, duration)

    def pomodaro_start(self):
        """
        Play the tune that signals the start of a Pomodoro session.
        """
        notes = [523.25, 587.33, 659.25, 698.46, 783.99, 880.00]
        duration = [0.1, 0.1, 0.1, 0.1, 0.15, 0.2]
        self._play_sequence(notes, duration)

    def pomodaro_end(self):
        """
        Play the tune that signals the end of a Pomodoro session.
        """
        notes = [880.00, 783.99, 659.25, 587.33, 659.25, 523.25]
        duration = [0.1, 0.1, 0.1, 0.1, 0.15, 0.2]
        self._play_sequence(notes, duration)
    
    def play_reset(self):
        """
        Play the reset tune to indicate a system reset.
        """
        notes = [392.00, 349.23, 329.63, 349.23, 392.00, 523.25]
        duration = [0.15, 0.15, 0.15, 0.15, 0.15, 0.3]
        self._play_sequence(notes, duration)

    def play_pause(self):
        """
        Play the pause tune to indicate that the system is on hold.
        """
        notes = [329.63, 392.00, 329.63, 392.00, 349.23, 329.63]
        duration = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3]
        self._play_sequence(notes, duration)

    def _play_sequence(self, notes, durations):
        """
        Play a sequence of notes with corresponding durations.

        Args:
            notes (list): List of frequencies (float).
            durations (list): List of durations (float).
        """
        for note, dur in zip(notes, durations):
            self.play_tone(note, dur)

    def cleanup(self):
        """
        Cleanup the GPIO settings and stop PWM.
        """
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup()

