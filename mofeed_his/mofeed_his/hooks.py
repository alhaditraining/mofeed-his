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
# Hook into Healthcare Patient to generate/validate MRN values
# while keeping the core Patient doctype untouched.
doc_events = {
    "Patient": {
        "before_insert": "mofeed_his.mofeed_his.utils.mrn.generate_patient_mrn",
        "validate": "mofeed_his.mofeed_his.utils.mrn.validate_mrn_unique",
    }
}

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

website_route_rules = [
    {"from_route": "/login", "to_route": "mofeed_login"},
]
