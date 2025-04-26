#!/usr/bin/python3

from rpi_lcd import LCD
import time

class Display:
    def __init__(self):
        self.lcd = LCD()

    def home(self):
        self.lcd.clear()
        self.lcd.text("Pomodoro Timer", 1)

    def show_message(self, line1="", line2=""):
        self.lcd.clear()
        if line1:
            self.lcd.text(line1, 1)
        if line2:
            self.lcd.text(line2, 2)

    def clear(self):
        self.lcd.clear()

    def cleanup(self):
        self.lcd.clear()






















