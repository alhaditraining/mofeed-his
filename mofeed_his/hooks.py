"""
Al-Mofeed HIS - Frappe Hooks Configuration

This file contains the configuration for the mofeed_his Frappe app.
"""

app_name = "mofeed_his"
app_title = "Al-Mofeed HIS"
app_publisher = "Al-Mofeed HIS Team"
app_description = "Hospital Information System for clinics, medical centers, and hospitals in Iraq. Built on ERPNext + Healthcare."
app_email = "info@mofeed-his.com"
app_license = "MIT"
app_icon = "fa fa-hospital-o"
app_color = "#0C82E6"  # Medical Blue - primary color from theme guidelines

# Required apps
# NOTE: This app requires ERPNext and Healthcare app to be installed first.
# Install with: bench get-app healthcare && bench --site <site> install-app healthcare
required_apps = ["frappe", "erpnext", "healthcare"]

# Includes in <head>
# ------------------

# Include JS and CSS in desk
app_include_css = "/assets/mofeed_his/css/mofeed_his.css"
app_include_js = "/assets/mofeed_his/js/mofeed_his.js"

# Include JS and CSS for website
web_include_css = "/assets/mofeed_his/css/mofeed_login.css"
web_include_js = "/assets/mofeed_his/js/mofeed_login.js"

# Include custom SCSS if needed
# app_include_scss = "mofeed_his/public/scss/mofeed_his.scss"

# Website route rules
# Override the login page with custom multi-language login
website_route_rules = [
    {"from_route": "/login", "to_route": "mofeed_login"},
]

# Website context additions
# website_context = {
#     "favicon": "/assets/mofeed_his/images/favicon.ico",
# }

# Jinja environment customization for templates
# jinja = {
#     "methods": [],
#     "filters": []
# }

# Installation
# ------------

# before_install = "mofeed_his.install.before_install"
# after_install = "mofeed_his.install.after_install"

# After Migrate hooks
# after_migrate = []

# Uninstallation
# before_uninstall = "mofeed_his.uninstall.before_uninstall"
# after_uninstall = "mofeed_his.uninstall.after_uninstall"

# Desk Notifications
# notification_config = "mofeed_his.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#     "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }

# has_permission = {
#     "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# -------------
# Override standard doctype classes

# override_doctype_class = {
#     "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#     "*": {
#         "on_update": "method",
#         "on_cancel": "method",
#         "on_trash": "method"
#     }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#     "all": [],
#     "daily": [],
#     "hourly": [],
#     "weekly": [],
#     "monthly": [],
#     "cron": {
#         "0 0 * * *": []
#     }
# }

# Testing
# -------

# before_tests = "mofeed_his.install.before_tests"

# Overriding Methods
# ------------------

# override_whitelisted_methods = {
#     "frappe.desk.doctype.event.event.get_events": "mofeed_his.event.get_events"
# }

# Each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#     "Task": "mofeed_his.task.get_dashboard_data"
# }

# Exempt linked doctypes from being automatically cancelled
# auto_cancel_exempted_doctypes = []

# User Data Protection
# --------------------

# user_data_fields = [
#     {
#         "doctype": "{doctype_1}",
#         "filter_by": "{filter_by}",
#         "redact_fields": ["{field_1}", "{field_2}"],
#         "partial": 1,
#     },
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#     "mofeed_his.auth.validate"
# ]

# Fixtures
# --------
# Fixtures for exporting/importing data

fixtures = []

# Translation
# -----------

# Make link fields searchable
# ---------------------------

# Translation for custom doctypes
# Automatically translated fields based on language setting

# Home page setup
# ---------------

# home_page = "login"
