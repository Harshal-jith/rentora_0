/* ==========================================================================
   RENTORA ANIMATION REFINEMENT SCRIPT - SPECIFICATION V1.2
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initHeroSlideshow();
    initSeamlessAuthVideoLoop();
    initHeroParallax();
    initParticleCanvas();
    initFeatureCarousel();
    initScrollObserver();
    initMobileNav();
    initHeroStatsCounter();
});

/* --------------------------------------------------------------------------
   Seamless Video Background Looper (0.5s Opacity Fade In/Out via rAF)
   -------------------------------------------------------------------------- */
function initSeamlessAuthVideoLoop() {
    const video = document.getElementById('authBgVideo');
    if (!video) return;

    let isResetting = false;

    function monitorLoop() {
        if (video.duration && !isResetting) {
            const timeRemaining = video.duration - video.currentTime;

            if (video.currentTime < 0.5) {
                const opacity = (video.currentTime / 0.5) * 0.72;
                video.style.opacity = opacity.toFixed(2);
            } else if (timeRemaining < 0.5) {
                const opacity = (timeRemaining / 0.5) * 0.72;
                video.style.opacity = opacity.toFixed(2);
            } else {
                video.style.opacity = '0.72';
            }

            if (timeRemaining <= 0.12) {
                isResetting = true;
                video.style.opacity = '0';
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
        requestAnimationFrame(monitorLoop);
    }

    video.addEventListener('loadedmetadata', () => {
        requestAnimationFrame(monitorLoop);
    });

    if (video.readyState >= 1) {
        requestAnimationFrame(monitorLoop);
    }
}

/* --------------------------------------------------------------------------
   Hero Dynamic Background Slideshow (Butter-Smooth Dual-Layer Crossfade)
   -------------------------------------------------------------------------- */
function initHeroSlideshow() {
    const layerA = document.getElementById('bgLayerA');
    const layerB = document.getElementById('bgLayerB');
    if (!layerA || !layerB) return;

    const bgImages = [
        '/static/images/hero_mid_villa_1784964394119.jpg',
        '/static/images/scene_night_exterior_1784963519950.jpg',
        '/static/images/scene_kerala_estate_1784963501632.jpg',
        '/static/images/hero_fg_pool_1784964408615.jpg'
    ];

    let currentIndex = 0;
    let activeLayer = layerA;
    let inactiveLayer = layerB;

    setInterval(() => {
        currentIndex = (currentIndex + 1) % bgImages.length;
        const nextImage = bgImages[currentIndex];

        // Prepare inactive layer with next image
        inactiveLayer.style.backgroundImage = `url('${nextImage}')`;
        inactiveLayer.classList.add('active');
        activeLayer.classList.remove('active');

        // Swap active and inactive layer pointers
        const temp = activeLayer;
        activeLayer = inactiveLayer;
        inactiveLayer = temp;
    }, 5500);
}

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
   2. Ultra-Subtle Hero Parallax (Fixed Camera: Max 3-5px Total Movement)
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

        // Strictly capped between 2px and 3.5px max offset
        if (layer) layer.style.transform = `scale(1.03) translate3d(${targetX * 3.5}px, ${targetY * 3.5}px, 0)`;

        requestAnimationFrame(animateParallax);
    }

    requestAnimationFrame(animateParallax);
}

/* --------------------------------------------------------------------------
   3. Ambient Slow Floating Particle Canvas
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
   4. Feature Carousel (Slowing speed by ~45%: 0.42 speed with smooth drag)
   -------------------------------------------------------------------------- */
function initFeatureCarousel() {
    const wrapper = document.querySelector('.carousel-outer-wrapper');
    const track = document.getElementById('featureCarouselTrack');

    if (!wrapper || !track) return;

    let positionX = 0;
    let speed = 0.42; // Reduced speed for calm, luxury auto-scroll
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
   5. Scroll Intersection Observer for Slow 1.0s Blur/Fade Reveals (Staggered)
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
   6. Mobile Navigation Menu Toggle
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

/* --------------------------------------------------------------------------
   Animated Hero Stats Metrics Counter (Ported from premium-rentals.git)
   -------------------------------------------------------------------------- */
function initHeroStatsCounter() {
    const counters = document.querySelectorAll('.hero-counter');
    if (!counters.length) return;

    counters.forEach(counterEl => {
        const target = parseFloat(counterEl.getAttribute('data-target'));
        if (isNaN(target)) return;
        const prefix = counterEl.getAttribute('data-prefix') || '';
        const suffix = counterEl.getAttribute('data-suffix') || '';
        const isFloat = target % 1 !== 0;

        let current = 0;
        const duration = 1200; // ms
        const steps = 40;
        const increment = target / steps;
        const stepTime = duration / steps;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            const formattedVal = isFloat ? current.toFixed(1) : Math.floor(current);
            counterEl.textContent = `${prefix}${formattedVal}${suffix}`;
        }, stepTime);
    });
}
