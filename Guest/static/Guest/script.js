// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle
    const themeSwitch = document.getElementById('theme-switch');
    const body = document.body;

    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    });

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        themeSwitch.checked = true;
    }

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('nav ul');

    mobileMenuBtn.addEventListener('click', function() {
        this.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Modal Functionality
    const signupBtn = document.querySelector('.signup-btn');
    const getStartedBtn = document.querySelector('.get-started-btn');
    const ctaBtn = document.querySelector('.cta-btn');
    const signupModal = document.getElementById('signup-modal');
    const closeModal = document.querySelector('.close-modal');
    
    // Functions to open and close modal
    function openModal() {
        signupModal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
        
        // Reset modal to first step
        const steps = document.querySelectorAll('.step');
        steps.forEach(step => step.classList.remove('active'));
        document.querySelector('.step[data-step="1"]').classList.add('active');
        
        // Reset form fields
        document.getElementById('email-form').reset();
        if (document.getElementById('signup-details-form')) {
            document.getElementById('signup-details-form').reset();
        }
    }
    
    function closeModalFunc() {
        signupModal.classList.remove('show');
        document.body.style.overflow = ''; // Re-enable scrolling
    }
    
    // Event listeners for opening modal
    signupBtn.addEventListener('click', openModal);
    getStartedBtn.addEventListener('click', openModal);
    ctaBtn.addEventListener('click', openModal);
    
    // Event listener for closing modal
    closeModal.addEventListener('click', closeModalFunc);
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === signupModal) {
            closeModalFunc();
        }
    });

    // Password visibility toggle
    const togglePassword = document.getElementById('togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordField = document.getElementById('password');
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle icon
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Get CSRF token for AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrfToken = getCookie('csrftoken');

    // Email form submission
    const emailForm = document.getElementById('email-form');
    if (emailForm) {
        emailForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            
            // Send AJAX request to check if email exists
            fetch('/Guest/sign-up/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                body: `txt_email=${encodeURIComponent(email)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Move to next step
                    document.querySelector('.step[data-step="1"]').classList.remove('active');
                    document.querySelector('.step[data-step="2"]').classList.add('active');
                    
                    // Pre-fill the email in the next step
                    document.getElementById('signup-email').value = email;
                } else {
                    // Show error message
                    alert(data.message || 'This email already exists. Please use a different email or log in.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }

    // Back button functionality
    const backBtn = document.querySelector('.back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            document.querySelector('.step[data-step="2"]').classList.remove('active');
            document.querySelector('.step[data-step="1"]').classList.add('active');
        });
    }

    // OAuth buttons
    const githubBtn = document.getElementById('github-oauth');
    const googleBtn = document.getElementById('google-oauth');
    
    if (githubBtn) {
        githubBtn.addEventListener('click', function() {
            // Implement GitHub OAuth logic
            console.log('GitHub OAuth clicked');
            alert('GitHub OAuth integration will be implemented soon!');
        });
    }
    
    if (googleBtn) {
        googleBtn.addEventListener('click', function() {
            // Implement Google OAuth logic
            console.log('Google OAuth clicked');
            alert('Google OAuth integration will be implemented soon!');
        });
    }

    // Final signup form submission
    const signupDetailsForm = document.getElementById('signup-details-form');
    if (signupDetailsForm) {
        signupDetailsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = new URLSearchParams();
            for (const pair of formData) {
                data.append(pair[0], pair[1]);
            }
            
            // Send AJAX request to register user
            fetch('/Guest/user-registration/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                body: data
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Move to success step
                    document.querySelector('.step[data-step="2"]').classList.remove('active');
                    document.querySelector('.step[data-step="3"]').classList.add('active');
                } else {
                    alert('Registration failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during registration. Please try again.');
            });
        });
    }

    // Testimonial slider
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    let currentSlide = 0;
    
    function showSlide(n) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        currentSlide = (n + slides.length) % slides.length;
        
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }
    
    if (prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
        nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));
        
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => showSlide(index));
        });
    }
}); 