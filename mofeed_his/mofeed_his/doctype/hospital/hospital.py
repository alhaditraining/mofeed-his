"""Hospital DocType controller.

This doctype represents a Hospital/Facility in the system.
Each hospital has a unique code that is used as a prefix for MRN generation.
"""

import frappe
from frappe.model.document import Document


class Hospital(Document):
    """Hospital/Facility master data.

    Attributes:
        hospital_name: Name of the hospital
        code: Unique code used as MRN prefix (e.g., KRBHOSP)
        location: Hospital location
        address: Full address
    """

    def validate(self):
        """Validate hospital data before saving."""
        # Ensure code is uppercase and trimmed
        if self.code:
            self.code = self.code.strip().upper()

        # Validate code format (alphanumeric only)
        if self.code and not self.code.isalnum():
            frappe.throw("Hospital Code must contain only alphanumeric characters")
