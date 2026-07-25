/* ==========================================================================
   RENTORA LANDING PAGE REFINEMENT INTERACTION SCRIPT - SPECIFICATION V1.1
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initHeroParallax();
    initParticleCanvas();
    initFeatureCarousel();
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
   2. 3-Layer Subtle Mouse Parallax (Hero Section: Max 3-8px Offset)
   -------------------------------------------------------------------------- */
function initHeroParallax() {
    const heroSection = document.querySelector('.hero-section');
    const layerBg = document.querySelector('.parallax-bg');
    const layerMid = document.querySelector('.parallax-mid');
    const layerFg = document.querySelector('.parallax-fg');

    if (!heroSection || !layerBg) return;

    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (e) => {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        mouseX = (e.clientX / windowWidth) - 0.5;
        mouseY = (e.clientY / windowHeight) - 0.5;
    }, { passive: true });

    function animateParallax() {
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        if (layerBg) layerBg.style.transform = `scale(1.05) translate3d(${targetX * 4}px, ${targetY * 4}px, 0)`;
        if (layerMid) layerMid.style.transform = `scale(1.03) translate3d(${targetX * 7}px, ${targetY * 7}px, 0)`;
        if (layerFg) layerFg.style.transform = `scale(1.02) translate3d(${targetX * 11}px, ${targetY * 11}px, 0)`;

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
    const particleCount = 35;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 1.5 + 0.5,
            alpha: Math.random() * 0.5 + 0.1,
            speedY: Math.random() * 0.3 + 0.1,
            speedX: (Math.random() - 0.5) * 0.2
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
   4. RENTORA ADVANTAGE HORIZONTAL FEATURE CAROUSEL (Infinite Auto-Scroll + Drag/Touch)
   -------------------------------------------------------------------------- */
function initFeatureCarousel() {
    const wrapper = document.querySelector('.carousel-outer-wrapper');
    const track = document.getElementById('featureCarouselTrack');

    if (!wrapper || !track) return;

    let positionX = 0;
    let speed = 0.8;
    let isPaused = false;
    let isDragging = false;
    let startX = 0;
    let dragStartX = 0;
    let animationFrameId = null;

    // Total width of half the cards (for seamless infinite loop)
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
        animationFrameId = requestAnimationFrame(step);
    }

    // Pause / Resume on Hover
    wrapper.addEventListener('mouseenter', () => { isPaused = true; }, { passive: true });
    wrapper.addEventListener('mouseleave', () => {
        isPaused = false;
        isDragging = false;
    }, { passive: true });

    // Mouse Drag Handlers
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

    // Touch Swipe Handlers (Mobile)
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
   5. Mobile Navigation Menu Toggle
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
