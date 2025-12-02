"""MRN Sequence DocType controller.

This doctype maintains the running sequence for MRN generation per hospital per year.
It ensures thread-safe incremental MRN numbering.
"""

import frappe
from frappe.model.document import Document


class MRNSequence(Document):
    """MRN Sequence tracker per hospital per year.

    Attributes:
        hospital_code: Hospital code prefix (e.g., KRBHOSP)
        year: Year for the sequence (e.g., 2025)
        current_value: Current running number in the sequence
    """

    pass
