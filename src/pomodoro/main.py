from flask import Blueprint, render_template, jsonify, request, url_for, redirect
from .pomodoro_timer import PomodoroTimer
from .buzzer_tunes import Buzzer
from .lcd import Display
from .get_ip import IPAddressFetcher

bp = Blueprint("main", __name__, url_prefix="/")
timer = PomodoroTimer()
buz = Buzzer()
lcd = Display()
ip = IPAddressFetcher()


@bp.route("/")
@bp.route("/home")
def home():
    return render_template("home.html")


@bp.route("/about")
def about():
    ip_address = ip.fetch_ip()
    if ip.is_connected():
        lcd.show_message(ip_address, 0,0)
    return render_template("about.html")


@bp.route("/start", methods=["POST"])
def start_timer():
    buz.pomodaro_start()
    lcd.title()
    timer.handle_event("start")
    ip_address = ip.fetch_ip()
    if ip.is_connected():
        lcd.show_message(ip_address, 0,0)
    return jsonify({"message": "timer started"})


@bp.route("/pause", methods=["POST"])
def pause_timer():
    buz.play_pause()
    lcd.title()
    timer.handle_event("pause")
    ip_address = ip.fetch_ip()
    if ip.is_connected():
        lcd.show_message(ip_address, 0,0)
    return jsonify({"message": "timer paused"})


@bp.route("/reset", methods=["POST"])
def reset_timer():
    global timer
    buz.play_reset()
    lcd.title()
    timer = PomodoroTimer()
    timer.handle_event("reset")
    ip_address = ip.fetch_ip()
    if ip.is_connected():
        lcd.show_message(ip_address, 0,0)
    return jsonify({"message": "timer reset"})


@bp.route("/state")
def get_timer_state():
    ip_address = ip.fetch_ip()
    if ip.is_connected():
        lcd.show_message(ip_address, 0,0)
    else:
        lcd.title()    
    time_remaining = timer.get_remaining_time()
    mode = timer.update_mode(time_remaining)
    return jsonify(
        {
            "state": timer.current_state,
            "time_remaining": time_remaining,
            "mode": mode,
        }
    )
  
  
@bp.route("/submit", methods=["POST"])
def submit_break():
    try:
        break_duration = int(request.form['break-input']) * 60
    except ValueError:
        return "Please enter a valid integer for break duration.", 400

    try:
        focus_duration = int(request.form['focus-input']) * 60 
    except ValueError:
        return "Please enter a valid integer for focus duration.", 400

    timer.set_focus_and_break(focus_duration, break_duration)

    return redirect(url_for("main.home"))

buz.system_start()
ip_address = ip.fetch_ip()
if ip.is_connected():
    lcd.show_message(ip_address, 0,0)


