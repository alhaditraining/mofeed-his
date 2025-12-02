# Copyright (c) 2025, Al-Mofeed HIS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Clinic(Document):
    """
    Clinic doctype for managing clinics/departments in the Al-Mofeed HIS.
    
    Each clinic belongs to a hospital and has a specialty and type (OPD/IPD/etc.).
    Default services can be configured per clinic.
    """
    
    pass
