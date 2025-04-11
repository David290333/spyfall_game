document.addEventListener("DOMContentLoaded", function () {
    const roomCode = document.querySelector('input[name="room_code"]').value;

    async function pollGameStatus() {
        try {
            const res = await fetch(`/game_status?room_code=${roomCode}`);
            const data = await res.json();

            if (data.game_over) {
                const resultBtn = document.getElementById("showResultBtn");
                if (resultBtn) resultBtn.disabled = false;

                // případně přesměrování automaticky:
                // window.location.href = `/game_over?room_code=${roomCode}`;
            } else {
                setTimeout(pollGameStatus, 3000);
            }
        } catch (err) {
            console.error("Chyba při kontrole konce hry:", err);
            setTimeout(pollGameStatus, 5000);
        }
    }

    pollGameStatus();
});
