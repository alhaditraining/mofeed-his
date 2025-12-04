app_name = "mofeed_his"
app_title = "Al-Mofeed HIS"
app_publisher = "Al-Mofeed Team"
app_description = "Al-Mofeed Hospital Information System - Custom Frappe App for Iraqi Healthcare"
app_email = "info@mofeed-his.com"
app_license = "MIT"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "mofeed_his",
# 		"logo": "/assets/mofeed_his/images/mofeed_his_logo.png",
# 		"title": "Al-Mofeed HIS",
# 		"route": "/app/mofeed_his",
# 		"has_permission": "mofeed_his.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mofeed_his/css/mofeed_his.css"
# app_include_js = "/assets/mofeed_his/js/mofeed_his.js"

# include js, css files in header of web template
web_include_css = "/assets/mofeed_his/css/mofeed_login.css"
# web_include_js = "/assets/mofeed_his/js/mofeed_his.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "mofeed_his/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Sprite Icons
# ----------------
# Include custom svg sprite icons for the icons used in the app.
# svg_icons = {"icons" : ["icon1", "icon2", "icon3"]}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mofeed_his.utils.jinja_methods",
# 	"filters": "mofeed_his.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mofeed_his.install.before_install"
# after_install = "mofeed_his.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mofeed_his.uninstall.before_uninstall"
# after_uninstall = "mofeed_his.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mofeed_his.utils.before_app_install"
# after_app_install = "mofeed_his.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mofeed_his.utils.before_app_uninstall"
# after_app_uninstall = "mofeed_his.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mofeed_his.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mofeed_his.tasks.all"
# 	],
# 	"daily": [
# 		"mofeed_his.tasks.daily"
# 	],
# 	"hourly": [
# 		"mofeed_his.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mofeed_his.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mofeed_his.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "mofeed_his.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mofeed_his.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mofeed_his.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mofeed_his.utils.before_request"]
# after_request = ["mofeed_his.utils.after_request"]

# Job Events
# ----------
# before_job = ["mofeed_his.utils.before_job"]
# after_job = ["mofeed_his.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mofeed_his.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Website Route Rules
website_route_rules = [
    {"from_route": "/login", "to_route": "mofeed_login"},
]
