document.addEventListener("DOMContentLoaded", function() {
    // Sidebar toggle functionality using Vanilla JavaScript
    var minimizeBtn = document.querySelector(".x-navigation-minimize");
    var pageContainer = document.querySelector(".page-container");

    if (minimizeBtn && pageContainer) {
        minimizeBtn.addEventListener("click", function(e) {
            e.preventDefault();
            pageContainer.classList.toggle("sidebar-minimized");
        });
    }
});