window.addEventListener("DOMContentLoaded", function () {
    let seconds = parseInt(document.getElementById("countdown").dataset.timer);
    const countdownEl = document.getElementById("countdown");

    function updateCountdown() {
        let min = Math.floor(seconds / 60);
        let sec = seconds % 60;
        countdownEl.textContent = `${min}:${sec.toString().padStart(2, '0')}`;
        if (seconds > 0) {
            seconds--;
            setTimeout(updateCountdown, 1000);
        }
    }

    updateCountdown();
});

function showGameOverPopup() {
    const popup = document.getElementById("popup");
    const roomCode = document.querySelector('input[name="room_code"]').value;

    fetch(`/game_over_json?room_code=${encodeURIComponent(roomCode)}`)
        .then((res) => res.json())
        .then((data) => {
            document.getElementById("popupSpy").textContent = data.spy;
            document.getElementById("popupLocation").textContent = data.location;
            popup.style.display = "block";
        });
}