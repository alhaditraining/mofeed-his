# Copyright (c) 2025, Al-Mofeed HIS Team and contributors
# For license information, please see license.txt

"""
Mofeed Login Page Controller

Custom login page for Al-Mofeed HIS with multi-language support.
This controller handles the context for the mofeed_login.html template.
"""

import frappe

no_cache = 1


def get_context(context):
    """
    Build context for the custom login page.
    
    - Sets up language from user preference or request
    - Handles redirect after login
    - Provides CSRF token for form submission
    """
    # Check if user is already logged in
    if frappe.session.user != "Guest":
        redirect_url = frappe.local.request.args.get("redirect-to") or "/app"
        frappe.local.flags.redirect_location = redirect_url
        raise frappe.Redirect
    
    # Get language preference
    lang = frappe.local.request.args.get("lang") or frappe.local.lang or "en"
    
    # Set up context
    context.no_cache = 1
    context.for_test = frappe.local.request.args.get("for_test")
    context.title = frappe._("Login") + " – " + frappe._("Al-Mofeed HIS")
    
    return context
