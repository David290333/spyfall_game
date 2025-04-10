document.addEventListener("DOMContentLoaded", function () {
    const locationItems = document.querySelectorAll(".location-item");
    locationItems.forEach(item => {
        item.addEventListener("click", () => {
            item.classList.toggle("crossed");
        });
    });
});
