# Login Language Handler – Technical Documentation

This document explains the Python controller/handler in the Frappe Framework that processes the login form and applies the selected language to:

1. `frappe.local.lang` (session language)
2. The User's `language` field (also known as "preferred language") if login succeeds

---

## Overview

In Frappe/ERPNext, the login process is handled by a combination of:

- **Frontend JavaScript**: `frappe/public/js/frappe/request.js` and login page JS
- **Backend Python API**: `frappe.auth` module
- **Whitelisted functions**: Exposed via `@frappe.whitelist(allow_guest=True)`

The key files involved are:

| File | Purpose |
|------|---------|
| `frappe/auth.py` | Main authentication logic |
| `frappe/handler.py` | Whitelisted API endpoint handler |
| `frappe/core/doctype/user/user.py` | User doctype with `preferred_language` field |
| `frappe/translate.py` | Translation and language utilities |

---

## Step-by-Step Login Flow

### Step 1: Frontend Submits Login Request

When the user submits the login form with:
- Username
- Password
- Selected language (e.g., `ar`, `en`, `ku`)

The frontend makes a POST request to `/api/method/login` with:

```javascript
frappe.call({
    method: 'login',
    args: {
        usr: username,
        pwd: password
    },
    // Language is typically sent via cookie or header
});
```

If a language selector is present on the login page, the selected language is often stored in:
- A cookie (`frappe.request.cookies.get('preferred_language')`)
- Or passed as a parameter

---

### Step 2: `frappe.handler.handle()` Receives Request

The request hits Frappe's main handler in `frappe/handler.py`:

```python
# frappe/handler.py

@frappe.whitelist(allow_guest=True)
def login():
    """Authenticate the user."""
    from frappe.auth import LoginManager
    
    # Get credentials from request
    usr = frappe.form_dict.get('usr')
    pwd = frappe.form_dict.get('pwd')
    
    # Create login manager and attempt login
    login_manager = LoginManager()
    login_manager.authenticate(usr, pwd)
    login_manager.post_login()
    
    # Return success response
    return frappe.auth.get_logged_user()
```

---

### Step 3: `LoginManager.authenticate()` Validates Credentials

In `frappe/auth.py`, the `LoginManager` class handles authentication:

```python
# frappe/auth.py

class LoginManager:
    def __init__(self):
        self.user = None
        self.info = None
        
    def authenticate(self, user=None, pwd=None):
        """Validate user credentials."""
        if not user:
            user = frappe.form_dict.get('usr')
        if not pwd:
            pwd = frappe.form_dict.get('pwd')
            
        # Validate credentials
        self.check_if_enabled(user)
        self.user = self.check_password(user, pwd)
```

---

### Step 4: `post_login()` Sets Session and Language

After successful authentication, `post_login()` is called:

```python
# frappe/auth.py

class LoginManager:
    def post_login(self):
        """Called after successful login."""
        self.run_trigger('on_login')
        self.validate_ip_address()
        self.validate_hour()
        
        # Set session user
        frappe.local.login_manager = self
        frappe.session.user = self.user
        
        # Set language from user preferences
        self.set_user_language()
        
        # Update user's last login
        self.update_user_login_info()
```

---

### Step 5: `set_user_language()` Applies Language

This is the **key function** that applies the selected language:

```python
# frappe/auth.py

class LoginManager:
    def set_user_language(self):
        """Set language for the session based on user preference or request."""
        
        # Priority 1: Check if language is passed in the request
        lang = frappe.form_dict.get('lang') or frappe.request.cookies.get('preferred_language')
        
        # Priority 2: Get user's saved language preference (stored in 'language' field)
        if not lang:
            lang = frappe.db.get_value('User', self.user, 'language')
        
        # Priority 3: Fall back to system default
        if not lang:
            lang = frappe.db.get_single_value('System Settings', 'language') or 'en'
        
        # ===== APPLY LANGUAGE TO frappe.local.lang =====
        frappe.local.lang = lang
        
        # Set cookie for subsequent requests
        frappe.local.cookie_manager.set_cookie('preferred_language', lang)
```

---

### Step 6: Update User's `preferred_language` Field

If the user selects a new language on the login page, the system may update their saved preference:

```python
# frappe/auth.py or custom handler

def update_user_language_preference(user, language):
    """
    Update the User doctype's language field.
    This persists the user's language choice for future sessions.
    """
    if language:
        # ===== UPDATE 'language' FIELD (stores preferred language) =====
        frappe.db.set_value('User', user, 'language', language)
        frappe.db.commit()
```

In the User doctype (`frappe/core/doctype/user/user.json`), the `language` field stores the user's preferred language:

```json
{
    "fieldname": "language",
    "fieldtype": "Link",
    "label": "Language",
    "options": "Language",
    "description": "User's preferred language for the interface"
}
```

