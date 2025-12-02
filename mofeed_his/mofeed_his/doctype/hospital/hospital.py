# Copyright (c) 2025, Al-Mofeed HIS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Hospital(Document):
    """
    Hospital doctype for managing facilities in the Al-Mofeed HIS.
    
    Each hospital has a unique code and prefix used for MRN generation.
    """
    
    def validate(self):
        """Validate hospital data before saving."""
        if self.prefix:
            self.prefix = self.prefix.upper()
