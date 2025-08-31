// Main JavaScript functionality for Plow Ahead Initiative website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initScrollAnimations();
    initSmoothScrolling();
    initNavbarTransparency();
    initFormValidation();
    initParticleEffects();
});

// Scroll animations for fade-in effects
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all sections for fade-in animation
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('fade-in');
        observer.observe(section);
    });
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    const navbarToggler = document.querySelector('.navbar-toggler');
                    navbarToggler.click();
                }
            }
        });
    });
}

// Navbar transparency effect on scroll
function initNavbarTransparency() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(33, 68, 135, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = '#214487';
            navbar.style.backdropFilter = 'none';
        }
    });
}

// Enhanced form validation
function initFormValidation() {
    const form = document.querySelector('.registration-form');
    
    if (form) {
        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            // Real-time validation feedback
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                // Clear error state on input
                this.classList.remove('is-invalid');
                const feedback = this.parentNode.querySelector('.invalid-feedback');
                if (feedback) {
                    feedback.remove();
                }
            });
        });
        
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }
}

// Field validation helper
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Remove existing error feedback
    field.classList.remove('is-invalid');
    const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Required field validation
    if (field.hasAttribute('required') || fieldName === 'name' || fieldName === 'email') {
        if (!value) {
            errorMessage = `${getFieldLabel(field)} is required.`;
            isValid = false;
        }
    }
    
    // Email validation
    if (fieldName === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            errorMessage = 'Please enter a valid email address.';
            isValid = false;
        }
    }
    
    // Phone validation (if provided)
    if (fieldName === 'phone' && value) {
        const phoneRegex = /^[\+]?[\d\s\-\(\)]{10,}$/;
        if (!phoneRegex.test(value)) {
            errorMessage = 'Please enter a valid phone number.';
            isValid = false;
        }
    }
    
    // Length validation
    if (fieldName === 'name' && value && value.length < 2) {
        errorMessage = 'Name must be at least 2 characters long.';
        isValid = false;
    }
    
    if (fieldName === 'message' && value && value.length > 500) {
        errorMessage = 'Message must be less than 500 characters.';
        isValid = false;
    }
    
    // Display error if validation failed
    if (!isValid) {
        field.classList.add('is-invalid');
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = errorMessage;
        field.parentNode.appendChild(feedback);
    }
    
    return isValid;
}

// Get field label helper
function getFieldLabel(field) {
    const label = field.parentNode.querySelector('label');
    return label ? label.textContent.replace('*', '').trim() : field.name;
}

// Particle effects for hero section (optional enhancement)
function initParticleEffects() {
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection && window.innerWidth > 768) {
        createFloatingParticles(heroSection);
    }
}

// Create floating particles
function createFloatingParticles(container) {
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        setTimeout(() => {
            createParticle(container);
        }, i * 200);
    }
}

// Individual particle creation
function createParticle(container) {
    const particle = document.createElement('div');
    particle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        pointer-events: none;
        z-index: 1;
    `;
    
    // Random starting position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    
    container.appendChild(particle);
    
    // Animate particle
    animateParticle(particle);
    
    // Remove after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 8000);
}

// Particle animation
function animateParticle(particle) {
    const duration = 8000 + Math.random() * 4000;
    const startY = parseInt(particle.style.top);
    const endY = startY - 100;
    const startX = parseInt(particle.style.left);
    const endX = startX + (Math.random() - 0.5) * 100;
    
    particle.animate([
        {
            transform: `translate(0, 0)`,
            opacity: 0
        },
        {
            transform: `translate(0, 0)`,
            opacity: 0.8,
            offset: 0.1
        },
        {
            transform: `translate(${endX - startX}px, ${endY - startY}px)`,
            opacity: 0,
            offset: 1
        }
    ], {
        duration: duration,
        easing: 'ease-out'
    });
}

// Utility function for smooth scrolling to specific sections
function scrollToSection(sectionId) {
    const section = document.querySelector(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 80;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// Auto-dismiss alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.querySelector('.btn-close')) {
            alert.querySelector('.btn-close').click();
        }
    });
}, 5000);

// Form character counter for message field
const messageField = document.querySelector('textarea[name="message"]');
if (messageField) {
    const maxLength = 500;
    const counter = document.createElement('small');
    counter.className = 'form-text text-muted';
    counter.textContent = `0/${maxLength} characters`;
    messageField.parentNode.appendChild(counter);
    
    messageField.addEventListener('input', function() {
        const currentLength = this.value.length;
        counter.textContent = `${currentLength}/${maxLength} characters`;
        
        if (currentLength > maxLength * 0.9) {
            counter.className = 'form-text text-warning';
        } else {
            counter.className = 'form-text text-muted';
        }
    });
}
