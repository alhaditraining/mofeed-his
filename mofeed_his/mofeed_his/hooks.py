app_name = "mofeed_his"
app_title = "Al-Mofeed HIS"
app_publisher = "Al-Mofeed Team"
app_description = "Al-Mofeed Hospital Information System - Custom Frappe App for Iraqi Healthcare"
app_email = "info@mofeed-his.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext", "healthcare"]

# Web assets
web_include_css = "/assets/mofeed_his/css/mofeed_login.css"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Patient": {
		"before_insert": "mofeed_his.mofeed_his.utils.mrn.generate_patient_mrn",
		"validate": "mofeed_his.mofeed_his.utils.mrn.validate_mrn_unique",
	}
}

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

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [["name", "in", ["Patient-custom_mrn", "Patient-custom_hospital"]]],
	},
	{
		"dt": "Property Setter",
		"filters": [
			["name", "in", ["Patient-custom_mrn-unique", "Patient-custom_mrn-search_index"]],
		],
	},
]

# Website Route Rules
website_route_rules = [
    {"from_route": "/login", "to_route": "mofeed_login"},
]
