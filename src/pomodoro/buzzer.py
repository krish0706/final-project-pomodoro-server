import RPi.GPIO as GPIO
import time

class Buzzer:
    BUZZER_PIN = 4

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        self.pwm = None

    def _start_pwm(self, freq):
        if self.pwm is None:
            self.pwm = GPIO.PWM(self.BUZZER_PIN, freq)
            self.pwm.start(50)
        else:
            self.pwm.ChangeFrequency(freq)
            self.pwm.start(50)

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
