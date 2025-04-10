async function showGameOverPopup() {
    const roomCode = document.querySelector("input[name='room_code']").value;
    const response = await fetch(`/game_over_json?room_code=${roomCode}`);
    const data = await response.json();

    document.getElementById("popupSpy").textContent = data.spy;
    document.getElementById("popupLocation").textContent = data.location;
    document.getElementById("popup").style.display = "block";
}
