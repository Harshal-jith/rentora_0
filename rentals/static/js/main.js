/* ==========================================================================
   RENTORA CINEMATIC HERO & SERVICE LANDING SCRIPT - SPECIFICATION V1.3
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initSeamlessVideoLoop();
    initHeroParallax();
    initParticleCanvas();
    initFeatureCarousel();
    initScrollObserver();
    initMobileNav();
});

/* --------------------------------------------------------------------------
   1. Theme Toggle & Persistence
   -------------------------------------------------------------------------- */
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const savedTheme = localStorage.getItem('rentora_theme') || 'dark';
    setTheme(savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlEl.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }

    function setTheme(theme) {
        htmlEl.setAttribute('data-theme', theme);
        document.body.className = theme === 'dark' ? 'dark-theme' : 'light-theme';
        localStorage.setItem('rentora_theme', theme);

        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        }
    }
}

/* --------------------------------------------------------------------------
   2. Custom Seamless Video Looping Engine (Fade In 0.5s / Fade Out 0.5s / 100ms reset)
   -------------------------------------------------------------------------- */
function initSeamlessVideoLoop() {
    const video = document.querySelector('.hero-video-bg');
    if (!video) return;

    let isResetting = false;

    function monitorVideoLoop() {
        if (video.duration > 0 && !isResetting) {
            const currentTime = video.currentTime;
            const duration = video.duration;
            const timeRemaining = duration - currentTime;

            // Fade in during first 0.5 seconds
            if (currentTime < 0.5) {
                const fadeOpacity = Math.min(currentTime / 0.5, 1);
                video.style.opacity = (fadeOpacity * 0.75).toString();
            }
            // Fade out during last 0.5 seconds
            else if (timeRemaining < 0.5) {
                const fadeOpacity = Math.max(timeRemaining / 0.5, 0);
                video.style.opacity = (fadeOpacity * 0.75).toString();
            }
            // Normal middle opacity
            else {
                video.style.opacity = '0.75';
            }

            // Invisible seamless restart when reaching end
            if (timeRemaining <= 0.08 || video.ended) {
                isResetting = true;
                video.style.opacity = '0';
                video.pause();

                setTimeout(() => {
                    video.currentTime = 0;
                    video.play().then(() => {
                        isResetting = false;
                    }).catch(() => {
                        isResetting = false;
                    });
                }, 100);
            }
        }
        requestAnimationFrame(monitorVideoLoop);
    }

    // Ensure video is playing
    video.play().catch(() => {});
    requestAnimationFrame(monitorVideoLoop);
}

/* --------------------------------------------------------------------------
   3. Ultra-Subtle Hero Parallax (Fixed Camera: Max 3-5px Total Movement)
   -------------------------------------------------------------------------- */
function initHeroParallax() {
    const heroSection = document.querySelector('.hero-section');
    const layer = document.querySelector('.parallax-layer');

    if (!heroSection || !layer) return;

    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (e) => {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        mouseX = (e.clientX / windowWidth) - 0.5;
        mouseY = (e.clientY / windowHeight) - 0.5;
    }, { passive: true });

    function animateParallax() {
        targetX += (mouseX - targetX) * 0.025;
        targetY += (mouseY - targetY) * 0.025;

        if (layer) layer.style.transform = `scale(1.03) translate3d(${targetX * 3.5}px, ${targetY * 3.5}px, 0)`;

        requestAnimationFrame(animateParallax);
    }

    requestAnimationFrame(animateParallax);
}

/* --------------------------------------------------------------------------
   4. Ambient Slow Floating Particle Canvas
   -------------------------------------------------------------------------- */
