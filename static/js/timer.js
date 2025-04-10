window.addEventListener("DOMContentLoaded", function () {
    const countdownEl = document.getElementById("countdown");
    let seconds = parseInt(countdownEl.dataset.timer);
    const isPaused = countdownEl.dataset.paused === "true";

    function updateCountdown() {
        let min = Math.floor(seconds / 60);
        let sec = seconds % 60;
        countdownEl.textContent = `${min}:${sec.toString().padStart(2, '0')}`;

        if (seconds > 0 && !isPaused) {
            seconds--;
            setTimeout(updateCountdown, 1000);
        }
    }

    updateCountdown();
});
