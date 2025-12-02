"""
Custom Login Page Controller for Al-Mofeed HIS

This controller handles the custom login page with multi-language support
for Arabic, English, and Kurdish languages.

Integration with ERPNext/Frappe:
--------------------------------
1. Web Page Template: This controller works with the mofeed_login.html template
   in templates/pages/. It provides the context data needed by the template.

2. Language Handling: Detects and sets the user's preferred language, which
   affects the session language after login.

3. Website Route: Defined in hooks.py as website_route_rules to override the
   default Frappe login page.

4. Session Management: Works with Frappe's session to maintain language
   preferences and authentication state.

5. Security: Integrates with Frappe's CSRF protection and rate limiting.

Usage:
------
This page is accessed at /login and replaces the default Frappe login.
The route is configured in hooks.py:
    website_route_rules = [
        {"from_route": "/login", "to_route": "mofeed_login"},
    ]
"""

import frappe
from frappe import _


def get_context(context):
    """
    Build the context for the login page template.
    
    This function is called automatically by Frappe when rendering
    the mofeed_login.html template.
    
    Args:
        context: The page context dictionary to populate
        
    Returns:
        dict: Updated context with login page data
    """
    # Redirect if already logged in
    if frappe.session.user != "Guest":
        redirect_to = get_home_page_for_user(frappe.session.user)
        frappe.local.flags.redirect_location = redirect_to
        raise frappe.Redirect
    
    # Get the logo from website settings or use default
    context.logo = get_login_logo()
    
    # Get current language from session or browser
    context.current_language = get_current_language()
    
    # Get app version
    context.app_version = get_app_version()
    
    # Page metadata
    context.no_cache = 1
    context.no_breadcrumbs = True
    context.no_header = True
    context.no_sidebar = True
    
    # Add CSRF token to context
    context.csrf_token = frappe.sessions.get_csrf_token()
    
    # Custom page title
    context.title = _("Login") + " - Al-Mofeed HIS"
    
    # Languages supported
    context.languages = [
        {"code": "ar", "name": "العربية", "flag": "🇮🇶"},
        {"code": "en", "name": "English", "flag": "🇬🇧"},
        {"code": "ckb", "name": "کوردی", "flag": "🇮🇶"},
    ]
    
    return context


def get_login_logo():
    """
    Get the logo URL for the login page.
    
    Checks in order:
    1. Mofeed HIS Settings (if exists)
    2. Website Settings
    3. Default placeholder
    
    Returns:
        str: URL to the logo image or None
    """
    # Try Mofeed HIS Settings first (custom settings doctype)
    if frappe.db.exists("DocType", "Mofeed HIS Settings"):
        logo = frappe.db.get_single_value("Mofeed HIS Settings", "login_logo")
        if logo:
            return logo
    
    # Fallback to Website Settings
    website_logo = frappe.db.get_single_value("Website Settings", "app_logo") or \
                   frappe.db.get_single_value("Website Settings", "splash_image")
    
    if website_logo:
        return website_logo
    
    # Return None to use placeholder
    return None


def get_current_language():
    """
    Determine the current language for the login page.
    
    Priority:
    1. URL parameter (?lang=ar)
    2. Session language
    3. Browser Accept-Language header
    4. Default to English
    
    Returns:
        str: Language code (ar, en, or ckb)
    """
    # Check URL parameter
    lang_param = frappe.form_dict.get("lang")
    if lang_param and lang_param in ["ar", "en", "ckb"]:
        return lang_param
    
    # Check session
    if hasattr(frappe.local, "lang"):
        return frappe.local.lang
    
    # Check browser preference
    accept_language = frappe.request.headers.get("Accept-Language", "")
    if "ar" in accept_language:
        return "ar"
    if "ckb" in accept_language or "ku" in accept_language:
        return "ckb"
    
    # Default to English
    return "en"


def get_app_version():
    """
    Get the current version of the mofeed_his app.
    
    Returns:
        str: Version string (e.g., "0.1.0")
    """
    try:
        from mofeed_his import __version__
        return __version__
    except ImportError:
        return "1.0.0"


def get_home_page_for_user(user):
    """
    Determine the appropriate home page for a user based on their role.
    
    Args:
        user: User ID
        
    Returns:
        str: URL path to redirect to
    """
    # Get user's roles
    user_roles = frappe.get_roles(user)
    
    # Role-based home pages (defined in hooks.py role_home_page)
    if "Receptionist" in user_roles:
        return "/reception-workspace"
    if "Physician" in user_roles:
        return "/doctor-workbench"
    
    # Default to desk
    return "/desk"


@frappe.whitelist(allow_guest=True)
def login_with_language(usr, pwd, language="en"):
    """
    Custom login method that also sets language preference.
    
    This is an alternative to the standard frappe.auth.login that
    also handles language setting.
    
    Args:
        usr: Username or email
        pwd: Password
        language: Language code (ar, en, ckb)
        
    Returns:
        dict: Login result with message
    """
    try:
        # Use Frappe's standard login
        frappe.auth.LoginManager().authenticate(usr, pwd)
        
        # Set language if login successful
        if language and language in ["ar", "en", "ckb"]:
            frappe.db.set_value("User", frappe.session.user, "language", language)
        
        # Get redirect URL
        redirect_url = get_home_page_for_user(frappe.session.user)
        
        return {
            "success": True,
            "message": _("Login successful"),
            "redirect": redirect_url
        }
        
    except frappe.AuthenticationError:
        frappe.clear_messages()
        return {
            "success": False,
            "message": _("Invalid username or password")
        }
    except frappe.SecurityException as e:
        frappe.clear_messages()
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist(allow_guest=True)
def set_session_language(language):
    """
    Set the session language for guests (before login).
    
    This is used to switch the login page language.
    
    Args:
        language: Language code (ar, en, ckb)
        
    Returns:
        dict: Result
    """
    if language not in ["ar", "en", "ckb"]:
        return {"success": False, "message": _("Invalid language")}
    
    frappe.local.lang = language
    
    return {"success": True, "language": language}
