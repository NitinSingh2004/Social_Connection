/**
 * Social AI — Sidebar Controller
 * Include at the bottom of your base template (before </body>)
 * or load via {% static 'js/sidebar.js' %}
 */

(function () {
  'use strict';

  // ── Storage key ────────────────────────────────────────────────
  const STORAGE_KEY = 'socialai_sidebar_collapsed';

  // ── Element references ──────────────────────────────────────────
  const sidebar       = document.getElementById('sidebar');
  const overlay       = document.getElementById('sidebarOverlay');
  const toggleBtn     = document.getElementById('sidebarToggle');
  const userMenuBtn   = document.getElementById('userMenuToggle');
  const userDropdown  = document.getElementById('userDropdown');

  // Mobile hamburger (placed in topbar, optional)
  const mobileToggle  = document.getElementById('sidebarMobileToggle');

  if (!sidebar) return; // Guard: sidebar not present on this page

  // ── Helpers ──────────────────────────────────────────────────────
  function isCollapsed()  { return localStorage.getItem(STORAGE_KEY) === 'true'; }
  function isMobile()     { return window.innerWidth <= 768; }

  function setBodyClass() {
    if (isMobile()) {
      document.body.classList.remove('sidebar-open', 'sidebar-collapsed');
      return;
    }
    if (isCollapsed()) {
      document.body.classList.add('sidebar-collapsed');
      document.body.classList.remove('sidebar-open');
    } else {
      document.body.classList.add('sidebar-open');
      document.body.classList.remove('sidebar-collapsed');
    }
  }

  // ── Collapse / Expand ────────────────────────────────────────────
  function collapse() {
    sidebar.classList.add('collapsed');
    localStorage.setItem(STORAGE_KEY, 'true');
    setBodyClass();
  }

  function expand() {
    sidebar.classList.remove('collapsed');
    localStorage.setItem(STORAGE_KEY, 'false');
    setBodyClass();
  }

  function toggleCollapse() {
    isCollapsed() ? expand() : collapse();
  }

  // ── Mobile open / close ──────────────────────────────────────────
  function openMobile() {
    sidebar.classList.add('mobile-open');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobile() {
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  function toggleMobile() {
    sidebar.classList.contains('mobile-open') ? closeMobile() : openMobile();
  }

  // ── User dropdown ────────────────────────────────────────────────
  function openDropdown() {
    userDropdown.classList.add('open');
    userMenuBtn.classList.add('open');
    userMenuBtn.setAttribute('aria-expanded', 'true');
  }

  function closeDropdown() {
    userDropdown.classList.remove('open');
    userMenuBtn.classList.remove('open');
    userMenuBtn.setAttribute('aria-expanded', 'false');
  }

  function toggleDropdown(e) {
    e.stopPropagation();
    userDropdown.classList.contains('open') ? closeDropdown() : openDropdown();
  }

  // ── Init ─────────────────────────────────────────────────────────
  function init() {
    // Restore collapsed state on desktop
    if (!isMobile() && isCollapsed()) {
      sidebar.classList.add('collapsed');
    }
    setBodyClass();

    // Desktop collapse toggle
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        toggleCollapse();
      });
    }

    // Mobile hamburger toggle
    if (mobileToggle) {
      mobileToggle.addEventListener('click', toggleMobile);
    }

    // Overlay click closes mobile sidebar
    if (overlay) {
      overlay.addEventListener('click', closeMobile);
    }

    // User dropdown toggle
    if (userMenuBtn && userDropdown) {
      // Clicking anywhere in the user row toggles it
      userMenuBtn.addEventListener('click', toggleDropdown);
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (userDropdown && !userDropdown.contains(e.target) && e.target !== userMenuBtn) {
        closeDropdown();
      }
    });

    // Close mobile sidebar on nav link click (single-page feel)
    const navLinks = sidebar.querySelectorAll('.sidebar-nav-link');
    navLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        if (isMobile()) closeMobile();
      });
    });

    // Handle resize: collapse overlay if screen grows
    let resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (!isMobile()) {
          closeMobile();
          setBodyClass();
        } else {
          document.body.classList.remove('sidebar-open', 'sidebar-collapsed');
        }
      }, 120);
    });
  }

  // Run after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();