/* ═══════════════════════════════════════════════════
   Social AI — dashboard.js
   ═══════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Mobile sidebar ────────────────────────────── */
  const sidebar = document.getElementById('sidebar');
  const hamburger = document.getElementById('hamburger');
  const overlay = document.getElementById('overlay');

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('visible');
    document.body.style.overflow = '';
  }

  if (hamburger) hamburger.addEventListener('click', openSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  /* close sidebar on nav link click (mobile) */
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) closeSidebar();
    });
  });

  /* ── Account dropdown ──────────────────────────── */
  const trigger = document.getElementById('adTrigger');
  const menu = document.getElementById('adMenu');

  if (trigger && menu) {
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = !menu.hidden;
      menu.hidden = isOpen;
      trigger.classList.toggle('open', !isOpen);
    });

    document.querySelectorAll('.ad-opt').forEach(opt => {
      opt.addEventListener('click', () => {
        const label = trigger.querySelector('.ad-label');
        if (label) label.textContent = opt.textContent.trim();
        document.querySelectorAll('.ad-opt').forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        menu.hidden = true;
        trigger.classList.remove('open');
        // You can emit a custom event here so Django/HTMX can filter posts
        trigger.dispatchEvent(new CustomEvent('accountChange', {
          detail: { value: opt.dataset.val },
          bubbles: true
        }));
      });
    });

    /* close on outside click */
    document.addEventListener('click', (e) => {
      const dropdown = document.getElementById('acctDropdown');
      if (dropdown && !dropdown.contains(e.target)) {
        menu.hidden = true;
        trigger.classList.remove('open');
      }
    });
  }

  /* ── Dot menu (3-dot context) ──────────────────── */
  document.querySelectorAll('.dot-menu').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      // Placeholder: hook up a real context menu or modal here
      console.log('[Social AI] Post options clicked', btn.closest('.sched-row'));
    });
  });

  /* ── Stat counter animation ────────────────────── */
  function animateCount(el, target, suffix) {
    const duration = 900;
    const start = performance.now();
    const from = 0;

    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
      const current = Math.round(from + (target - from) * eased);
      el.textContent = current.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* parse values like "48", "2.4K", "5.6K" */
  function parseStatVal(text) {
    text = text.trim();
    if (text.endsWith('K')) return { val: parseFloat(text) * 1000, suffix: 'K', raw: parseFloat(text) };
    return { val: parseInt(text, 10), suffix: '', raw: parseInt(text, 10) };
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const orig = el.dataset.orig || el.textContent;
      el.dataset.orig = orig;

      if (orig.includes('K')) {
        const num = parseFloat(orig);
        animateCount(el, num * 10, 'K'); // animate in tenths → display as #.#K
        // Re-implement for K values
        const duration = 900;
        const start = performance.now();
        function stepK(now) {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const current = (num * eased).toFixed(1);
          el.textContent = current + 'K';
          if (progress < 1) requestAnimationFrame(stepK);
        }
        requestAnimationFrame(stepK);
      } else {
        const num = parseInt(orig, 10);
        if (!isNaN(num)) animateCount(el, num, '');
      }

      observer.unobserve(el);
    });
  }, { threshold: 0.4 });

  document.querySelectorAll('.stat-val').forEach(el => observer.observe(el));

  /* ── Notification bell badge ───────────────────── */
  const notifBtn = document.querySelector('.icon-btn[aria-label="Notifications"]');
  if (notifBtn) {
    notifBtn.addEventListener('click', () => {
      const pip = notifBtn.querySelector('.notif-pip');
      if (pip) pip.style.display = 'none';
    });
  }

  /* ── Connect buttons → connections page ─────────── */
  document.querySelectorAll('.btn-connect').forEach(btn => {
    btn.addEventListener('click', (e) => {
      // href handles navigation; this adds a visual pulse before navigate
      btn.style.transform = 'scale(0.96)';
      setTimeout(() => { btn.style.transform = ''; }, 120);
    });
  });

  /* ── Dashboard Connected Accounts logic ─────────── */
  const dashDataEls = document.querySelectorAll('#dash-connected-accounts-data .acct-data');
  const dashConnectedMap = {};
  dashDataEls.forEach(el => {
      dashConnectedMap[el.getAttribute('data-platform')] = el.getAttribute('data-name');
  });

  document.querySelectorAll('#dash-conn-grid .conn-acct-card').forEach(card => {
      const plat = card.getAttribute('data-plat');
      if(dashConnectedMap[plat]) {
          card.querySelector('.state-conn').style.display = 'inline-flex';
          card.querySelector('.state-not-conn').style.display = 'none';
          card.querySelector('.acct-name').textContent = dashConnectedMap[plat];
      } else {
          card.querySelector('.state-conn').style.display = 'none';
          card.querySelector('.state-not-conn').style.display = 'inline-flex';
          card.querySelector('.acct-name').textContent = '-';
      }
  });

})();