// volunteer-search.js: Implements live search for events in both tabs

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("event-search");
    if (!searchInput) return;

    function filterEvents(tabId, eventListSelector) {
        const query = searchInput.value.trim().toLowerCase();
        const events = document.querySelectorAll(`#${tabId} ${eventListSelector} .event-card`);
        let anyVisible = false;
        events.forEach(card => {
            // Get text from title, description, industry, and all skill badges
            const title = card.querySelector('.event-title')?.textContent.toLowerCase() || '';
            const description = card.querySelector('.event-description')?.textContent.toLowerCase() || '';
            const industry = card.querySelector('.industry-badge')?.textContent.toLowerCase() || '';
            let skills = '';
            card.querySelectorAll('.skill-badge').forEach(badge => {
                skills += ' ' + badge.textContent.toLowerCase();
            });
            const searchText = `${title} ${description} ${industry} ${skills}`;
            if (searchText.includes(query)) {
                card.style.display = "";
                anyVisible = true;
            } else {
                card.style.display = "none";
            }
        });
        // Show/hide empty state
        const emptyState = document.querySelector(`#${tabId} .empty-state`);
        if (emptyState) {
            emptyState.style.display = anyVisible ? "none" : "";
        }
    }

    searchInput.addEventListener("input", () => {
        // Filter both tabs
        filterEvents("tab-content-1", ".events-grid");
        filterEvents("tab-content-2", ".events-grid");
    });

    // Optionally: filter on tab switch for a consistent experience
    const tabButtons = document.querySelectorAll(".tab-button");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            filterEvents("tab-content-1", ".events-grid");
            filterEvents("tab-content-2", ".events-grid");
        });
    });
});
