document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const tabSlider = document.querySelector('.tab-slider');
    
    function setActiveTab(tabId) {
        // Update tab buttons
        tabButtons.forEach(button => {
            if (button.id === tabId) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
        
        // Update tab contents
        tabContents.forEach(content => {
            if (content.id === `tab-content-${tabId.split('-')[1]}`) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });
        
        // Move the slider
        const activeButton = document.getElementById(tabId);
        const buttonRect = activeButton.getBoundingClientRect();
        const buttonsContainer = document.querySelector('.tab-buttons');
        const containerRect = buttonsContainer.getBoundingClientRect();
        
        tabSlider.style.width = `${buttonRect.width}px`;
        tabSlider.style.left = `${buttonRect.left - containerRect.left}px`;
    }
    
    // Initialize tabs
    setActiveTab('tab-1');
    
    // Add click event listeners to tab buttons
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            setActiveTab(this.id);
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('event-search');
    const eventCards = document.querySelectorAll('.event-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            // Only search/filter cards in the currently active tab
            const activeTabContent = document.querySelector('.tab-content.active');
            const activeCards = activeTabContent.querySelectorAll('.event-card');
            let anyVisible = false;
            activeCards.forEach(card => {
                const eventTitle = (card.querySelector('.event-title')?.textContent || '').toLowerCase();
                const eventDescription = (card.querySelector('.event-description')?.textContent || '').toLowerCase();
                const eventLocation = (card.querySelector('.event-location span')?.textContent || '').toLowerCase();
                if (
                    eventTitle.includes(searchTerm) ||
                    eventDescription.includes(searchTerm) ||
                    eventLocation.includes(searchTerm)
                ) {
                    card.style.display = '';
                    anyVisible = true;
                } else {
                    card.style.display = 'none';
                }
            });
            // Empty state for no visible cards
            const existingEmptyState = activeTabContent.querySelector('.search-empty-state');
            if (!anyVisible && !existingEmptyState) {
                const eventsGrid = activeTabContent.querySelector('.events-grid');
                const noResultsEl = document.createElement('div');
                noResultsEl.className = 'empty-state search-empty-state';
                noResultsEl.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <h3 class="empty-title">No matching events found</h3>
                    <p class="empty-message">Try adjusting your search terms</p>
                `;
                eventsGrid.appendChild(noResultsEl);
            } else if (anyVisible && existingEmptyState) {
                existingEmptyState.remove();
            }
        });
    }
    
    // Sort functionality
    const sortSelect = document.getElementById('sort-select');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortValue = this.value;
            const activeTabContent = document.querySelector('.tab-content.active');
            const eventsGrid = activeTabContent.querySelector('.events-grid');
            const cards = Array.from(eventsGrid.querySelectorAll('.event-card'));
            
            // Sort cards based on selected option
            cards.sort((a, b) => {
                if (sortValue === 'date') {
                    const dateA = new Date(a.querySelector('.event-date span').textContent);
                    const dateB = new Date(b.querySelector('.event-date span').textContent);
                    return dateA - dateB;
                } else if (sortValue === 'name') {
                    const titleA = a.querySelector('.event-title').textContent.toLowerCase();
                    const titleB = b.querySelector('.event-title').textContent.toLowerCase();
                    return titleA.localeCompare(titleB);
                } else if (sortValue === 'location') {
                    const locationA = a.querySelector('.event-location span')?.textContent.toLowerCase() || '';
                    const locationB = b.querySelector('.event-location span')?.textContent.toLowerCase() || '';
                    return locationA.localeCompare(locationB);
                }
                return 0;
            });
            
            // Remove all cards and re-append in sorted order
            cards.forEach(card => card.remove());
            cards.forEach(card => eventsGrid.appendChild(card));
        });
    }
    
    // Handle window resize for tab slider
    window.addEventListener('resize', function() {
        const activeTab = document.querySelector('.tab-button.active');
        if (activeTab) {
            setActiveTab(activeTab.id);
        }
    });
});