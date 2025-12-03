# Custom Login Template – Al-Mofeed HIS

This document explains the custom login template created for Al-Mofeed HIS and how the multi-language support is implemented.

## Template Location

```
mofeed_his/templates/pages/login.html
```

## Features Implemented

### 1. Username Field
- Field ID: `usr`
- Field name: `usr` (Frappe standard)
- Bilingual label: "Username / اسم المستخدم"
- Includes placeholder text with translation support
- Has `autocomplete="username"` for browser autofill

### 2. Password Field
- Field ID: `pwd`
- Field name: `pwd` (Frappe standard)
- Bilingual label: "Password / كلمة المرور"
- Password visibility toggle with eye icon
- Has `autocomplete="current-password"` for browser autofill

### 3. Language Selector (ar, en, ku)
The language selector is implemented as a `<select>` dropdown with three options:

```html
<select class="language-select" id="language" name="language">
    <option value="ar">العربية (Arabic)</option>
    <option value="en">English</option>
    <option value="ku">کوردی (Kurdish)</option>
</select>
```

The current language is pre-selected based on `frappe.local.lang`.

### 4. Login Button
- Bilingual text: "Login – تسجيل الدخول"
- Uses Frappe's translation function `_("Login")`
- Has loading spinner for AJAX submission
- Disables during form submission to prevent double-click

### 5. CSRF Token Usage
The CSRF token is included as a hidden field and sent in AJAX headers:

```html
<!-- Hidden field in form -->
<input type="hidden" name="csrf_token" value="{{ frappe.session.csrf_token }}">
```

```javascript
// Sent in AJAX header
headers: {
    'Content-Type': 'application/json',
    'X-Frappe-CSRF-Token': data.csrf_token
}
```

### 6. RTL Switch for Arabic
The RTL switching is handled by JavaScript that:
1. Detects the selected language on page load
2. Sets `dir="rtl"` on the body when Arabic is selected
3. Updates direction dynamically when language changes

```javascript
function updateDirection(lang) {
    const body = document.body;
    if (lang === 'ar') {
        body.setAttribute('dir', 'rtl');
    } else {
        body.setAttribute('dir', 'ltr');
    }
}
```

CSS rules handle the RTL layout:
```css
body.login-page[dir="rtl"] {
    font-family: 'Cairo', 'Noto Sans Arabic', 'Inter', sans-serif;
}

body.login-page[dir="rtl"] .login-card,
body.login-page[dir="rtl"] .form-group {
    direction: rtl;
    text-align: right;
}
```

---

## How Language Selection is Wired

### Client-Side Flow

1. **On Page Load:**
   - The template checks `frappe.local.lang` to pre-select the current language
   - `updateDirection()` is called to set initial RTL/LTR direction

2. **On Language Change:**
   - Event listener on `<select>` triggers `updateDirection()`
   - Language preference is stored in a cookie: `preferred_language`

3. **On Form Submit:**
   - Selected language is sent to the server with login credentials
   - After successful login, the user's language preference is updated

### Server-Side Flow (Frappe Integration)

1. **Login API:**
   - Form posts to `/api/method/login` (Frappe standard)
   - CSRF token is validated by Frappe

2. **Language Setting:**
   - After login, the JavaScript calls `/api/method/frappe.client.set_value`
   - This updates the User doctype's `language` field

3. **Session Language:**
   - Frappe reads the user's language preference on subsequent requests
   - All translations are applied based on `frappe.local.lang`

---

## Integration with Frappe

To use this custom login template, you need to:

### 1. Create the Website Settings override

In your app's `hooks.py`:

```python
# Override login page
website_route_rules = [
    {"from_route": "/login", "to_route": "login"},
]
```

### 2. Or use website_context

```python
# In hooks.py
website_context = {
    "login_url": "/custom-login"
}
```

### 3. Ensure translations are loaded

Add translation files for Arabic and Kurdish:
- `mofeed_his/translations/ar.csv`
- `mofeed_his/translations/ku.csv`

---

## Color Scheme

The template uses the Al-Mofeed healthcare color palette:

| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary Blue | `#0C82E6` | Buttons, focus states |
| Secondary Cyan | `#26C6DA` | Accents |
| Accent Green | `#4CAF50` | Success states |
| Background | `#F9FAFB` | Page background |
| Text | `#1F2937` | Primary text |

---

## Typography

- **Arabic:** Cairo, Noto Sans Arabic
- **English/Kurdish:** Inter, Roboto

---

## Accessibility

- All inputs have associated labels
- Password toggle has `aria-label`
- Focus states are clearly visible
- Keyboard navigation is supported

---

## Security Features

1. **CSRF Protection:** Token is validated on every form submission
2. **No password in URL:** Form uses POST method
3. **Secure cookie:** Language preference cookie is set with proper path
4. **Rate limiting:** Handled by Frappe's built-in login throttling
