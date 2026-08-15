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
    initHeroScrollDampener();
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
    if (!heroSection) return;

    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (e) => {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        mouseX = (e.clientX / windowWidth) - 0.5;
        mouseY = (e.clientY / windowHeight) - 0.5;
    }, { passive: true });

    function animateParallax() {
        targetX += (mouseX - targetX) * 0.04;
        targetY += (mouseY - targetY) * 0.04;

        const activeBg = heroSection.querySelector('.hero-bg-layer.active');
        if (activeBg) {
            activeBg.style.transform = `scale(1.05) translate3d(${targetX * -15}px, ${targetY * -15}px, 0)`;
        }

        const flare = heroSection.querySelector('.hero-radial-flare');
        if (flare && document.body.classList.contains('hero-animate-active')) {
            flare.style.transform = `translate(-50%, -50%) translate3d(${targetX * 22}px, ${targetY * 22}px, 0) scale(1.1)`;
        }

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
   4. Feature Carousel (Silky Smooth Infinite Auto-Scroll with Zero Stutter)
   -------------------------------------------------------------------------- */
function initFeatureCarousel() {
    const wrapper = document.querySelector('.carousel-outer-wrapper');
    const track = document.getElementById('featureCarouselTrack');

    if (!wrapper || !track) return;

    // Dynamically clone original cards once to guarantee 100% exact width symmetry
    const originalCards = Array.from(track.children);
    originalCards.forEach(card => {
        const clone = card.cloneNode(true);
        // Strip scroll reveal animation classes from cloned cards to prevent pop glitches
        clone.classList.remove('reveal-popup', 'revealed');
        clone.style.opacity = '1';
        clone.style.transform = 'none';
        track.appendChild(clone);
    });

    let positionX = 0;
    let speed = 0.45; // Smooth luxury auto-scroll speed
    let isPaused = false;
    let isDragging = false;
    let startX = 0;
    let dragStartX = 0;
    let singleSetWidth = 0;

    function calculateWidth() {
        // Calculate exact width of original set
        singleSetWidth = track.scrollWidth / 2;
    }

    calculateWidth();
    window.addEventListener('resize', calculateWidth, { passive: true });

    function step() {
        if (!isPaused && !isDragging) {
            positionX -= speed;
            if (singleSetWidth > 0 && Math.abs(positionX) >= singleSetWidth) {
                // Smooth wrapping: add back exact width to avoid frame loss or visual jumps
                positionX += singleSetWidth;
            }
            track.style.transform = `translate3d(${positionX.toFixed(2)}px, 0, 0)`;
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

        if (singleSetWidth > 0) {
            if (positionX > 0) positionX -= singleSetWidth;
            if (Math.abs(positionX) >= singleSetWidth) positionX += singleSetWidth;
        }
        track.style.transform = `translate3d(${positionX.toFixed(2)}px, 0, 0)`;
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

        if (singleSetWidth > 0) {
            if (positionX > 0) positionX -= singleSetWidth;
            if (Math.abs(positionX) >= singleSetWidth) positionX += singleSetWidth;
        }
        track.style.transform = `translate3d(${positionX.toFixed(2)}px, 0, 0)`;
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
   7. Kinetic Hero Scroll Speed Control & Parallax Deceleration Engine
   -------------------------------------------------------------------------- */
function initHeroScrollDampener() {
    const heroSection = document.getElementById('hero');
    const heroContent = document.querySelector('.hero-content-editorial');
    const flare = document.querySelector('.hero-radial-flare');
    const statsBar = document.querySelector('.hero-stats-glass-bar');

    if (!heroSection) return;

    // Smooth Scroll Animation Frame Loop for Parallax Fade-Out
    function renderScrollEffects() {
        const scrollY = window.scrollY;
        const heroHeight = heroSection.offsetHeight || window.innerHeight;

        // Apply Parallax Fade-out & Slow Scale when scrolling out of Hero
        if (scrollY <= heroHeight * 1.1) {
            const scrollRatio = Math.min(1, scrollY / heroHeight);
            
            if (heroContent) {
                const opacity = Math.max(0, 1 - (scrollRatio * 1.35));
                const translateY = scrollY * 0.38;
                const blur = scrollRatio * 8;
                heroContent.style.transform = `translate3d(0, ${translateY.toFixed(2)}px, 0)`;
                heroContent.style.opacity = opacity.toFixed(3);
                heroContent.style.filter = `blur(${blur.toFixed(1)}px)`;
            }

            if (flare) {
                const flareOpacity = Math.max(0, 1 - (scrollRatio * 1.5));
                flare.style.opacity = flareOpacity.toFixed(3);
            }

            if (statsBar) {
                const barOpacity = Math.max(0, 1 - (scrollRatio * 1.6));
                statsBar.style.opacity = barOpacity.toFixed(3);
            }
        } else {
            // Reset inline styles when scrolled past hero
            if (heroContent) {
                heroContent.style.transform = '';
                heroContent.style.opacity = '';
                heroContent.style.filter = '';
            }
        }

        requestAnimationFrame(renderScrollEffects);
    }

    requestAnimationFrame(renderScrollEffects);

    // Smooth Click-to-Anchor Scroll (1.2s smooth glide)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetEl = document.querySelector(targetId);
                if (targetEl) {
                    e.preventDefault();
                    targetEl.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/* --------------------------------------------------------------------------
   8. Dual-Row Scroll-Driven Marquee Slide Engine
   -------------------------------------------------------------------------- */
function initMarqueeScrollSlide() {
    const row1 = document.getElementById("marqueeRow1");
    const row2 = document.getElementById("marqueeRow2");
    const section = document.getElementById("marquee");
    if (!row1 || !row2 || !section) return;

    const track1 = row1.querySelector(".marquee-track");
    const track2 = row2.querySelector(".marquee-track");

    let ticking = false;

    function updateScrollSlide() {
        const rect = section.getBoundingClientRect();
        const winHeight = window.innerHeight;
        
        if (rect.top <= winHeight && rect.bottom >= 0) {
            const scrollOffset = (window.scrollY - section.offsetTop + winHeight) * 0.35;
            
            if (track1) {
                track1.style.transform = `translate3d(${scrollOffset - 300}px, 0, 0)`;
            }
            if (track2) {
                track2.style.transform = `translate3d(${-(scrollOffset - 300)}px, 0, 0)`;
            }
        }
        ticking = false;
    }

    window.addEventListener("scroll", function() {
        if (!ticking) {
            requestAnimationFrame(updateScrollSlide);
            ticking = true;
        }
    }, { passive: true });

    updateScrollSlide();
}

document.addEventListener("DOMContentLoaded", function() {
    initMarqueeScrollSlide();
    initStickyStackingCards();
});

/* --------------------------------------------------------------------------
   9. Sticky Stacking Cards Motion Engine (3D Card Scale & Stacking)
   -------------------------------------------------------------------------- */
function initStickyStackingCards() {
    const cardSections = document.querySelectorAll(".sticky-stacking-section");
    if (!cardSections.length) return;

    function updateCardStacking() {
        cardSections.forEach(section => {
            const cards = section.querySelectorAll(".sticky-stack-card");
            if (!cards.length) return;

            const winHeight = window.innerHeight;

            cards.forEach((card, index) => {
                const offsetTop = 110 + (index * 24);
                card.style.top = `${offsetTop}px`;
                card.style.zIndex = (10 + index).toString();

                if (index < cards.length - 1) {
                    const nextCard = cards[index + 1];
                    const nextRect = nextCard.getBoundingClientRect();
                    const distance = nextRect.top - offsetTop;

                    if (distance < winHeight * 0.65) {
                        const progress = Math.max(0, Math.min(1, (winHeight * 0.65 - distance) / (winHeight * 0.65)));
                        const scale = 1 - (progress * 0.05);
                        const brightness = 1 - (progress * 0.25);
                        card.style.transform = `scale(${scale.toFixed(4)})`;
                        card.style.filter = `brightness(${brightness.toFixed(2)})`;
                    } else {
                        card.style.transform = `scale(1)`;
                        card.style.filter = `brightness(1)`;
                    }
                }
            });
        });
    }

    let ticking = false;
    window.addEventListener("scroll", function() {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateCardStacking();
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    updateCardStacking();
}

