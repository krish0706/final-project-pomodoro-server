let timer;
const timer_interval = 1000;
const focus_bg_color = "#FC94A1";
const break_bg_color = "#78C1A3";
const focus_mode = "focus";
const body = document.body;

function init_timer() {
    timer_interval_callback();
    timer = setInterval(timer_interval_callback, timer_interval);
}

function timer_interval_callback() {
    const timer_element = document.getElementById('timer');
    const mode_element = document.getElementById('mode');

    fetch('/state')
    .then(res => res.json())
    .then(data => {
        let seconds_remaining = data.time_remaining;
        let mins = Math.floor(seconds_remaining / 60);
        let secs = Math.floor(seconds_remaining % 60);
        timer_element.textContent = mins.toString().padStart(2, '0') + ":" + secs.toString().padStart(2, '0');
        mode_element.textContent = data.mode;
        body.style.backgroundColor = (data.mode == focus_mode) ? focus_bg_color : break_bg_color;
    });

}

function play_timer() {
    fetch('/start', {method:'POST'});
}

function pause_timer() {
    fetch('/pause', {method:'POST'});
}

function reset_timer() {
    fetch('/reset', {method:'POST'});
}

document.addEventListener("DOMContentLoaded", function() {
    init_timer();
});