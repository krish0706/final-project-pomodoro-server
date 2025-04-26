import RPi.GPIO as GPIO
import time

class Buzzer:
    BUZZER_PIN = 4

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        self.pwm = None
        
    def _start_pwm(self, freq):
        self.pwm = GPIO.PWM(self.BUZZER_PIN, freq)
        self.pwm.start(50)

    def play_tone(self, freq, duration):
        if self.pwm is None:  
            self._start_pwm(freq)
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
    

    def play_reset(self):
    # Reset tune - "Starting over" feeling (distinctive pattern)
        notes = [392.00, 349.23, 329.63, 349.23, 392.00, 523.25]  # G4, F4, E4, F4, G4, C5
        duration = [0.15, 0.15, 0.15, 0.15, 0.15, 0.3]
        self._play_sequence(notes, duration)

    def play_pause(self):
        # Pause tune - "On hold" feeling (gentle alternating pattern)
        notes = [329.63, 392.00, 329.63, 392.00, 349.23, 329.63]  # E4, G4, E4, G4, F4, E4
        duration = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3]
        self._play_sequence(notes, duration)

    def _play_sequence(self, notes, durations):
        for note, dur in zip(notes, durations):
            self.play_tone(note, dur)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
