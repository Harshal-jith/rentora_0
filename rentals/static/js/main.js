// RENTORA Kerala Luxury Real Estate - Liquid Glass UI & FadingVideo / BlurText Motion Engine

document.addEventListener('DOMContentLoaded', () => {
    // 1. Dark / Light Theme Toggle Management
    const themeToggleBtn = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlElement = document.documentElement;
    const bodyElement = document.body;

    const savedTheme = localStorage.getItem('rentora_theme') || 'dark';
    applyTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
            applyTheme(currentTheme);
        });
    }

    function applyTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        if (theme === 'light') {
            bodyElement.classList.remove('dark-theme');
            bodyElement.classList.add('light-theme');
            if (themeIcon) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            }
        } else {
            bodyElement.classList.remove('light-theme');
            bodyElement.classList.add('dark-theme');
            if (themeIcon) {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }
        }
        localStorage.setItem('rentora_theme', theme);
    }

    // 2. Navbar Scroll Glass Effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 3. FadingVideo Engine (Atmospheric Loop with 500ms fade-in and 550ms fade-out)
    const fadingVideos = document.querySelectorAll('.fading-video');
    fadingVideos.forEach(video => {
        video.addEventListener('loadeddata', () => {
            video.classList.add('visible');
        });

        video.addEventListener('timeupdate', () => {
            if (video.duration && (video.duration - video.currentTime <= 0.55)) {
                video.classList.remove('visible');
            }
        });

        video.addEventListener('ended', () => {
            video.currentTime = 0;
            video.play().then(() => {
                video.classList.add('visible');
            }).catch(() => {});
        });

        // Fallback check if already cached/playing
        if (video.readyState >= 3) {
            video.classList.add('visible');
        }
    });

    // 4. BlurText Word-by-Word Staggered Motion Engine
    const blurTextElements = document.querySelectorAll('[data-blur-text]');
    blurTextElements.forEach(el => {
        const text = el.textContent.trim();
        el.textContent = '';
        el.classList.add('blur-text-container');

        const words = text.split(/\s+/);
        words.forEach((word, index) => {
            const span = document.createElement('span');
            span.className = 'blur-word';
            span.textContent = word;
            span.style.transitionDelay = `${index * 100}ms`;
            el.appendChild(span);
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const childSpans = el.querySelectorAll('.blur-word');
                    childSpans.forEach(span => span.classList.add('animated'));
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.1 });

        observer.observe(el);
    });

    // 5. Auto Dismiss Toast Notifications
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    });

    // 6. Mobile Navigation Menu Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            const isVisible = navLinks.style.display === 'flex';
            if (isVisible) {
                navLinks.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.background = '#090c12';
                navLinks.style.padding = '20px';
                navLinks.style.gap = '15px';
            }
        });
    }
});
