window.addEventListener("beforeunload", function () {
    const roomCodeEl = document.querySelector('input[name="room_code"]');
    const usernameEl = document.querySelector('meta[name="username"]'); // budeme potřebovat

    if (!roomCodeEl || !usernameEl) return;

    const roomCode = roomCodeEl.value;
    const username = usernameEl.content;

    navigator.sendBeacon(
        `/leave_room?room_code=${encodeURIComponent(roomCode)}&username=${encodeURIComponent(username)}`
    );
});
