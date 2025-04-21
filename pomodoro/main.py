import time
from flask import Blueprint, render_template, jsonify

# TODO: move to separate file
# TODO: move event handling to inside class
class PomodoroTimer:

    def __init__(self):
        self.states = {"paused", "running"}
        self.current_state = "paused"
        self.start_time = None
        self.pause_time = None
        self.was_paused = False
        self.FOCUS_DURATION = 2*60
        self.BREAK_DURATION = 1*60
        self.focus_break_toggle = True
        self.mode = "focus"
        self.duration = self.FOCUS_DURATION 


bp = Blueprint('main', __name__, url_prefix='/')
timer = PomodoroTimer()

@bp.route("/")
@bp.route("/home")
def home():
    global timer 
    timer = PomodoroTimer()
    return render_template('home.html')

@bp.route("/about")
def about():
    return render_template('about.html')

@bp.route("/start", methods=['POST'])
def start_timer():
    if timer.current_state == "paused":
        timer.current_state = "running"
        timer.duration = timer.FOCUS_DURATION
        timer.mode = "focus"
        if not timer.was_paused:
            timer.start_time = int(time.monotonic())
        else:
            # starting once again after pause, handle that case
            duration_paused = int(time.monotonic()) - timer.pause_time
            timer.start_time += duration_paused 
    return jsonify({"message":"timer started"})

@bp.route("/pause", methods=['POST'])
def pause_timer():
    if timer.current_state == "running":
        timer.pause_time = int(time.monotonic())
        timer.current_state = "paused"
        timer.was_paused = True
    return jsonify({"message":"timer paused"})

@bp.route("/reset", methods=['POST'])
def reset_timer():
    global timer 
    timer = PomodoroTimer()
    return jsonify({"message":"timer reset"})

@bp.route("/state")
def get_timer_state():
    if timer.current_state == "running":
        time_elapsed = int(time.monotonic()) - timer.start_time
        time_remaining = max(timer.duration - time_elapsed, 0)
    elif timer.current_state == "paused" and timer.was_paused:
        time_elapsed = timer.pause_time - timer.start_time
        time_remaining = max(timer.duration - time_elapsed, 0)
    else:
        time_remaining = timer.duration

    # if 0 time remaining in current state, switch mode
    if time_remaining == 0:
        if timer.focus_break_toggle:
            timer.duration = timer.BREAK_DURATION
            timer.mode = "break"
        else:
            timer.duration = timer.FOCUS_DURATION
            timer.mode = "focus"
        timer.start_time = int(time.monotonic())
        timer.focus_break_toggle = not timer.focus_break_toggle

    return jsonify({"state": timer.current_state, "time_remaining": time_remaining, "mode": timer.mode})

