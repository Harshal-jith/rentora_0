document.addEventListener('DOMContentLoaded', () => {
  // Register GSAP Plugins
  gsap.registerPlugin(ScrollTrigger);

  // Global Lenis Smooth Scroll Initialization (Desktop / Fine-Pointer Only)
  const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (window.matchMedia && window.matchMedia('(pointer: coarse)').matches);
  if (typeof Lenis !== 'undefined' && !isTouchDevice) {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1.0,
      infinite: false,
    });

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });

    gsap.ticker.lagSmoothing(0);
    window.lenis = lenis;
  }

  // Day & Night Mode Lighting Switcher
  const dayBtn = document.getElementById('day-btn');
  const nightBtn = document.getElementById('night-btn');
  const daySlides = document.querySelectorAll('.day-slide');
  const nightSlides = document.querySelectorAll('.night-slide');
  const isHeroPage = document.getElementById('hero-loader') !== null ||
                     document.getElementById('imagery') !== null ||
                     document.querySelector('section[aria-label="Hero"]') !== null ||
                     window.location.pathname === '/' ||
                     window.location.pathname.endsWith('/home/');
  let isNightMode = localStorage.getItem('rentora_theme') === 'night';

  function setLightingMode(night) {
    if (isHeroPage) {
      document.documentElement.classList.remove('night-mode', 'light-mode');
      document.body.classList.remove('night-mode', 'light-mode');
      return; // Completely isolate hero page from theme switching
    }
    isNightMode = night;
    localStorage.setItem('rentora_theme', night ? 'night' : 'day');
    
    if (night) {
      document.documentElement.classList.add('night-mode');
      document.body.classList.add('night-mode');
      document.body.classList.remove('light-mode');
      if (nightBtn) {
        nightBtn.className = "px-2.5 py-1 text-[0.65rem] uppercase tracking-widest rounded-full transition-all duration-300 theme-switch-btn-active font-semibold shadow-sm";
      }
      if (dayBtn) {
        dayBtn.className = "px-2.5 py-1 text-[0.65rem] uppercase tracking-widest rounded-full transition-all duration-300 theme-switch-btn-inactive";
      }

      daySlides.forEach(slide => slide.style.opacity = '0');
      if (nightSlides[0]) nightSlides[0].style.opacity = '1';
    } else {
      document.documentElement.classList.remove('night-mode');
      document.body.classList.remove('night-mode');
      document.body.classList.add('light-mode');
      if (dayBtn) {
        dayBtn.className = "px-2.5 py-1 text-[0.65rem] uppercase tracking-widest rounded-full transition-all duration-300 theme-switch-btn-active font-semibold shadow-sm";
      }
      if (nightBtn) {
        nightBtn.className = "px-2.5 py-1 text-[0.65rem] uppercase tracking-widest rounded-full transition-all duration-300 theme-switch-btn-inactive";
      }

      nightSlides.forEach(slide => slide.style.opacity = '0');
      if (daySlides[0]) daySlides[0].style.opacity = '1';
    }
  }

  // If on hero page, completely strip night-mode/light-mode body classes
  if (isHeroPage) {
    document.documentElement.classList.remove('night-mode', 'light-mode');
    document.body.classList.remove('night-mode', 'light-mode');
  } else {
    // Initialize saved theme preference for interior & post-login pages
    setLightingMode(isNightMode);

    if (dayBtn && nightBtn) {
      dayBtn.addEventListener('click', () => setLightingMode(false));
      nightBtn.addEventListener('click', () => setLightingMode(true));
    }
  }

  window.addEventListener('pageshow', () => {
    if (isHeroPage) {
      document.documentElement.classList.remove('night-mode', 'light-mode');
      document.body.classList.remove('night-mode', 'light-mode');
    }
  });

  // ----------------------------------------------------
  // 2. APARTMENT SPECS FILTER TABS
  // ----------------------------------------------------
  const aptTabs = document.querySelectorAll('.apartment-tab');
  const aptCards = document.querySelectorAll('.apt-card');

  aptTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const type = tab.getAttribute('data-type');

      aptTabs.forEach(t => {
        t.classList.remove('active');
      });

      tab.classList.add('active');

      aptCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (type === 'all' || category === type) {
          card.style.display = 'flex';
          gsap.fromTo(card, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5 });
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // ----------------------------------------------------
  // 3. BOOK A CALL MODAL POPUP
  // ----------------------------------------------------
  const callModal = document.getElementById('call-modal');
  const closeModalBtn = document.getElementById('close-modal');
  const bookCallBtns = document.querySelectorAll('#book-call-btn, #book-call-btn-mobile, .open-inquiry-btn');

  bookCallBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      if (callModal) {
        callModal.classList.remove('opacity-0', 'pointer-events-none');
      }
    });
  });

  if (closeModalBtn && callModal) {
    closeModalBtn.addEventListener('click', () => {
      callModal.classList.add('opacity-0', 'pointer-events-none');
    });
    callModal.addEventListener('click', (e) => {
      if (e.target === callModal) {
        callModal.classList.add('opacity-0', 'pointer-events-none');
      }
    });
  }

  // ----------------------------------------------------
  // 3B. SIGN UP & LOG IN MODAL POPUP
  // ----------------------------------------------------
  const authModal = document.getElementById('auth-modal');
  const closeAuthModalBtn = document.getElementById('close-auth-modal');
  const loginBtns = document.querySelectorAll('.open-login-btn');
  const signupBtns = document.querySelectorAll('.open-signup-btn');
  const tabLogin = document.getElementById('tab-login');
  const tabSignup = document.getElementById('tab-signup');
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const switchToSignup = document.getElementById('switch-to-signup');
  const switchToLogin = document.getElementById('switch-to-login');

  function showAuthTab(mode) {
    if (mode === 'login') {
      if (loginForm) loginForm.classList.remove('hidden');
      if (signupForm) signupForm.classList.add('hidden');
      if (tabLogin) {
        tabLogin.classList.add('active');
        tabLogin.classList.remove('inactive');
      }
      if (tabSignup) {
        tabSignup.classList.remove('active');
        tabSignup.classList.add('inactive');
      }
    } else {
      if (signupForm) signupForm.classList.remove('hidden');
      if (loginForm) loginForm.classList.add('hidden');
      if (tabSignup) {
        tabSignup.classList.add('active');
        tabSignup.classList.remove('inactive');
      }
      if (tabLogin) {
        tabLogin.classList.remove('active');
        tabLogin.classList.add('inactive');
      }
    }
  }

  loginBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      showAuthTab('login');
      if (authModal) authModal.classList.remove('opacity-0', 'pointer-events-none');
    });
  });

  signupBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      showAuthTab('signup');
      if (authModal) authModal.classList.remove('opacity-0', 'pointer-events-none');
    });
  });

  if (tabLogin && tabSignup) {
    tabLogin.addEventListener('click', () => showAuthTab('login'));
    tabSignup.addEventListener('click', () => showAuthTab('signup'));
  }

  if (switchToSignup) switchToSignup.addEventListener('click', () => showAuthTab('signup'));
  if (switchToLogin) switchToLogin.addEventListener('click', () => showAuthTab('login'));

  if (closeAuthModalBtn && authModal) {
    closeAuthModalBtn.addEventListener('click', () => {
      authModal.classList.add('opacity-0', 'pointer-events-none');
    });
    authModal.addEventListener('click', (e) => {
      if (e.target === authModal) {
        authModal.classList.add('opacity-0', 'pointer-events-none');
      }
    });
  }

  // ----------------------------------------------------
  // 3C. INLINE SIGN UP & LOG IN PORTAL (BOTTOM SECTION)
  // ----------------------------------------------------
  const inlineTabLogin = document.getElementById('inline-tab-login');
  const inlineTabSignup = document.getElementById('inline-tab-signup');
  const inlineLoginForm = document.getElementById('inline-login-form');
  const inlineSignupForm = document.getElementById('inline-signup-form');
  const inlineSwitchToSignup = document.getElementById('inline-switch-to-signup');
  const inlineSwitchToLogin = document.getElementById('inline-switch-to-login');

  function showInlineAuthTab(mode) {
    if (mode === 'login') {
      if (inlineLoginForm) inlineLoginForm.classList.remove('hidden');
      if (inlineSignupForm) inlineSignupForm.classList.add('hidden');
      if (inlineTabLogin) {
        inlineTabLogin.classList.add('active');
        inlineTabLogin.classList.remove('inactive');
      }
      if (inlineTabSignup) {
        inlineTabSignup.classList.remove('active');
        inlineTabSignup.classList.add('inactive');
      }
    } else {
      if (inlineSignupForm) inlineSignupForm.classList.remove('hidden');
      if (inlineLoginForm) inlineLoginForm.classList.add('hidden');
      if (inlineTabSignup) {
        inlineTabSignup.classList.add('active');
        inlineTabSignup.classList.remove('inactive');
      }
      if (inlineTabLogin) {
        inlineTabLogin.classList.remove('active');
        inlineTabLogin.classList.add('inactive');
      }
    }
  }

  if (inlineTabLogin && inlineTabSignup) {
    inlineTabLogin.addEventListener('click', () => showInlineAuthTab('login'));
    inlineTabSignup.addEventListener('click', () => showInlineAuthTab('signup'));
  }

  if (inlineSwitchToSignup) inlineSwitchToSignup.addEventListener('click', () => showInlineAuthTab('signup'));
  if (inlineSwitchToLogin) inlineSwitchToLogin.addEventListener('click', () => showInlineAuthTab('login'));



  // ----------------------------------------------------
  // 4. MOBILE MENU DRAWER TOGGLE
  // ----------------------------------------------------
  const openMenuBtn = document.getElementById('open-menu');
  const closeMenuBtn = document.getElementById('close-menu');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  if (openMenuBtn && closeMenuBtn && mobileMenu) {
    openMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.remove('translate-x-full');
    });
    closeMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.add('translate-x-full');
    });
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('translate-x-full');
      });
    });
  }

  // ----------------------------------------------------
  // 5. ULTRA-SMOOTH CINEMATIC INTRO HERO LOADER
  // ----------------------------------------------------
  const loaderEl = document.getElementById('hero-loader');
  const hasMessagesOrForm = document.querySelector('.bg-red-950\\/80') || window.location.hash || window.location.search;

  function playHeroEntrance() {
    gsap.to('.hero-fade-word', {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.03,
      ease: 'power3.out'
    });

    gsap.to('.hero-fade-in', {
      opacity: 1,
      y: 0,
      duration: 0.5,
      stagger: 0.08,
      ease: 'power2.out',
      delay: 0.05
    });
  }

  if (loaderEl && hasMessagesOrForm) {
    loaderEl.style.display = 'none';
    loaderEl.style.pointerEvents = 'none';
    playHeroEntrance();
    setTimeout(() => {
      if (typeof ScrollTrigger !== 'undefined') {
        ScrollTrigger.refresh();
      }
    }, 100);
  } else if (loaderEl) {
    const loaderBox = document.querySelector('.hero-loader__box');
    const growingImgBox = document.querySelector('.hero-loader__growing-image');
    const loaderStartWord = document.querySelector('.hero-loader__word--start');
    const loaderEndWord = document.querySelector('.hero-loader__word--end');
    const loaderSlides = Array.from(document.querySelectorAll('.loader-img-slide'));
    
    // Ensure all loader images are preloaded into browser cache immediately for 0ms rendering
    loaderSlides.forEach(slide => {
      const img = slide.querySelector('img');
      if (img && img.src) {
        const pImg = new Image();
        pImg.src = img.src;
      }
    });

    const isMobile = window.innerWidth < 640;
    const targetWidth = isMobile ? '80px' : '160px';

    // Initial setup: Slide 0 visible with gentle scale, other slides ready with 0 opacity
    loaderSlides.forEach((slide, i) => {
      gsap.set(slide, {
        opacity: i === 0 ? 1 : 0,
        scale: 1.14,
        force3D: true
      });
    });

    // Master GSAP Intro Loader Timeline with buttery 120 FPS transitions
    const introTl = gsap.timeline({
      defaults: { ease: 'power2.inOut' },
      onComplete: () => {
        if (loaderEl) {
          loaderEl.style.pointerEvents = 'none';
          gsap.to(loaderEl, {
            opacity: 0,
            duration: 0.35,
            ease: 'power2.inOut',
            onComplete: () => {
              loaderEl.style.display = 'none';
              playHeroEntrance();
              setTimeout(() => {
                if (typeof ScrollTrigger !== 'undefined') {
                  ScrollTrigger.refresh();
                }
              }, 100);
            }
          });
        } else {
          playHeroEntrance();
          setTimeout(() => {
            if (typeof ScrollTrigger !== 'undefined') {
              ScrollTrigger.refresh();
            }
          }, 100);
        }
      }
    });

  // Step 1: Hold intact RENTORA logo briefly (0.35s)
  introTl.to({}, { duration: 0.35 });

  // Step 2: Line appears gracefully between RENT and ORA (0.3s)
  introTl.to(loaderBox, {
    width: '3px',
    opacity: 1,
    margin: '0 0.2rem',
    duration: 0.3,
    ease: 'power2.out'
  });

  // Step 3: Line opens smoothly into the image portal slot (0.5s)
  introTl.to(loaderBox, {
    width: targetWidth,
    margin: '0 0.45rem',
    borderRadius: '8px',
    duration: 0.5,
    ease: 'power3.inOut'
  });

  introTl.to(growingImgBox, {
    opacity: 1,
    duration: 0.35,
    ease: 'power2.inOut'
  }, '<+=0.1');

  // Step 4: Silky Ken-Burns image crossfades inside the opened slot
  // Slide 0 Ken-Burns drift
  introTl.to(loaderSlides[0], {
    scale: 1.0,
    duration: 0.75,
    ease: 'power1.out'
  }, '<');

  // Smooth Crossfade to Slide 1 (Munnar Tea Highlands)
  if (loaderSlides[1]) {
    introTl.to(loaderSlides[1], {
      opacity: 1,
      scale: 1.0,
      duration: 0.65,
      ease: 'power1.inOut'
    }, '+=0.08')
    .set(loaderSlides[0], { opacity: 0 });
  }

  // Smooth Crossfade to Slide 2 (Varkala Cliffside Ocean Residence)
  if (loaderSlides[2]) {
    introTl.to(loaderSlides[2], {
      opacity: 1,
      scale: 1.0,
      duration: 0.65,
      ease: 'power1.inOut'
    }, '+=0.08')
    .set(loaderSlides[1], { opacity: 0 });
  }

  // Smooth Crossfade to Final Slide 3 (Kumarakom Water Pavilion - matches Hero Slide 1)
  if (loaderSlides[3]) {
    introTl.to(loaderSlides[3], {
      opacity: 1,
      scale: 1.0,
      duration: 0.65,
      ease: 'power1.inOut'
    }, '+=0.08')
    .set(loaderSlides[2], { opacity: 0 });
  }

  // Step 5: Smooth Cinematic Zoom to Full Viewport
  introTl.to([loaderStartWord, loaderEndWord], {
    width: 0,
    opacity: 0,
    margin: 0,
    padding: 0,
    duration: 0.65,
    ease: 'power4.inOut'
  }, '+=0.1');

  introTl.to(loaderBox, {
    width: '100vw',
    height: '100vh',
    borderRadius: '0px',
    margin: 0,
    duration: 0.7,
    ease: 'power4.inOut'
  }, '<');
  }


  // ----------------------------------------------------
  // 6. HERO BACKGROUND CAROUSEL
  // ----------------------------------------------------
  const prevBtn = document.getElementById('prev-slide');
  const nextBtn = document.getElementById('next-slide');
  let currentSlide = 0;
  let carouselTimer = null;

  function showSlide(index) {
    const activeSlides = isNightMode ? nightSlides : daySlides;
    if (!activeSlides.length) return;
    
    activeSlides.forEach((slide, i) => {
      slide.style.opacity = i === index ? '1' : '0';
    });
    currentSlide = index;
  }

  function nextSlide() {
    const activeSlides = isNightMode ? nightSlides : daySlides;
    if (!activeSlides.length) return;
    const nextIdx = (currentSlide + 1) % activeSlides.length;
    showSlide(nextIdx);
  }

  function prevSlide() {
    const activeSlides = isNightMode ? nightSlides : daySlides;
    if (!activeSlides.length) return;
    const prevIdx = (currentSlide - 1 + activeSlides.length) % activeSlides.length;
    showSlide(prevIdx);
  }

  if (nextBtn && prevBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      resetCarouselTimer();
    });
    prevBtn.addEventListener('click', () => {
      prevSlide();
      resetCarouselTimer();
    });
  }

  function resetCarouselTimer() {
    if (carouselTimer) clearInterval(carouselTimer);
    carouselTimer = setInterval(nextSlide, 5000);
  }
  resetCarouselTimer();

  // ----------------------------------------------------
  // 7. STATEMENT WORD SCROLL SCRUBBING
  // ----------------------------------------------------
  const statementTextEl = document.querySelector('.statement-text');
  if (statementTextEl) {
    const rawText = statementTextEl.textContent.trim();
    const words = rawText.split(/\s+/);
    statementTextEl.innerHTML = words.map(w => `<span class="statement-word inline-block mr-[0.25em]">${w}</span>`).join('');
  }

  const statementWords = document.querySelectorAll('.statement-word');
  const statementSection = document.getElementById('opportunity');
  
  if (statementWords.length > 0 && statementSection) {
    gsap.set(statementWords, { opacity: 0.12, y: 0 });
    
    gsap.to(statementWords, {
      opacity: 1,
      ease: 'none',
      stagger: { each: 0.05, from: 'start' },
      scrollTrigger: {
        trigger: statementSection,
        start: 'top 75%',
        end: 'bottom 60%',
        scrub: 0.8
      }
    });

    gsap.fromTo('.statement-star', 
      { opacity: 0, scale: 0.4, rotate: -120 },
      {
        opacity: 1,
        scale: 1,
        rotate: 0,
        duration: 1.4,
        ease: 'expo.out',
        scrollTrigger: {
          trigger: statementSection,
          start: 'top 80%',
          toggleActions: 'play none none reverse'
        }
      }
    );
  }

  // ----------------------------------------------------
  // 8. ERA RESIDENCE SIGNATURE HORIZONTAL SCROLL SHOWCASE (GSAP MULTI-LAYER PARALLAX TIMELINE)
  // ----------------------------------------------------
  const horizontalSection = document.getElementById('stay');
  const horizontalTrack = document.querySelector('.horizontal-track');
  const horizontalPanels = document.querySelectorAll('.horizontal-panel');
  const horizontalProgressFill = document.getElementById('horizontal-progress-fill');
  const horizontalSlideNum = document.getElementById('horizontal-slide-num');
  const verticalScrollBar = document.getElementById('vertical-scroll-bar');

  if (horizontalSection && horizontalTrack && horizontalPanels.length > 0) {
    const totalPanels = horizontalPanels.length;
    const isDesktop = window.matchMedia('(min-width: 768px)').matches;

    if (isDesktop) {
      // Ensure track width is 300vw and panels do not shrink
      horizontalTrack.style.width = `${totalPanels * 100}vw`;
      horizontalTrack.style.display = 'flex';
      horizontalTrack.style.flexWrap = 'nowrap';
      horizontalPanels.forEach(panel => {
        panel.style.width = '100vw';
        panel.style.minWidth = '100vw';
        panel.style.flexShrink = '0';
      });

      // Master Horizontal Scroll Timeline with Rock-Solid Screen Pinning
      const hTl = gsap.timeline({
        scrollTrigger: {
          trigger: horizontalSection,
          pin: true,
          pinSpacing: true,
          anticipatePin: 1,
          fastScrollEnd: true,
          preventOverlaps: true,
          scrub: 1,
          start: 'top top',
          end: () => `+=${Math.max(100, Math.round(horizontalTrack.scrollWidth - window.innerWidth))}`,
          invalidateOnRefresh: true,

          onUpdate: (self) => {
            const progress = self.progress;
            
            if (horizontalProgressFill) {
              horizontalProgressFill.style.transform = `scaleX(${progress})`;
            }

            if (verticalScrollBar) {
              verticalScrollBar.style.transform = `scaleY(${progress})`;
            }

            const currentIdx = Math.min(
              totalPanels,
              Math.floor(progress * totalPanels + 0.05) + 1
            );
            if (horizontalSlideNum) {
              horizontalSlideNum.textContent = `0${currentIdx} / 0${totalPanels}`;
            }
          }
        }
      });

      // 1. Horizontal Track Translation
      hTl.to(horizontalTrack, {
        x: () => -(horizontalTrack.scrollWidth - window.innerWidth),
        ease: 'none',
        duration: 3,
        force3D: true,
        autoRound: false
      }, 0);

      // 2. Multi-Plane Botanical Canopy Parallax (ERA Residence Multi-Layer Motion)
      hTl.to('.top-left-canopy', {
        x: -220,
        rotate: -3,
        ease: 'none',
        duration: 3,
        force3D: true
      }, 0);

      hTl.to('.top-right-canopy', {
        x: -160,
        rotate: 3,
        ease: 'none',
        duration: 3,
        force3D: true
      }, 0);

      hTl.to('.panel-ground-bush', {
        x: -320,
        y: -15,
        ease: 'none',
        duration: 3,
        force3D: true
      }, 0);

      // 3. Panel 1 (THE CONCEPT) Content Scale & Fade Out as Panel 2 Enters
      hTl.fromTo('.panel-1-content',
        { opacity: 1, scale: 1, y: 0 },
        { opacity: 0.15, scale: 0.94, y: -25, ease: 'power1.in', duration: 0.8 },
        0.2
      );

      // 4. Panel 2 (RESIDENCES / EMERALD WATERS) Entrance & Parallax Scaling
      hTl.fromTo('.panel-2-text',
        { opacity: 0.1, y: 40, x: 70 },
        { opacity: 1, y: 0, x: 0, ease: 'power2.out', duration: 0.75 },
        0.7
      );

      hTl.fromTo('.panel-2-image',
        { opacity: 0.2, scale: 0.88, x: 90 },
        { opacity: 1, scale: 1.0, x: 0, ease: 'power2.out', duration: 0.75 },
        0.7
      );

      hTl.fromTo('.panel-2-image img',
        { scale: 1.25, x: 60 },
        { scale: 1.0, x: 0, ease: 'none', duration: 1.2 },
        0.7
      );

      // Panel 2 Exit
      hTl.to(['.panel-2-text', '.panel-2-image'],
        { opacity: 0.2, y: -30, ease: 'power1.in', duration: 0.7 },
        1.7
      );

      // 5. Panel 3 (WELLBEING & CONCIERGE) Entrance & Staggered Feature Cascade
      hTl.fromTo('.panel-3-text',
        { opacity: 0.1, y: 45, x: 85 },
        { opacity: 1, y: 0, x: 0, ease: 'power2.out', duration: 0.8 },
        1.9
      );

      hTl.fromTo('.panel-3-features > div',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, stagger: 0.12, ease: 'power2.out', duration: 0.6 },
        2.2
      );

      // Refresh ScrollTrigger when window finishes loading
      window.addEventListener('load', () => {
        ScrollTrigger.refresh();
      });
    } else {
      horizontalTrack.style.width = '100%';
      horizontalTrack.style.flexDirection = 'column';
      horizontalPanels.forEach(panel => {
        panel.style.width = '100%';
        panel.style.height = 'auto';
        panel.style.padding = '4rem 1.5rem';
      });
    }
  }

  // ----------------------------------------------------
  // 9. THE 3 CARDS JOINING & PARALLAX ANIMATION (#place)
  // ----------------------------------------------------
  const pillarsSection = document.getElementById('place');
  const pillars = Array.from(document.querySelectorAll('.rentora-pillar'));
  const pillarImgs = Array.from(document.querySelectorAll('.pillar-img'));
  
  if (pillarsSection && pillars.length > 0) {
    const isDesktop = window.matchMedia('(min-width: 768px)').matches;
    // Refined Stagger: Card 1 starts +160px down, Card 2 starts +80px down, Card 3 at 0px
    const initialOffsets = isDesktop ? [160, 80, 0] : [80, 40, 0];

    gsap.set(pillars, { 
      y: i => initialOffsets[i] ?? 0,
      force3D: true
    });

    // Master ScrollTrigger for the 3 Pillar Cards aligning early as user enters section
    const pTl = gsap.timeline({
      scrollTrigger: {
        trigger: pillarsSection,
        start: 'top 85%',
        end: 'top 20%', // Completes alignment early while section is in full view
        scrub: 0.5,
        invalidateOnRefresh: true
      }
    });

    // Animate the cards to y: 0 (aligning together seamlessly)
    pTl.to(pillars, {
      y: 0,
      ease: 'power1.out',
      force3D: true
    }, 0);

    // Inner Image Parallax (shifts images smoothly inside the cards for 3D depth)
    if (pillarImgs.length > 0) {
      pTl.fromTo(pillarImgs, {
        y: '-8%'
      }, {
        y: '8%',
        ease: 'power1.out',
        force3D: true
      }, 0);
    }
  }


  // ----------------------------------------------------
  // 10. REVEAL-ON-SCROLL INTERSECTION OBSERVER
  // ----------------------------------------------------
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-in');
      }
    });
  }, { threshold: 0.12 });

  revealElements.forEach(el => revealObserver.observe(el));

  // ----------------------------------------------------
  // 11. GLOBAL VIDEO AUTOPLAY & LAPTOP PERFORMANCE ENGINE
  // ----------------------------------------------------
  const allVideos = document.querySelectorAll('video');

  function initVideoPlayback(v) {
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    v.setAttribute('webkit-playsinline', '');

    // Handle low-end laptop GPU decode errors on WebM by forcing fallback
    const sources = v.querySelectorAll('source');
    sources.forEach(src => {
      src.onerror = () => {
        // If a WebM source fails to decode on low-end GPUs, force load next available fallback (e.g. MP4)
        if (src.type === 'video/webm' && sources.length > 1) {
          v.removeAttribute('src');
          v.load();
          v.play().catch(() => {});
        }
      };
    });

    if (v.paused) {
      const p = v.play();
      if (p !== undefined) {
        p.catch(() => {
          // Low-power mode, battery saver, or browser energy saver suspended playback
        });
      }
    }
  }

  function playAllVideos() {
    allVideos.forEach(v => initVideoPlayback(v));
  }

  playAllVideos();

  // Laptop & Mobile Wake Hooks (triggers on mouse movement, scroll, tab switch, or click)
  ['touchstart', 'touchmove', 'mousemove', 'pointermove', 'scroll', 'click', 'pointerdown', 'focus'].forEach(evt => {
    window.addEventListener(evt, playAllVideos, { passive: true });
  });

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) playAllVideos();
  });

  // ----------------------------------------------------
  // 12. MULTI-CURRENCY CONVERSION MANAGER
  // ----------------------------------------------------
  const currencySelect = document.getElementById('currency-select');
  const currencyRates = {
    INR: { rate: 1.0, symbol: '₹', prefix: true },
    USD: { rate: 0.01156, symbol: '$', prefix: true },
    EUR: { rate: 0.01109, symbol: '€', prefix: true },
    GBP: { rate: 0.00921, symbol: '£', prefix: true },
    AED: { rate: 0.04255, symbol: 'AED', prefix: false }
  };

  function formatCurrencyValue(inrValue, currencyCode) {
    const config = currencyRates[currencyCode] || currencyRates.INR;
    const converted = Math.round(inrValue * config.rate);
    const formattedNum = converted.toLocaleString('en-US');
    return config.prefix ? `${config.symbol}${formattedNum}` : `${formattedNum} ${config.symbol}`;
  }

  function applyGlobalCurrency(currencyCode) {
    const priceElements = document.querySelectorAll('.rentora-price[data-price-inr]');
    priceElements.forEach(el => {
      const rawInr = parseFloat(el.getAttribute('data-price-inr'));
      if (!isNaN(rawInr)) {
        el.textContent = formatCurrencyValue(rawInr, currencyCode);
      }
    });
    localStorage.setItem('rentora_currency', currencyCode);
    if (currencySelect) {
      currencySelect.value = currencyCode;
    }
  }

  const savedCurrency = localStorage.getItem('rentora_currency') || 'INR';
  applyGlobalCurrency(savedCurrency);

  if (currencySelect) {
    currencySelect.addEventListener('change', (e) => {
      applyGlobalCurrency(e.target.value);
    });
  }
});




