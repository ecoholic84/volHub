// JS for Organizer Event Detail Tabs

document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.org-tab-button');
    const tabContents = document.querySelectorAll('.org-tab-content');

    tabButtons.forEach((btn, idx) => {
        btn.addEventListener('click', function() {
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            tabContents[idx].classList.add('active');
        });
    });

    // Activate the first tab by default
    if (tabButtons.length > 0) {
        tabButtons[0].classList.add('active');
        tabContents[0].classList.add('active');
    }
});
