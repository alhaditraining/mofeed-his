"""Frappe hooks configuration for mofeed_his app.

This file defines all the hooks that integrate mofeed_his with the Frappe framework.

Design Choice for MRN Generation:
---------------------------------
We use `doc_events` hooks on the Patient doctype (from Healthcare module) to:
1. Generate MRN on `before_insert` - ensures MRN is set before first save
2. Validate MRN uniqueness on `validate` - prevents duplicates

Alternative approaches considered:
- Custom controller override: Would require patching Healthcare module
- Client-side generation: Not reliable for uniqueness guarantees
- Autoname: Healthcare Patient already has its own naming, MRN is separate field

The `custom_mrn` field is added via Property Setter or Customize Form to maintain
compatibility with Healthcare module updates.
"""

app_name = "mofeed_his"
app_title = "Mofeed HIS"
app_publisher = "Al-Mofeed"
app_description = "Hospital Information System for clinics and hospitals in Iraq"
app_email = "info@mofeed.iq"
app_license = "MIT"

# Document Events
# ----------------
# Hook on document events for core functionality

doc_events = {
    # MRN Generation Hook for Patient doctype
    # Generates unique facility-prefixed MRN on patient creation
    "Patient": {
        "before_insert": "mofeed_his.mofeed_his.utils.mrn.generate_patient_mrn",
        "validate": "mofeed_his.mofeed_his.utils.mrn.validate_mrn_unique",
    }
}

# Fixtures
# --------
# Fixtures are used to export/import custom fields, property setters, etc.
# This ensures the custom_mrn field is created on installation

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                "Patient-custom_mrn",
                "Patient-custom_hospital",
            ]]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["name", "in", [
                "Patient-custom_mrn-unique",
                "Patient-custom_mrn-search_index",
            ]]
        ]
    }
]

# Installation Hooks
# ------------------
# Called after app installation to set up initial data

# after_install = "mofeed_his.install.after_install"

# Scheduled Tasks
# ---------------
# Define scheduled tasks here

# scheduler_events = {
#     "daily": [
#         "mofeed_his.tasks.daily"
#     ]
# }

# Jinja Environment
# -----------------
# Add custom filters/functions to Jinja templates

# jinja = {
#     "methods": [],
#     "filters": []
# }

# Override Methods
# ----------------
# Override standard frappe/erpnext methods

# override_whitelisted_methods = {}

# DocType Class Mappings
# ----------------------
# Override standard doctype classes

# override_doctype_class = {}

# Required Apps
# -------------
# Apps that must be installed before this app

required_apps = ["frappe", "erpnext", "healthcare"]
