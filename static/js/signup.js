/* =========================================================
   signup.js  –  Social AI Signup Page Scripts
   Place at: social_ai/static/js/signup.js
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ──────────────────────────────────────────
      1. Password show / hide toggles
  ────────────────────────────────────────── */
  const EYE_OPEN = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>`;
  const EYE_CLOSED = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8
    a18.45 18.45 0 0 1 5.06-5.94"/>
    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8
    a18.5 18.5 0 0 1-2.16 3.19"/>
    <line x1="1" y1="1" x2="23" y2="23"/>`;

  function setupToggle(btnId, inputId, iconId) {
    const btn   = document.getElementById(btnId);
    const input = document.getElementById(inputId);
    const icon  = document.getElementById(iconId);
    if (!btn || !input) return;

    btn.addEventListener('click', () => {
      const hidden = input.type === 'password';
      input.type    = hidden ? 'text' : 'password';
      icon.innerHTML = hidden ? EYE_CLOSED : EYE_OPEN;
      btn.setAttribute('aria-label', hidden ? 'Hide password' : 'Show password');
    });
  }

  setupToggle('togglePw1', 'id_password1', 'eyeIcon1');
  setupToggle('togglePw2', 'id_password2', 'eyeIcon2');


  /* ──────────────────────────────────────────
      2. Password strength meter
  ────────────────────────────────────────── */
  const pw1Input      = document.getElementById('id_password1');
  const strengthFill  = document.getElementById('strengthFill');
  const strengthLabel = document.getElementById('strengthLabel');

  const STRENGTHS = [
    { label: '',         color: 'transparent', pct: 0  },
    { label: 'Weak',     color: '#ef4444',     pct: 25 },
    { label: 'Fair',     color: '#f59e0b',     pct: 50 },
    { label: 'Good',     color: '#3b82f6',     pct: 75 },
    { label: 'Strong',   color: '#22c55e',     pct: 100},
  ];

  function scorePassword(pw) {
    if (!pw) return 0;
    let score = 0;
    if (pw.length >= 8)  score++;
    if (pw.length >= 12) score++;
    if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++;
    if (/\d/.test(pw))   score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;
    return Math.min(4, score);
  }

  if (pw1Input && strengthFill && strengthLabel) {
    pw1Input.addEventListener('input', () => {
      const level = scorePassword(pw1Input.value);
      const s = STRENGTHS[level];
      strengthFill.style.width           = s.pct + '%';
      strengthFill.style.backgroundColor = s.color;
      strengthLabel.textContent          = s.label;
      strengthLabel.style.color          = s.color;
    });
  }


  /* ──────────────────────────────────────────
      3. Confirm password match check
  ────────────────────────────────────────── */
  const pw2Input    = document.getElementById('id_password2');
  const pwMatchErr  = document.getElementById('pwMatchError');

  function checkMatch() {
    if (!pw2Input.value) { pwMatchErr.textContent = ''; return true; }
    const match = pw1Input.value === pw2Input.value;
    pwMatchErr.textContent = match ? '' : 'Passwords do not match.';
    pw2Input.classList.toggle('input-error', !match);
    pw2Input.classList.toggle('input-valid',  match);
    return match;
  }

  if (pw2Input) {
    pw2Input.addEventListener('input', checkMatch);
    pw1Input && pw1Input.addEventListener('input', () => {
      if (pw2Input.value) checkMatch();
    });
  }


  /* ──────────────────────────────────────────
      4. Email availability check (debounced)
  ────────────────────────────────────────── */
  const emailInput = document.getElementById('id_email');
  const emailStatus = document.getElementById('emailStatus');
  const usernameInput = document.getElementById('id_username'); // Fixed: Added back definition so validation won't crash
  let emailTimer = null;

  async function checkEmail(value) {
    if (!value || !value.includes('@')) {
      if (emailStatus) emailStatus.textContent = '';
      return;
    }

    if (emailStatus) emailStatus.textContent = '⏳';

    try {
      // Adjusted endpoint address to match what your routing expects
      const res = await fetch(`/check-email/?email=${encodeURIComponent(value)}`);
      const data = await res.json();

      // Fixed: Match Django view return scheme (data.exists is false means it's available)
      if (!data.exists) {
        if (emailStatus) emailStatus.textContent = '✅';
        emailInput.classList.remove('input-error');
        emailInput.classList.add('input-valid');
      } else {
        if (emailStatus) emailStatus.textContent = '❌ Email already exists';
        emailInput.classList.add('input-error');
        emailInput.classList.remove('input-valid');
      }
    } catch (error) {
      console.error(error);
      if (emailStatus) emailStatus.textContent = '';
    }
  }

  if (emailInput) {
    emailInput.addEventListener('input', () => {
      clearTimeout(emailTimer);
      emailTimer = setTimeout(() => {
        checkEmail(emailInput.value.trim());
      }, 500);
    });
  }


  /* ──────────────────────────────────────────
      5. Client-side form validation on submit
  ────────────────────────────────────────── */
  const form      = document.getElementById('signupForm');
  const submitBtn = document.getElementById('submitBtn');
  const btnText   = submitBtn?.querySelector('.btn-text');
  const spinner   = document.getElementById('btnSpinner');
  const termsCheck = document.getElementById('termsCheck');
  const termsError = document.getElementById('termsError');

  function showFieldError(input, msg) {
    input.classList.add('input-error');
    const group = input.closest('.field-group');
    let err = group?.querySelector('.field-error');
    if (!err) {
      err = document.createElement('span');
      err.className = 'field-error';
      input.closest('.input-wrap')?.after(err);
    }
    err.textContent = msg;
  }

  function clearFieldError(input) {
    input.classList.remove('input-error');
    const group = input.closest('.field-group');
    const err = group?.querySelector('.field-error');
    if (err) err.textContent = '';
  }

  // Clear on input
  [usernameInput, emailInput, pw1Input, pw2Input].forEach(el => {
    el?.addEventListener('input', () => clearFieldError(el));
  });

  if (form) {
    form.addEventListener('submit', (e) => {
      let valid = true;

      if (usernameInput && !usernameInput.value.trim()) {
        showFieldError(usernameInput, 'Username is required.');
        valid = false;
      }

      if (emailInput && !emailInput.value.trim()) {
        showFieldError(emailInput, 'Email is required.');
        valid = false;
      } else if (emailInput && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
        showFieldError(emailInput, 'Enter a valid email address.');
        valid = false;
      }

      if (pw1Input && !pw1Input.value) {
        showFieldError(pw1Input, 'Password is required.');
        valid = false;
      }

      if (pw2Input && !pw2Input.value) {
        showFieldError(pw2Input, 'Please confirm your password.');
        valid = false;
      } else if (!checkMatch()) {
        valid = false;
      }

      if (termsCheck && !termsCheck.checked) {
        if (termsError) termsError.textContent = 'You must accept the terms to continue.';
        valid = false;
      } else if (termsError) {
        termsError.textContent = '';
      }

      if (!valid) { e.preventDefault(); return; }

      // Loading state
      if (submitBtn) submitBtn.disabled = true;
      if (btnText)   btnText.textContent = 'Creating account…';
      if (spinner)   spinner.hidden = false;
    });
  }

  // Reset on bfcache restore
  window.addEventListener('pageshow', (e) => {
    if (e.persisted) {
      if (submitBtn) submitBtn.disabled = false;
      if (btnText)   btnText.textContent = 'Create Account';
      if (spinner)   spinner.hidden = true;
    }
  });


  /* ──────────────────────────────────────────
      6. Dismiss Django messages on click
  ────────────────────────────────────────── */
  document.querySelectorAll('.alert').forEach(alert => {
    alert.addEventListener('click', () => {
      alert.style.transition = 'opacity 0.3s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    });
  });


  /* ──────────────────────────────────────────
      7. Auto-focus first empty field
  ────────────────────────────────────────── */
  const firstEmpty = document.querySelector(
    '#id_first_name, #id_last_name, #id_username, #id_email'
  );
  firstEmpty?.focus();

});