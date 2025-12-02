"""
Frappe Hooks for Al-Mofeed HIS

This file contains the configuration for the mofeed_his Frappe application.
"""

app_name = "mofeed_his"
app_title = "Mofeed HIS"
app_publisher = "Al-Mofeed HIS Team"
app_description = "Al-Mofeed Hospital Information System"
app_email = "info@mofeed-his.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext", "healthcare"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/mofeed_his/css/mofeed_his.css"
app_include_js = "/assets/mofeed_his/js/mofeed_his.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "mofeed_his/public/scss/website"

# Fixtures
# --------

fixtures = [
    {"dt": "Workspace", "filters": [["module", "=", "Mofeed HIS"]]}
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# Document Events
# ---------------

# Hook on document methods and events

# Scheduled Tasks
# ---------------

# scheduler_events = {}

# App Include
# -----------

# include app include js files
# app_include_js = "/assets/mofeed_his/js/mofeed_his.js"

# Desk Notifications
# ------------------

# See frappe.core.notifications.get_notification_config

# notification_config = "mofeed_his.notifications.get_notification_config"

# Permissions
# -----------

# Permissions evaluated in scripted ways

# permission_query_conditions = {}

# has_permission = {}

# DocType Class
# -------------

# Override standard doctype classes

# override_doctype_class = {}

# Document Events
# ---------------

# Hook on document methods and events

# doc_events = {}