function initParticleCanvas() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }, { passive: true });

    const particles = [];
    const particleCount = 28;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 1.2 + 0.4,
            alpha: Math.random() * 0.35 + 0.05,
            speedY: Math.random() * 0.15 + 0.05,
            speedX: (Math.random() - 0.5) * 0.1
        });
    }

    function renderParticles() {
        ctx.clearRect(0, 0, width, height);

        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(214, 181, 108, ${p.alpha})`;
            ctx.fill();

            p.y -= p.speedY;
            p.x += p.speedX;

            if (p.y < 0) {
                p.y = height + 10;
                p.x = Math.random() * width;
            }
        });

        requestAnimationFrame(renderParticles);
    }

    requestAnimationFrame(renderParticles);
}

/* --------------------------------------------------------------------------
   5. Feature Carousel (Auto-Scroll + Mouse Drag + Touch Swipe)
   -------------------------------------------------------------------------- */
function initFeatureCarousel() {
    const wrapper = document.querySelector('.carousel-outer-wrapper');
    const track = document.getElementById('featureCarouselTrack');

    if (!wrapper || !track) return;

    let positionX = 0;
    let speed = 0.42;
    let isPaused = false;
    let isDragging = false;
    let startX = 0;
    let dragStartX = 0;

    function getHalfWidth() {
        return track.scrollWidth / 2;
    }

    function step() {
        if (!isPaused && !isDragging) {
            positionX -= speed;
            const halfWidth = getHalfWidth();
            if (halfWidth > 0 && Math.abs(positionX) >= halfWidth) {
                positionX = 0;
            }
            track.style.transform = `translate3d(${positionX}px, 0, 0)`;
        }
        requestAnimationFrame(step);
    }

    wrapper.addEventListener('mouseenter', () => { isPaused = true; }, { passive: true });
    wrapper.addEventListener('mouseleave', () => {
        isPaused = false;
        isDragging = false;
    }, { passive: true });

    wrapper.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.pageX;
        dragStartX = positionX;
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const diff = e.pageX - startX;
        positionX = dragStartX + diff;
        
        const halfWidth = getHalfWidth();
        if (halfWidth > 0) {
            if (positionX > 0) positionX = -halfWidth + (positionX % halfWidth);
            if (Math.abs(positionX) >= halfWidth) positionX = positionX % halfWidth;
        }
        track.style.transform = `translate3d(${positionX}px, 0, 0)`;
    });

    window.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            isPaused = false;
        }
    });

    wrapper.addEventListener('touchstart', (e) => {
        isDragging = true;
        startX = e.touches[0].pageX;
        dragStartX = positionX;
    }, { passive: true });

    wrapper.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        const diff = e.touches[0].pageX - startX;
        positionX = dragStartX + diff;
        
        const halfWidth = getHalfWidth();
        if (halfWidth > 0) {
            if (positionX > 0) positionX = -halfWidth + (positionX % halfWidth);
            if (Math.abs(positionX) >= halfWidth) positionX = positionX % halfWidth;
        }
        track.style.transform = `translate3d(${positionX}px, 0, 0)`;
    }, { passive: true });

    wrapper.addEventListener('touchend', () => {
        isDragging = false;
        isPaused = false;
    }, { passive: true });

    requestAnimationFrame(step);
}

/* --------------------------------------------------------------------------
   6. Scroll Intersection Observer for Staggered Blur Pop Reveals
   -------------------------------------------------------------------------- */
function initScrollObserver() {
    const revealElements = document.querySelectorAll('.reveal-on-scroll, .reveal-popup');
    if (!revealElements.length) return;

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('is-visible');
                }, index * 90);
                obs.unobserve(entry.target);
            }
        });
    }, observerOptions);

    revealElements.forEach(el => {
        observer.observe(el);
    });
}

/* --------------------------------------------------------------------------
   7. Mobile Navigation Menu Toggle
   -------------------------------------------------------------------------- */
function initMobileNav() {
    const mobileBtn = document.getElementById('mobileToggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            const isOpen = navLinks.style.display === 'flex';
            navLinks.style.display = isOpen ? 'none' : 'flex';
            if (!isOpen) {
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.background = 'rgba(20, 20, 20, 0.95)';
                navLinks.style.padding = '20px';
                navLinks.style.borderRadius = '16px';
                navLinks.style.marginTop = '10px';
                navLinks.style.border = '1px solid var(--border-gold)';
            }
        });
    }
}
