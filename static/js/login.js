/* =========================================================
   login.js  –  Django Login Page Scripts
   Place at: yourapp/static/js/login.js
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. Password show / hide toggle ── */
  const toggleBtn     = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('id_password');
  const eyeIcon       = document.getElementById('eyeIcon');

  const EYE_OPEN = `
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>
  `;
  const EYE_CLOSED = `
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8
             a18.45 18.45 0 0 1 5.06-5.94"/>
    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8
             a18.5 18.5 0 0 1-2.16 3.19"/>
    <line x1="1" y1="1" x2="23" y2="23"/>
  `;

  if (toggleBtn && passwordInput) {
    toggleBtn.addEventListener('click', () => {
      const isHidden = passwordInput.type === 'password';
      passwordInput.type = isHidden ? 'text' : 'password';
      eyeIcon.innerHTML   = isHidden ? EYE_CLOSED : EYE_OPEN;
      toggleBtn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
    });
  }


  /* ── 2. Client-side validation ── */
  const form        = document.getElementById('loginForm');
  const usernameInput = document.getElementById('id_username');

  function showFieldError(input, message) {
    input.classList.add('input-error');
    let errEl = input.closest('.field-group').querySelector('.field-error');
    if (!errEl) {
      errEl = document.createElement('span');
      errEl.className = 'field-error';
      input.closest('.input-wrap').after(errEl);
    }
    errEl.textContent = message;
  }

  function clearFieldError(input) {
    input.classList.remove('input-error');
    const errEl = input.closest('.field-group').querySelector('.field-error');
    if (errEl) errEl.textContent = '';
  }

  // Clear errors on input
  [usernameInput, passwordInput].forEach(input => {
    if (!input) return;
    input.addEventListener('input', () => clearFieldError(input));
  });

  if (form) {
    form.addEventListener('submit', (e) => {
      let valid = true;

      // Validate username
      if (usernameInput && !usernameInput.value.trim()) {
        showFieldError(usernameInput, 'Please enter your username or email.');
        valid = false;
      }

      // Validate password
      if (passwordInput && !passwordInput.value) {
        showFieldError(passwordInput, 'Please enter your password.');
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
        return;
      }

      // Show loading state
      setLoadingState(true);
    });
  }


  /* ── 3. Submit button loading state ── */
  const submitBtn  = document.getElementById('submitBtn');
  const btnText    = submitBtn  ? submitBtn.querySelector('.btn-text')    : null;
  const btnSpinner = document.getElementById('btnSpinner');

  function setLoadingState(loading) {
    if (!submitBtn) return;
    submitBtn.disabled = loading;
    if (btnText)    btnText.textContent = loading ? 'Signing in…' : 'Sign In';
    if (btnSpinner) btnSpinner.hidden   = !loading;
  }

  // Safety: reset button if page is restored from bfcache (back/forward)
  window.addEventListener('pageshow', (e) => {
    if (e.persisted) setLoadingState(false);
  });


  /* ── 4. Auto-focus first empty field ── */
  if (usernameInput && !usernameInput.value) {
    usernameInput.focus();
  } else if (passwordInput) {
    passwordInput.focus();
  }


  /* ── 5. Custom checkbox visual sync ── */
  const rememberCheckbox = document.getElementById('rememberMe');
  if (rememberCheckbox) {
    // Sync on keyboard Enter/Space (accessibility)
    rememberCheckbox.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        rememberCheckbox.checked = !rememberCheckbox.checked;
      }
    });
  }


  /* ── 6. Dismiss Django messages on click ── */
  document.querySelectorAll('.alert').forEach(alert => {
    alert.style.cursor = 'pointer';
    alert.setAttribute('title', 'Click to dismiss');
    alert.addEventListener('click', () => {
      alert.style.transition = 'opacity 0.3s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    });
  });

});