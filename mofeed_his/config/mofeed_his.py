"""
Mofeed HIS Module Configuration

Defines the module sidebar links for the Mofeed HIS module.
"""

from frappe import _


def get_data():
    return [
        {
            "label": _("Setup"),
            "icon": "fa fa-cog",
            "items": [
                {
                    "type": "doctype",
                    "name": "Hospital",
                    "label": _("Hospital"),
                    "description": _("Manage hospitals and facilities"),
                },
                {
                    "type": "doctype",
                    "name": "Clinic",
                    "label": _("Clinic"),
                    "description": _("Manage clinics and departments"),
                },
            ],
        },
        {
            "label": _("Patient Management"),
            "icon": "fa fa-users",
            "items": [
                {
                    "type": "doctype",
                    "name": "Patient Extension",
                    "label": _("Patient Extension"),
                    "description": _("Extended patient information for Iraqi healthcare"),
                },
            ],
        },
    ]
