/* ==========================================================================
   RENTORA CINEMATIC LANDING PAGE INTERACTION SCRIPT - SPECIFICATION V1.0
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initHeroParallax();
    initParticleCanvas();
    initScrollMarquee();
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
            if (theme === 'dark') {
                themeIcon.className = 'fa-solid fa-sun';
            } else {
                themeIcon.className = 'fa-solid fa-moon';
            }
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

        // Calculate normalized offset (-0.5 to 0.5)
        mouseX = (e.clientX / windowWidth) - 0.5;
        mouseY = (e.clientY / windowHeight) - 0.5;
    }, { passive: true });

    function animateParallax() {
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        // Apply smooth 3px, 5px, 8px subtle parallax movements
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
   4. Scroll-Driven Dual-Row Marquee (3D Creator Linked Motion)
   -------------------------------------------------------------------------- */
function initScrollMarquee() {
    const rowTop = document.querySelector('.marquee-row-top');
    const rowBottom = document.querySelector('.marquee-row-bottom');

    if (!rowTop || !rowBottom) return;

    let currentScroll = window.scrollY;
    let targetScroll = currentScroll;
    let ease = 0.08;

    window.addEventListener('scroll', () => {
        targetScroll = window.scrollY;
    }, { passive: true });

    function updateMarquee() {
        currentScroll += (targetScroll - currentScroll) * ease;

        // Top Row moves RIGHT at 1.0x, Bottom Row moves LEFT at 0.82x
        const shiftTop = (currentScroll * 0.35) % 1200;
        const shiftBottom = (-currentScroll * 0.28) % 1200;

        rowTop.style.transform = `translate3d(${shiftTop}px, 0, 0)`;
        rowBottom.style.transform = `translate3d(${shiftBottom}px, 0, 0)`;

        requestAnimationFrame(updateMarquee);
    }

    requestAnimationFrame(updateMarquee);
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
