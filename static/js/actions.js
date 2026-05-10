document.addEventListener("DOMContentLoaded", function() {
    // Sidebar toggle functionality using Vanilla JavaScript
    var minimizeBtn = document.querySelector(".x-navigation-minimize");
    var pageContainer = document.querySelector(".page-container");

    // Add mobile overlay dynamically
    var overlay = document.createElement("div");
    overlay.className = "mobile-overlay";
    if (pageContainer) {
        pageContainer.appendChild(overlay);
    }

    if (minimizeBtn && pageContainer) {
        minimizeBtn.addEventListener("click", function(e) {
            e.preventDefault();
            // Check if on mobile viewport
            if (window.innerWidth <= 768) {
                pageContainer.classList.toggle("sidebar-mobile-open");
                // Reset minimized state if it was there
                pageContainer.classList.remove("sidebar-minimized");
            } else {
                pageContainer.classList.toggle("sidebar-minimized");
            }
        });
    }

    // Close mobile sidebar when overlay is clicked
    overlay.addEventListener("click", function() {
        pageContainer.classList.remove("sidebar-mobile-open");
    });
});