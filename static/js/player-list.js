document.addEventListener("DOMContentLoaded", function () {
    const roomCode = document.querySelector('input[name="room_code"]').value;
    const playerListEl = document.getElementById("playerList");

    async function updatePlayerList() {
        try {
            const res = await fetch(`/player_list?room_code=${roomCode}`);
            const data = await res.json();

            if (Array.isArray(data.players)) {
                playerListEl.innerHTML = ""; // vyčisti seznam
                data.players.forEach((player) => {
                    const li = document.createElement("li");
                    li.textContent = player;
                    playerListEl.appendChild(li);
                });
            }
        } catch (err) {
            console.error("An error occurred while loading the players:", err);
        } finally {
            setTimeout(updatePlayerList, 3000); // kontroluj každé 3 sekundy
        }
    }

    updatePlayerList();
});
