document.addEventListener('DOMContentLoaded', () => {
  // Register GSAP Plugins
  gsap.registerPlugin(ScrollTrigger);

  // Global Lenis Smooth Scroll Initialization
  if (typeof Lenis !== 'undefined') {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1.0,
      touchMultiplier: 1.5,
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
        nightBtn.className = "px-2.5 py-1 text-[0.65rem] uppercase tracking-widest rounded-full transition-all duration-300 bg-white text-[#181614] font-semibold shadow-sm";
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
        dayBtn.className = "px-2.5 py-1 text-[0.65rem] uppercase tracking-widest rounded-full transition-all duration-300 bg-[#181614] text-white font-semibold shadow-sm";
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
        t.classList.remove('bg-[var(--ink)]', 'text-white', 'shadow-md', 'active');
        t.classList.add('text-[var(--ink)]/70');
      });

      tab.classList.add('bg-[var(--ink)]', 'text-white', 'shadow-md', 'active');
      tab.classList.remove('text-[var(--ink)]/70');

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
        tabLogin.classList.add('bg-white', 'text-[#181614]', 'shadow-md');
        tabLogin.classList.remove('text-white/70');
      }
      if (tabSignup) {
        tabSignup.classList.remove('bg-white', 'text-[#181614]', 'shadow-md');
        tabSignup.classList.add('text-white/70');
      }
    } else {
      if (signupForm) signupForm.classList.remove('hidden');
      if (loginForm) loginForm.classList.add('hidden');
      if (tabSignup) {
        tabSignup.classList.add('bg-white', 'text-[#181614]', 'shadow-md');
        tabSignup.classList.remove('text-white/70');
      }
      if (tabLogin) {
        tabLogin.classList.remove('bg-white', 'text-[#181614]', 'shadow-md');
        tabLogin.classList.add('text-white/70');
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
        inlineTabLogin.classList.add('bg-white', 'text-[#181614]', 'shadow-md');
        inlineTabLogin.classList.remove('text-white/70');
      }
      if (inlineTabSignup) {
        inlineTabSignup.classList.remove('bg-white', 'text-[#181614]', 'shadow-md');
        inlineTabSignup.classList.add('text-white/70');
      }
    } else {
      if (inlineSignupForm) inlineSignupForm.classList.remove('hidden');
      if (inlineLoginForm) inlineLoginForm.classList.add('hidden');
      if (inlineTabSignup) {
        inlineTabSignup.classList.add('bg-white', 'text-[#181614]', 'shadow-md');
        inlineTabSignup.classList.remove('text-white/70');
      }
      if (inlineTabLogin) {
        inlineTabLogin.classList.remove('bg-white', 'text-[#181614]', 'shadow-md');
        inlineTabLogin.classList.add('text-white/70');
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
  const loaderPlayed = sessionStorage.getItem('rentora_loader_played');
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

  if (loaderEl && (loaderPlayed || hasMessagesOrForm)) {
    loaderEl.style.display = 'none';
    loaderEl.style.pointerEvents = 'none';
    playHeroEntrance();
    setTimeout(() => {
      if (typeof ScrollTrigger !== 'undefined') {
        ScrollTrigger.refresh();
      }
    }, 100);
  } else if (loaderEl) {
    sessionStorage.setItem('rentora_loader_played', 'true');

    const loaderBox = document.querySelector('.hero-loader__box');
    const growingImgBox = document.querySelector('.hero-loader__growing-image');
    const loaderStartWord = document.querySelector('.hero-loader__word--start');
    const loaderEndWord = document.querySelector('.hero-loader__word--end');
    const loaderSlides = Array.from(document.querySelectorAll('.loader-img-slide'));
    
    // Preload loader images immediately for 0ms lag-free GPU rendering
    const preloadUrls = [
      'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1200&q=80',
      'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=1200&q=80',
      'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80',
      'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=2000&q=85'
    ];
    preloadUrls.forEach(url => {
      const img = new Image();
      img.src = url;
    });

    const isMobile = window.innerWidth < 640;
    const targetWidth = isMobile ? '76px' : '150px';

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

  // Smooth Crossfade to Slide 1 (Munnar Highlands)
  if (loaderSlides[1]) {
    introTl.to(loaderSlides[0], {
      opacity: 0,
      duration: 0.5,
      ease: 'power2.inOut'
    }, '+=0.05')
    .to(loaderSlides[1], {
      opacity: 1,
      scale: 1.0,
      duration: 0.75,
      ease: 'power1.out'
    }, '<');
  }

  // Smooth Crossfade to Slide 2 (Kerala Coast)
  if (loaderSlides[2]) {
    introTl.to(loaderSlides[1], {
      opacity: 0,
      duration: 0.5,
      ease: 'power2.inOut'
    }, '+=0.05')
    .to(loaderSlides[2], {
      opacity: 1,
      scale: 1.0,
      duration: 0.75,
      ease: 'power1.out'
    }, '<');
  }

  // Smooth Crossfade to Final Slide 3 (Matches Hero Slide 1)
  if (loaderSlides[3]) {
    introTl.to(loaderSlides[2], {
      opacity: 0,
      duration: 0.5,
      ease: 'power2.inOut'
    }, '+=0.05')
    .to(loaderSlides[3], {
      opacity: 1,
      scale: 1.0,
      duration: 0.75,
      ease: 'power1.out'
    }, '<');
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

      // 2. Multi-Plane Botanical Canopy Parallax
      hTl.to('.top-left-canopy', {
        x: -60,
        ease: 'none',
        duration: 3,
        force3D: true,
        autoRound: false
      }, 0);

      // 3. Ground Bush Multi-Plane Float
      hTl.to('.panel-ground-bush', {
        x: -150,
        ease: 'none',
        duration: 3,
        force3D: true,
        autoRound: false
      }, 0);

      // 4. Slide 2 Image Parallax
      hTl.fromTo('.panel-2-image img', 
        { scale: 1.08 },
        {
          scale: 1.0,
          ease: 'none',
          duration: 3,
          force3D: true
        }, 0
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
  // 11. GLOBAL VIDEO AUTOPLAY & LOOP ENFORCER
  // ----------------------------------------------------
  const allVideos = document.querySelectorAll('video');
  function playAllVideos() {
    allVideos.forEach(v => {
      if (v.paused) {
        v.play().catch(() => {});
      }
    });
  }
  playAllVideos();
  window.addEventListener('scroll', playAllVideos, { passive: true });
  document.addEventListener('click', playAllVideos, { once: true });

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




