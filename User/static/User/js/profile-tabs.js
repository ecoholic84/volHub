// profile-tabs.js: Modern tab slider for public profile
// (Based on static-tabs.js)
document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            tabButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");
            tabContents.forEach(content => content.classList.remove("active"));
            const selectedContent = document.querySelector(`#tab-content-${index + 1}`);
            selectedContent.classList.add("active");
            const slider = document.querySelector(".tab-slider-inner");
            if (slider) {
                slider.style.transform = `translateX(${index * 100}%)`;
            }
        });
    });
});
