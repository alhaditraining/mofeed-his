/**
 * Al-Mofeed HIS - Custom Login Page JavaScript
 * 
 * Handles:
 * - Language switching with RTL/LTR toggle
 * - Password visibility toggle
 * - Form submission via AJAX
 * - Error handling and display
 * - Session language persistence
 */

(function() {
  'use strict';

  // DOM Elements
  const loginWrapper = document.getElementById('mofeed-login-wrapper');
  const loginForm = document.getElementById('mofeed-login-form');
  const languageSelect = document.getElementById('language_select');
  const passwordInput = document.getElementById('login_password');
  const togglePasswordBtn = document.getElementById('toggle-password');
  const togglePasswordIcon = document.getElementById('toggle-password-icon');
  const loginBtn = document.getElementById('mofeed-login-btn');
  const errorContainer = document.getElementById('login-error');

  /**
   * Initialize the login page
   */
  function init() {
    if (!loginForm) return;

    // Set initial language direction
    updateLanguageDirection(languageSelect?.value || 'en');

    // Event listeners
    if (languageSelect) {
      languageSelect.addEventListener('change', handleLanguageChange);
    }

    if (togglePasswordBtn) {
      togglePasswordBtn.addEventListener('click', togglePasswordVisibility);
    }

    loginForm.addEventListener('submit', handleFormSubmit);

    // Focus on username field
    const usernameInput = document.getElementById('login_email');
    if (usernameInput) {
      usernameInput.focus();
    }
  }

  /**
   * Handle language selection change
   * @param {Event} event - Change event
   */
  function handleLanguageChange(event) {
    const selectedLang = event.target.value;
    updateLanguageDirection(selectedLang);
    
    // Store language preference in session storage for persistence
    try {
      sessionStorage.setItem('mofeed_login_lang', selectedLang);
    } catch (e) {
      // Session storage might be disabled
      console.warn('Could not save language preference:', e);
    }
  }

  /**
   * Update page direction based on language
   * @param {string} lang - Language code (ar, en, ku)
   */
  function updateLanguageDirection(lang) {
    if (!loginWrapper) return;

    // Arabic and Kurdish use RTL
    const isRTL = lang === 'ar' || lang === 'ku';
    loginWrapper.setAttribute('dir', isRTL ? 'rtl' : 'ltr');
    
    // Update document direction for full page effect
    document.documentElement.setAttribute('dir', isRTL ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
  }

  /**
   * Toggle password field visibility
   */
  function togglePasswordVisibility() {
    if (!passwordInput || !togglePasswordIcon) return;

    const isPassword = passwordInput.type === 'password';
    passwordInput.type = isPassword ? 'text' : 'password';
    
    // Update icon
    togglePasswordIcon.classList.remove('fa-eye', 'fa-eye-slash');
    togglePasswordIcon.classList.add(isPassword ? 'fa-eye-slash' : 'fa-eye');
  }

  /**
   * Handle form submission
   * @param {Event} event - Submit event
   */
  function handleFormSubmit(event) {
    event.preventDefault();

    // Clear previous errors
    hideError();

    // Get form data
    const formData = new FormData(loginForm);
    const username = formData.get('usr');
    const password = formData.get('pwd');
    const language = formData.get('language');

    // Basic validation
    if (!username || !password) {
      showError(getTranslatedMessage('please_fill_fields', language));
      return;
    }

    // Show loading state
    setLoadingState(true);

    // Perform login via Frappe API
    performLogin(username, password, language);
  }

  /**
   * Perform login via Frappe API
   * @param {string} username - Username or email
   * @param {string} password - Password
   * @param {string} language - Selected language
   */
  function performLogin(username, password, language) {
    // Use Frappe's login API
    const loginData = {
      usr: username,
      pwd: password
    };

    fetch('/api/method/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'X-Frappe-CSRF-Token': getCsrfToken()
      },
      body: new URLSearchParams(loginData)
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.message || data._server_messages || 'Login failed');
        });
      }
      return response.json();
    })
    .then(data => {
      // Set language preference after successful login
      setUserLanguage(language);
      
      // Redirect to desk or home
      const redirectUrl = getRedirectUrl();
      window.location.href = redirectUrl;
    })
    .catch(error => {
      setLoadingState(false);
      const errorMessage = parseErrorMessage(error.message, language);
      showError(errorMessage);
    });
  }

  /**
   * Set user language preference after login
   * @param {string} language - Language code
   */
  function setUserLanguage(language) {
    // Try to set the language via Frappe API
    // This will be applied on the next page load
    try {
      fetch('/api/method/frappe.client.set_value', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-Frappe-CSRF-Token': getCsrfToken()
        },
        body: JSON.stringify({
          doctype: 'User',
          name: frappe?.session?.user || '',
          fieldname: 'language',
          value: language
        })
      }).catch(() => {
        // Silent fail - language will use system default
      });
    } catch (e) {
      // Silent fail
    }
  }

  /**
   * Get CSRF token from meta tag or cookie
   * @returns {string} CSRF token
   */
  function getCsrfToken() {
    // Try to get from meta tag first
    const metaTag = document.querySelector('meta[name="csrf_token"]');
    if (metaTag) {
      return metaTag.getAttribute('content');
    }
    
    // Try to get from frappe object
    if (typeof frappe !== 'undefined' && frappe.csrf_token) {
      return frappe.csrf_token;
    }

    // Fallback - try to get from cookie
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrf_token') {
        return decodeURIComponent(value);
      }
    }

    return '';
  }

  /**
   * Get redirect URL after login
   * @returns {string} Redirect URL
   */
  function getRedirectUrl() {
    // Check for redirect parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    const redirect = urlParams.get('redirect-to');
    
    if (redirect && !redirect.includes('login')) {
      return redirect;
    }
    
    // Default to desk
    return '/app';
  }

  /**
   * Parse error message from server response
   * @param {string} message - Error message
   * @param {string} language - Current language
   * @returns {string} Parsed error message
   */
  function parseErrorMessage(message, language) {
    // Try to parse server messages
    try {
      if (message.startsWith('[')) {
        const parsed = JSON.parse(message);
        if (Array.isArray(parsed) && parsed.length > 0) {
          const serverMsg = JSON.parse(parsed[0]);
          return serverMsg.message || message;
        }
      }
    } catch (e) {
      // Use original message
    }

    // Check for common error messages
    if (message.includes('Incorrect password') || message.includes('Invalid login')) {
      return getTranslatedMessage('invalid_credentials', language);
    }

    if (message.includes('User disabled') || message.includes('not allowed')) {
      return getTranslatedMessage('user_disabled', language);
    }

    return message;
  }

  /**
   * Get translated message based on language
   * @param {string} key - Message key
   * @param {string} language - Language code
   * @returns {string} Translated message
   */
  function getTranslatedMessage(key, language) {
    // NOTE: Kurdish (ku) translations use Sorani Kurdish (Central Kurdish).
    // These are placeholder translations and should be verified by a native speaker.
    const messages = {
      please_fill_fields: {
        ar: 'يرجى ملء جميع الحقول المطلوبة',
        en: 'Please fill in all required fields',
        ku: 'تکایە هەموو بوارە پێویستەکان پڕبکەوە'
      },
      invalid_credentials: {
        ar: 'اسم المستخدم أو كلمة المرور غير صحيحة',
        en: 'Invalid username or password',
        ku: 'ناوی بەکارهێنەر یان وشەی نهێنی هەڵەیە'
      },
      user_disabled: {
        ar: 'حساب المستخدم معطل',
        en: 'User account is disabled',
        ku: 'ئەکاونتی بەکارهێنەر لەکارخراوە'
      },
      login_error: {
        ar: 'حدث خطأ أثناء تسجيل الدخول',
        en: 'An error occurred during login',
        ku: 'هەڵەیەک ڕوویدا لە کاتی چوونەژوورەوە'
      }
    };

    const msgObj = messages[key];
    if (!msgObj) return key;

    return msgObj[language] || msgObj.en;
  }

  /**
   * Show error message
   * @param {string} message - Error message to display
   */
  function showError(message) {
    if (!errorContainer) return;

    errorContainer.textContent = message;
    errorContainer.style.display = 'block';
    
    // Scroll error into view
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  /**
   * Hide error message
   */
  function hideError() {
    if (!errorContainer) return;

    errorContainer.textContent = '';
    errorContainer.style.display = 'none';
  }

  /**
   * Set loading state on login button
   * @param {boolean} isLoading - Loading state
   */
  function setLoadingState(isLoading) {
    if (!loginBtn) return;

    loginBtn.disabled = isLoading;
    loginBtn.classList.toggle('loading', isLoading);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
