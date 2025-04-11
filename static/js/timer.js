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
            console.error("Chyba při ukládání času:", err);
        }
    }

    function updateCountdown() {
        let min = Math.floor(seconds / 60);
        let sec = seconds % 60;
        countdownEl.textContent = `${min}:${sec.toString().padStart(2, '0')}`;

        // Dynamicky zkontroluj, jestli je pauza AKTUÁLNÍ
        const isPaused = countdownEl.dataset.paused === "true";

        if (seconds > 0 && !isPaused) {
            seconds--;
            updateTimerOnServer(seconds);
            setTimeout(updateCountdown, 1000);
        } else {
            setTimeout(updateCountdown, 1000); // pokračuj v kontrole pauzy
        }
    }

    updateCountdown();
});