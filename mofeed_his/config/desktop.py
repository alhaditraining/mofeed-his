"""
Mofeed HIS Desktop Configuration

Configures the module appearance in the Frappe Desk sidebar.
Uses healthcare theme color and icon.
"""

from frappe import _


def get_data():
    return [
        {
            "module_name": "Mofeed HIS",
            "category": "Modules",
            "label": _("Mofeed HIS"),
            "color": "#0C82E6",  # Medical Blue - primary color
            "icon": "fa fa-hospital-o",
            "type": "module",
            "description": _("Hospital Information System - Clinics, Patients, Encounters"),
            "onboard_present": 1,
        }
    ]
