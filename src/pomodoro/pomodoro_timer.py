import time
from .buzzer_tunes import Buzzer
from .lcd import Display

buz = Buzzer()
lcd = Display()


class PomodoroTimer:

    FOCUS_DURATION = 5 * 60
    BREAK_DURATION = 1 * 60

    def __init__(self):
        self.events = None
        self.state_table = None
        self.start_time = None
        self.pause_time = None
        self.was_paused = None
        self.focus_break_toggle = None
        self.mode = None
        self.duration = None
        self.current_state = None
        self._reset()
        

    def _reset(self):
        self.events = {"start", "pause", "reset"}
        self.state_table = {
            "paused": self._paused,
            "running": self._running,
        }
        self.current_state = "paused"
        self.start_time = None
        self.pause_time = None
        self.was_paused = False
        self.focus_break_toggle = True
        self.mode = "focus"
        self.duration = self.FOCUS_DURATION

        lcd.clear()
        #lcd.show_message(f"Mode: {self.mode}", 1, 3)

        #lcd.show_message("Mode: Focus", "Press Start")
        if self.mode == "focus":
            lcd.show_message("Focus Time!", 1, 3)
        else:
            lcd.show_message("Break Time!", 1, 3)


    def _paused(self, event):
        if event == "start":
            self.current_state = "running"
            if not self.was_paused:
                self.start_time = int(time.monotonic())
            else:
                duration_paused = int(time.monotonic()) - self.pause_time
                self.start_time += duration_paused

            #lcd.clear()
            #lcd.show_message(f"Mode: {self.mode}", 1, 3)  # LCD shows running

            #lcd.show_message(f"Mode: {self.mode}", "Running...")  # LCD shows running
            if self.mode == "focus":
                lcd.show_message("Focus Time!", 1, 3)
            else:
                lcd.show_message("Break Time!", 1, 3)

        elif event == "reset":
            self._reset()

    def _running(self, event):
        if event == "pause":
            self.pause_time = int(time.monotonic())
            self.current_state = "paused"
            self.was_paused = True

            #lcd.clear()
            #lcd.show_message(f"Mode: {self.mode}", 1, 3)  # LCD shows paused

            #lcd.show_message(f"Mode: {self.mode}", "Paused")  # LCD shows paused
            if self.mode == "focus":
                lcd.show_message("Focus Time!", 1, 3)
            else:
                lcd.show_message("Break Time!", 1, 3)

        elif event == "reset":
            self._reset()

    def get_remaining_time(self):
        if self.current_state == "running":
            time_elapsed = int(time.monotonic()) - self.start_time
        elif self.current_state == "paused" and self.was_paused:
            time_elapsed = self.pause_time - self.start_time
        else:
            time_elapsed = 0

        remaining = max(self.duration - time_elapsed, 0)

        # remaining time on LCD
        minutes = remaining // 60
        seconds = remaining % 60

        #lcd.clear()
        #lcd.show_message(f"Mode: {self.mode}", 1, 3)
        lcd.show_message(f"{minutes:02}:{seconds:02} Left",2, 3)

        #lcd.show_message(f"{minutes:02}:{seconds:02} Left")
    


        return remaining

    def update_mode(self, time_remaining):
        if time_remaining == 0:
            if self.focus_break_toggle:
                self.duration = self.BREAK_DURATION
                self.mode = "break"
                buz.pomodaro_end()

                lcd.show_message("Break Time!", 1, 3)

                #lcd.show_message("Break Time!", 1)

            else:
                self.duration = self.FOCUS_DURATION
                self.mode = "focus"
                buz.pomodaro_start()

                lcd.show_message("Focus Time!", 1, 3)

                #lcd.show_message("Focus Time!", 1)

            self.start_time = int(time.monotonic())
            self.focus_break_toggle = not self.focus_break_toggle

        return self.mode

    def handle_event(self, event):
        if event in self.events:
            self.state_table[self.current_state](event)
        else:
            print("Unknown event!")

    def set_focus_and_break(self, focus_duration, break_duration):
        self.FOCUS_DURATION = focus_duration
        self.BREAK_DURATION = break_duration
        self._reset()
