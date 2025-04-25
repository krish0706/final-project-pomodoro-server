import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=4, frequency=1000):
        self.pin = pin
        self.frequency = frequency
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)

    def play_tone(self, freq, duration):
        self.pwm.ChangeFrequency(freq)
        self.pwm.start(50)
        time.sleep(duration)
        self.pwm.stop()
        time.sleep(0.05)

    def system_start(self):
        notes = [392, 523.25, 587.33, 659.25, 523.25]
        duration = [0.15, 0.15, 0.15, 0.2, 0.3]
        self._play_sequence(notes, duration)

    def system_end(self):
        notes = [783.99, 659.25, 587.33, 523.25, 493.88, 392.00]
        duration = [0.15, 0.15, 0.15, 0.2, 0.3, 0.3]
        self._play_sequence(notes, duration)

    def pomodaro_start(self):
        notes = [523.25, 587.33, 659.25, 698.46, 783.99, 880.00]
        duration = [0.1, 0.1, 0.1, 0.1, 0.15, 0.2]
        self._play_sequence(notes, duration)

    def pomodaro_end(self):
        notes = [880.00, 783.99, 659.25, 587.33, 659.25, 523.25]
        duration = [0.1, 0.1, 0.1, 0.1, 0.15, 0.2]
        self._play_sequence(notes, duration)

    def pomodaro_ambient(self):
        notes = [98.00, 123.47, 146.83, 130.81]
        duration = [0.7, 0.7, 0.8, 1.0]
        for note, dur in zip(notes, duration):
            self.play_tone(note, dur)
            time.sleep(0.3)

    def _play_sequence(self, notes, durations):
        for note, dur in zip(notes, durations):
            self.play_tone(note, dur)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
