window.addEventListener("DOMContentLoaded", function () {
    const countdownEl = document.getElementById("countdown");
    let seconds = parseInt(countdownEl.dataset.timer);
    const roomCode = document.querySelector('input[name="room_code"]').value;

    async function updateTimerOnServer(remaining) {
        try {
            await fetch("/update_timer", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ room_code: roomCode, seconds: remaining })
            });
        } catch (err) {
            console.error("An error occurred while saving the time:", err);
        }
    }

    async function pollPausedStatus() {
        try {
            const res = await fetch(`/room_status?room_code=${roomCode}`);
            const data = await res.json();

            if (data.paused !== undefined) {
                countdownEl.dataset.paused = data.paused.toString();
            }
        } catch (err) {
            console.error("An error occurred while checking the pause status:", err);
        } finally {
            setTimeout(pollPausedStatus, 3000);
        }
    }

    function updateCountdown() {
        let min = Math.floor(seconds / 60);
        let sec = seconds % 60;
        countdownEl.textContent = `${min}:${sec.toString().padStart(2, '0')}`;

        const isPaused = countdownEl.dataset.paused === "true";

        if (seconds > 0 && !isPaused) {
            seconds--;
            updateTimerOnServer(seconds);
        }

        setTimeout(updateCountdown, 1000); // vždy pokračuj ve smyčce
    }

    pollPausedStatus();   // spuštění kontroly pauzy
    updateCountdown();    // spuštění odpočtu
});
