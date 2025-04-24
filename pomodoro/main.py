from flask import Blueprint, render_template, jsonify
from .pomodoro_timer import PomodoroTimer


bp = Blueprint("main", __name__, url_prefix="/")
timer = PomodoroTimer()


@bp.route("/")
@bp.route("/home")
def home():
    return render_template("home.html")


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/start", methods=["POST"])
def start_timer():
    timer.handle_event("start")
    return jsonify({"message": "timer started"})


@bp.route("/pause", methods=["POST"])
def pause_timer():
    timer.handle_event("pause")
    return jsonify({"message": "timer paused"})


@bp.route("/reset", methods=["POST"])
def reset_timer():
    global timer
    timer = PomodoroTimer()
    timer.handle_event("reset")
    return jsonify({"message": "timer reset"})


@bp.route("/state")
def get_timer_state():
    time_remaining = timer.get_remaining_time()
    mode = timer.update_mode(time_remaining)
    return jsonify(
        {
            "state": timer.current_state,
            "time_remaining": time_remaining,
            "mode": mode,
        }
    )
