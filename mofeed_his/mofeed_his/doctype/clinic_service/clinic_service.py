# Copyright (c) 2025, Al-Mofeed HIS Team and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class ClinicService(Document):
    """
    Clinic Service child doctype.
    
    Links a service Item to a Clinic with an optional custom rate.
    Used as a child table in the Clinic doctype.
    """
    
    pass
