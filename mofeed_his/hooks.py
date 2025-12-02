"""
hooks.py - Main Configuration File for Mofeed HIS

This file defines how the mofeed_his app integrates with Frappe/ERPNext framework.
It configures app metadata, assets, permissions, doctypes customization, 
scheduled jobs, overrides, and more.

Key Integration Points with ERPNext/Healthcare:
1. app_include_css/js - Loads custom CSS/JS on all desk pages
2. website_route_rules - Defines custom login page route
3. doctype_js - Extends Patient and other Healthcare doctypes with custom JS
4. doc_events - Hooks into lifecycle events of Healthcare doctypes
5. fixtures - Exports custom fields, property setters for Patient Extension
6. scheduler_events - Background jobs for queue management, reports

"""

app_name = "mofeed_his"
app_title = "Mofeed HIS"
app_publisher = "Al-Mofeed Healthcare Solutions"
app_description = "Hospital Information System for clinics and hospitals in Iraq, built on ERPNext + Healthcare"
app_email = "support@mofeed.iq"
app_license = "MIT"
app_icon = "octicon octicon-heart"
app_color = "#0C82E6"  # Medical Blue - matching the UI guidelines

# Required Apps - This app depends on these
required_apps = ["erpnext", "healthcare"]

# Includes in <head>
# ------------------

# Custom CSS for healthcare theme - loaded on all Desk pages
app_include_css = [
    "/assets/mofeed_his/css/mofeed_his.css",
]

# Custom JS for global functionality - loaded on all Desk pages  
app_include_js = [
    "/assets/mofeed_his/js/mofeed_his.js",
]

# Include JS in specific doctypes - extends existing Healthcare doctypes
doctype_js = {
    "Patient": "public/js/patient.js",            # Custom patient form extensions
    "Patient Appointment": "public/js/appointment.js",  # Appointment workflow extensions
    "Patient Encounter": "public/js/encounter.js",      # Encounter form with voice/AI features
}

# Website Routes
# ---------------

# Custom login page with multi-language support
website_route_rules = [
    {"from_route": "/login", "to_route": "mofeed_login"},
]

# Web Page templates
website_context = {
    "splash_image": "/assets/mofeed_his/images/logo.png"
}

# DocType Class Customizations
# ----------------------------

# Override default classes for Healthcare doctypes
# override_doctype_class = {
#     "Patient": "mofeed_his.overrides.patient.MofeedPatient",
# }

# Document Events
# ---------------

# Hook into document lifecycle events
doc_events = {
    "Patient": {
        "before_insert": "mofeed_his.mofeed_his.doctype.patient_extension.patient_extension.before_patient_insert",
        "after_insert": "mofeed_his.mofeed_his.doctype.patient_extension.patient_extension.after_patient_insert",
        "validate": "mofeed_his.mofeed_his.doctype.patient_extension.patient_extension.validate_patient",
    },
    "Patient Appointment": {
        "before_insert": "mofeed_his.events.appointment.before_appointment_insert",
        "on_update": "mofeed_his.events.appointment.on_appointment_update",
    },
    "Patient Encounter": {
        "after_insert": "mofeed_his.events.encounter.after_encounter_insert",
        "on_submit": "mofeed_his.events.encounter.on_encounter_submit",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    # Run every 5 minutes - refresh reception queues
    "cron": {
        "*/5 * * * *": [
            "mofeed_his.tasks.refresh_patient_queues",
        ],
    },
    # Daily at midnight - cleanup and reports
    "daily": [
        "mofeed_his.tasks.generate_daily_reports",
    ],
    # Weekly on Sunday - analytics
    "weekly": [
        "mofeed_his.tasks.generate_weekly_analytics",
    ],
}

# Fixtures - Export custom configurations
# ----------------------------------------

# Fixtures define what custom configurations to export when creating app bundle
fixtures = [
    # Custom fields added to existing doctypes (e.g., Patient)
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "in", ["Patient", "Patient Appointment", "Patient Encounter"]],
            ["fieldname", "like", "mofeed_%"]
        ]
    },
    # Property setters for modifying existing fields
    {
        "dt": "Property Setter",
        "filters": [
            ["doc_type", "in", ["Patient", "Patient Appointment", "Patient Encounter"]]
        ]
    },
    # Translation strings for Arabic/Kurdish
    {
        "dt": "Translation",
        "filters": [
            ["language", "in", ["ar", "ckb"]]
        ]
    },
    # Custom Print Formats for healthcare documents
    {
        "dt": "Print Format",
        "filters": [
            ["name", "like", "Mofeed%"]
        ]
    },
]

# Jinja Environment Customizations
# ---------------------------------

# Add custom template filters and globals
jinja = {
    "methods": [
        "mofeed_his.utils.jinja.get_patient_mrn",
        "mofeed_his.utils.jinja.format_arabic_date",
        "mofeed_his.utils.jinja.get_hospital_prefix",
    ],
}

# Permission Query Conditions
# ---------------------------

# Row-level security based on hospital/clinic
permission_query_conditions = {
    "Patient": "mofeed_his.permissions.patient_permission_query",
    "Hospital": "mofeed_his.permissions.hospital_permission_query",
    "Clinic": "mofeed_his.permissions.clinic_permission_query",
}

has_permission = {
    "Patient": "mofeed_his.permissions.patient_has_permission",
}

# Desk Sidebar Workspaces
# -----------------------

# Add custom workspaces for Reception and Doctor
# (defined in mofeed_his/mofeed_his/workspace/)

# Boot Session Info
# ------------------

# Add custom data to frappe.boot for client-side access
boot_session = "mofeed_his.boot.add_to_boot"

# Login/Logout Hooks
# ------------------

# Custom actions on login - e.g., set language preference
on_login = "mofeed_his.auth.on_login"

# User Data Protection (GDPR compliance)
# --------------------------------------

user_data_fields = [
    {
        "doctype": "Patient",
        "filter_by": "owner",
        "redact_fields": ["email", "mobile", "national_id"],
        "partial": 1,
    },
]

# Regional Overrides - Iraq specific
# ----------------------------------

regional_overrides = {
    "Iraq": {
        "mofeed_his.utils.regional.get_region_specific_data": "mofeed_his.utils.iraq.get_iraq_data",
    }
}

# Authentication Backend
# ----------------------

# Custom authentication for login page
# auth_hooks = [
#     "mofeed_his.auth.validate_login",
# ]

# Override Home Page
# ------------------

# Different home pages based on role
role_home_page = {
    "Receptionist": "reception-workspace",
    "Physician": "doctor-workbench",
    "Administrator": "Desk",
}

# Portal Menu Items (if patient portal is enabled later)
# ------------------------------------------------------

# portal_menu_items = [
#     {"title": "My Medical Records", "route": "/my-records", "reference_doctype": "Patient Encounter"},
# ]

# Notification Config
# -------------------

notification_config = "mofeed_his.notifications.get_notification_config"

# Default Settings
# ----------------

default_mail_footer = """
<div style="text-align: center; padding: 10px; color: #666;">
    <small>Powered by Al-Mofeed HIS | مدعوم من نظام المفيد</small>
</div>
"""
