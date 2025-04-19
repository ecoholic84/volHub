// static/js/dashboard-tabs.js
document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");
    const slider = document.querySelector(".tab-slider");
    // Initialize slider position on load
    if (slider && tabButtons.length) {
        const activeBtn = document.querySelector(".tab-button.active") || tabButtons[0];
        slider.style.left = (activeBtn.offsetLeft) + "px";
        slider.style.width = activeBtn.offsetWidth + "px";
    }

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
            const slider = document.querySelector(".tab-slider");
            if (slider) {
                const activeBtn = button;
                const btnRect = activeBtn.getBoundingClientRect();
                const parentRect = activeBtn.parentElement.getBoundingClientRect();
                slider.style.left = (activeBtn.offsetLeft) + "px";
                slider.style.width = activeBtn.offsetWidth + "px";
            }
        });
    });
});
