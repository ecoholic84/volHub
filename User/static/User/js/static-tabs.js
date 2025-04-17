// static/js/dashboard-tabs.js
document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            // Toggle active tab button
            tabButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            // Toggle tab content
            tabContents.forEach(content => content.classList.remove("active"));
            const selectedContent = document.querySelector(`#tab-content-${index + 1}`);
            selectedContent.classList.add("active");

            // Move slider
            const slider = document.querySelector(".tab-slider-inner");
            if (slider) {
                slider.style.transform = `translateX(${index * 100}%)`;
            }
        });
    });
});
