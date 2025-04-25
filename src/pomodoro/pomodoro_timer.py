import time


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

    def _paused(self, event):
        if event == "start":
            self.current_state = "running"
            if not self.was_paused:
                self.start_time = int(time.monotonic())
            else:
                duration_paused = int(time.monotonic()) - self.pause_time
                self.start_time += duration_paused
        elif event == "reset":
            self._reset()

    def _running(self, event):
        if event == "pause":
            self.pause_time = int(time.monotonic())
            self.current_state = "paused"
            self.was_paused = True
        elif event == "reset":
            self._reset()

    def get_remaining_time(self):
        if self.current_state == "running":
            time_elapsed = int(time.monotonic()) - self.start_time
        elif self.current_state == "paused" and self.was_paused:
            time_elapsed = self.pause_time - self.start_time
        else:
            time_elapsed = 0
        return max(self.duration - time_elapsed, 0)

    def update_mode(self, time_remaining):
        if time_remaining == 0:
            if self.focus_break_toggle:
                self.duration = self.BREAK_DURATION
                self.mode = "break"
            else:
                self.duration = self.FOCUS_DURATION
                self.mode = "focus"
            self.start_time = int(time.monotonic())
            self.focus_break_toggle = not self.focus_break_toggle

        return self.mode

    def handle_event(self, event):
        if event in self.events:
            self.state_table[self.current_state](event)
        else:
            print("Unknown event!")
