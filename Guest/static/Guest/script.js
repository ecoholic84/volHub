// Ensure strict mode for better error catching
'use strict';

// Wrap all code in an IIFE for better scoping
(function() {
    // Utility Functions
    function showMessage(message, type) {
        const messageDiv = document.getElementById('message');
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.className = 'message ' + (type === 'error' ? 'error-message' : 'success-message');
            messageDiv.style.display = 'block';
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        } else {
            console.error('Message div not found');
        }
    }

    function initializeApp() {
        console.log('Initializing app...');
        try {
            initializeTheme();
            initializeMobileMenu();
            initializeSmoothScroll();
            initializeTestimonialSlider();
        } catch (error) {
            console.error('Initialization error:', error);
        }
    }

    function initializeTheme() {
        console.log('Initializing theme...');
        const themeSwitch = document.getElementById('theme-switch');
        const body = document.body;

        if (!themeSwitch || !body) {
            console.error('Theme switch or body not found');
            return;
        }

        const savedTheme = localStorage.getItem('theme') || 'light-theme';
        body.classList.add(savedTheme);
        themeSwitch.checked = savedTheme === 'dark-theme';

        themeSwitch.addEventListener('click', function() {
            if (this.checked) {
                body.classList.remove('light-theme');
                body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark-theme');
            } else {
                body.classList.remove('dark-theme');
                body.classList.add('light-theme');
                localStorage.setItem('theme', 'light-theme');
            }
        });
    }

    function initializeMobileMenu() {
        console.log('Initializing mobile menu...');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const nav = document.querySelector('nav');

        if (!mobileMenuBtn || !nav) {
            console.error('Mobile menu button or nav not found');
            return;
        }

        mobileMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            nav.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    function initializeSmoothScroll() {
        console.log('Initializing smooth scroll...');
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    function initializeTestimonialSlider() {
        console.log('Initializing testimonial slider...');
        const testimonialGroups = document.querySelectorAll('.testimonial-group');
        const dots = document.querySelectorAll('.dot');
        const prevBtn = document.querySelector('.prev-btn');
        const nextBtn = document.querySelector('.next-btn');
        let currentGroup = 0;
        let slideInterval;

        function showGroup(index) {
            testimonialGroups.forEach(group => group.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            currentGroup = (index + testimonialGroups.length) % testimonialGroups.length;
            testimonialGroups[currentGroup].classList.add('active');
            dots[currentGroup].classList.add('active');
        }

        function nextGroup() {
            showGroup(currentGroup + 1);
        }

        function prevGroup() {
            showGroup(currentGroup - 1);
        }

        function startSlideshow() {
            if (slideInterval) {
                clearInterval(slideInterval);
            }
            slideInterval = setInterval(nextGroup, 6000);
        }

        function pauseSlideshow() {
            clearInterval(slideInterval);
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                prevGroup();
                pauseSlideshow();
                startSlideshow();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                nextGroup();
                pauseSlideshow();
                startSlideshow();
            });
        }

        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showGroup(index);
                pauseSlideshow();
                startSlideshow();
            });
        });

        const testimonialSlider = document.querySelector('.testimonial-slider');
        if (testimonialSlider) {
            testimonialSlider.addEventListener('mouseenter', pauseSlideshow);
            testimonialSlider.addEventListener('mouseleave', startSlideshow);
        }

        startSlideshow();
    }

    // Add DOMContentLoaded event listener to initialize the app
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM fully loaded and parsed');
        initializeApp();
    });
})();