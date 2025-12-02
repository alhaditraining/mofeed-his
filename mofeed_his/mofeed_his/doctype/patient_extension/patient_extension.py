# Copyright (c) 2025, Al-Mofeed HIS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PatientExtension(Document):
    """
    Patient Extension doctype for extending ERPNext Healthcare Patient.
    
    Provides Iraqi healthcare-specific fields:
    - National ID
    - Phone (Iraqi format)
    - Insurance Company and Plan
    - Preferred Language (ar/en/ku)
    - Custom MRN with facility prefix
    
    Each Patient Extension is linked 1:1 to a Patient record.
    """
    
    def validate(self):
        """Validate patient extension data before saving."""
        # Normalize national ID (remove spaces/dashes)
        if self.national_id:
            self.national_id = self.national_id.replace(" ", "").replace("-", "")
