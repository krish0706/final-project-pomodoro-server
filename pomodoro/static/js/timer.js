let timer;
const timer_interval = 1000;

function init_timer() {
    // TODO: find a way to load default values from server rather than adding information inside html page
    timer_interval_callback();
    timer = setInterval(timer_interval_callback, timer_interval);
}

function timer_interval_callback() {
    const timer_element = document.getElementById('timer');
    const state_element = document.getElementById('state');
    const mode_element = document.getElementById('mode');

    fetch('/state')
    .then(res => res.json())
    .then(data => {
        let seconds_remaining = data.time_remaining;
        let mins = Math.floor(seconds_remaining / 60);
        let secs = Math.floor(seconds_remaining % 60);
        timer_element.textContent = mins.toString().padStart(2, '0') + ":" + secs.toString().padStart(2, '0');
        state_element.textContent = data.state;
        mode_element.textContent = data.mode;
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

init_timer();