> **Note**: In Frappe, the field is named `language` in the database schema, but it's often referred to as the user's "preferred language" in documentation and UI. Both terms refer to the same `User.language` field.
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LOGIN FLOW                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. User fills login form:                                                   │
│     ┌──────────────────────────┐                                             │
│     │ Username: ahmad          │                                             │
│     │ Password: ****           │                                             │
│     │ Language: [عربي ▼]       │  ◄─── Language selector                     │
│     │ [Login]                  │                                             │
│     └──────────────────────────┘                                             │
│                  │                                                           │
│                  ▼                                                           │
│  2. POST /api/method/login                                                   │
│     {usr: "ahmad", pwd: "****", lang: "ar"}                                  │
│                  │                                                           │
│                  ▼                                                           │
│  3. frappe.handler.handle()                                                  │
│     └── Calls login() whitelisted function                                   │
│                  │                                                           │
│                  ▼                                                           │
│  4. LoginManager.authenticate()                                              │
│     └── Validates username/password                                          │
│     └── Returns user if valid                                                │
│                  │                                                           │
│                  ▼                                                           │
│  5. LoginManager.post_login()                                                │
│     ├── Sets frappe.session.user                                             │
│     ├── Calls set_user_language()                                            │
│     │   ├── frappe.local.lang = "ar"  ◄─── SESSION LANGUAGE SET              │
│     │   └── Sets cookie: preferred_language=ar                               │
│     │                                                                        │
│     └── update_user_language_preference()                                    │
│         └── frappe.db.set_value('User', 'ahmad', 'language', 'ar')           │
│                                                                              │
│                  │                                                           │
│                  ▼                                                           │
│  6. Response: Success                                                        │
│     ├── User redirected to Desk                                              │
│     └── All UI rendered in Arabic (ar)                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Code Locations in Frappe

### 1. Setting `frappe.local.lang`

The session language is stored in `frappe.local.lang`. This is set during:

- **Request initialization** (`frappe/app.py`):
  ```python
  def set_request_lang():
      # Check cookie, header, or user preference
      lang = frappe.request.cookies.get('preferred_language')
      if lang:
          frappe.local.lang = lang
  ```

- **After login** (`frappe/auth.py`):
  ```python
  frappe.local.lang = selected_language
  ```

### 2. Updating User's `preferred_language` (language field)

The User doctype has a `language` field that stores the user's preferred language:

- **File**: `frappe/core/doctype/user/user.py`
- **Field**: `language` (Link to Language doctype)

When updated:
```python
frappe.db.set_value('User', username, 'language', 'ar')
```

---

## Custom Implementation for Al-Mofeed HIS

For the Al-Mofeed HIS login screen with a language selector (Arabic/English/Kurdish), you can implement a custom login handler:

### Custom Login API (`mofeed_his/api/auth.py`)

```python
import frappe
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def login_with_language(usr, pwd, lang=None):
    """
    Custom login handler that applies selected language.
    
    Args:
        usr: Username or email
        pwd: Password
        lang: Selected language code (ar, en, ku)
    
    Returns:
        dict: Login result with user info
    """
    # Step 1: Authenticate user
    login_manager = LoginManager()
    login_manager.authenticate(usr, pwd)
    
    # Step 2: Apply selected language to session
    if lang:
        frappe.local.lang = lang
        frappe.local.cookie_manager.set_cookie('preferred_language', lang)
    
    # Step 3: Complete login process
    login_manager.post_login()
    
    # Step 4: Update user's language preference if provided
    if lang:
        frappe.db.set_value('User', login_manager.user, 'language', lang)
        frappe.db.commit()
    
    return {
        'message': 'Logged In',
        'user': login_manager.user,
        'language': lang or frappe.local.lang
    }
```

### Frontend Call

```javascript
frappe.call({
    method: 'mofeed_his.api.auth.login_with_language',
    args: {
        usr: $('#username').val(),
        pwd: $('#password').val(),
        lang: $('#language-selector').val()  // 'ar', 'en', or 'ku'
    },
    callback: function(r) {
        if (r.message) {
            // Redirect to workspace
            window.location.href = '/app';
        }
    }
});
```

---

## Summary

| Step | Action | Code Location |
|------|--------|---------------|
| 1 | User submits login form with language | Frontend JS |
| 2 | Request hits `/api/method/login` | `frappe/handler.py` |
| 3 | `LoginManager.authenticate()` validates | `frappe/auth.py` |
| 4 | `post_login()` sets session | `frappe/auth.py` |
| 5 | `frappe.local.lang = lang` | Session language applied |
| 6 | `User.language = lang` saved to DB | `frappe/core/doctype/user/user.py` |
| 7 | Cookie set for future requests | `frappe.cookie_manager` |

---

## References

- [Frappe Auth Module](https://github.com/frappe/frappe/blob/develop/frappe/auth.py)
- [Frappe Handler](https://github.com/frappe/frappe/blob/develop/frappe/handler.py)
- [User DocType](https://github.com/frappe/frappe/blob/develop/frappe/core/doctype/user/user.py)
- [Translation System](https://frappeframework.com/docs/user/en/translations)
