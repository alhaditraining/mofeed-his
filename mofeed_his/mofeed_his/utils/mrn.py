"""MRN (Medical Record Number) generation utilities.

This module provides functions to generate unique MRN numbers for patients
in the format: {HOSPITAL_CODE}-{YEAR}-{RUNNING_NUMBER}
Example: KRBHOSP-2025-000123

Design Choices:
1. MRN is added to Patient doctype via customize (or Patient Extension) to
   maintain compatibility with Healthcare module updates.

2. The MRN format follows the PDR specification:
   - Hospital code prefix for facility identification
   - Year component for chronological grouping
   - 6-digit running number for unique identification within year

3. Thread-safe sequence generation using database-level locking
   via SELECT ... FOR UPDATE to prevent duplicate MRNs in concurrent scenarios.

4. The MRN Sequence doctype tracks running numbers per hospital per year,
   allowing for automatic reset at year boundaries.

5. A before_insert hook on Patient ensures MRN is generated before first save.
"""

import frappe
from frappe.utils import nowdate


def get_default_hospital_code():
    """Get the default hospital code for MRN generation.

    Returns the code of the first hospital in the system,
    or raises an error if no hospital is configured.

    Returns:
        str: Hospital code (e.g., 'KRBHOSP')

    Raises:
        frappe.ValidationError: If no hospital is configured
    """
    # Try to get default hospital from Mofeed HIS Settings if it exists
    default_hospital = frappe.db.get_single_value(
        "Mofeed HIS Settings", "default_hospital"
    )
    if default_hospital:
        return frappe.db.get_value("Hospital", default_hospital, "code")

    # Fallback: get the first hospital
    hospital_code = frappe.db.get_value(
        "Hospital", filters={}, fieldname="code", order_by="creation asc"
    )

    if not hospital_code:
        frappe.throw(
            "No hospital configured. Please create a Hospital record first.",
            frappe.ValidationError,
        )

    return hospital_code


def get_next_mrn(hospital_code=None):
    """Generate the next MRN for a given hospital.

    Uses database-level locking to ensure thread-safe sequence generation.
    Format: {HOSPITAL_CODE}-{YEAR}-{RUNNING_NUMBER:06d}

    Args:
        hospital_code: Hospital code prefix. If None, uses default hospital.

    Returns:
        str: Generated MRN (e.g., 'KRBHOSP-2025-000123')

    Raises:
        frappe.ValidationError: If hospital code is invalid
    """
    if not hospital_code:
        hospital_code = get_default_hospital_code()

    # Ensure hospital code is uppercase
    hospital_code = hospital_code.upper()

    # Validate hospital exists
    if not frappe.db.exists("Hospital", {"code": hospital_code}):
        frappe.throw(
            f"Hospital with code '{hospital_code}' not found.",
            frappe.ValidationError,
        )

    # Get current year
    current_year = int(nowdate()[:4])

    # Generate sequence key
    sequence_name = f"{hospital_code}-{current_year}"

    # Use database-level locking for thread safety
    # This ensures concurrent inserts don't get duplicate MRNs
    next_value = _get_next_sequence_value(hospital_code, current_year, sequence_name)

    # Format MRN: HOSPITAL_CODE-YEAR-RUNNING_NUMBER (6 digits, zero-padded)
    mrn = f"{hospital_code}-{current_year}-{next_value:06d}"

    return mrn


def _get_next_sequence_value(hospital_code, year, sequence_name):
    """Get the next sequence value with database-level locking.

    This function uses SELECT ... FOR UPDATE to lock the row
    and prevent race conditions in concurrent environments.

    Args:
        hospital_code: Hospital code prefix
        year: Current year
        sequence_name: Sequence document name

    Returns:
        int: Next sequence value
    """
    # Try to get existing sequence with row lock
    existing = frappe.db.sql(
        """
        SELECT name, current_value
        FROM `tabMRN Sequence`
        WHERE hospital_code = %s AND year = %s
        FOR UPDATE
        """,
        (hospital_code, year),
        as_dict=True,
    )

    if existing:
        # Increment existing sequence
        next_value = existing[0]["current_value"] + 1
        frappe.db.sql(
            """
            UPDATE `tabMRN Sequence`
            SET current_value = %s, modified = NOW()
            WHERE name = %s
            """,
            (next_value, existing[0]["name"]),
        )
    else:
        # Create new sequence for this hospital/year combination
        next_value = 1
        # Use db.sql for direct insert to avoid document lifecycle overhead
        frappe.db.sql(
            """
            INSERT INTO `tabMRN Sequence`
            (name, hospital_code, year, current_value, creation, modified, owner, modified_by)
            VALUES (%s, %s, %s, %s, NOW(), NOW(), %s, %s)
            """,
            (
                sequence_name,
                hospital_code,
                year,
                next_value,
                frappe.session.user,
                frappe.session.user,
            ),
        )

    return next_value


def generate_patient_mrn(doc, method=None):
    """Hook function to generate MRN for new patients.

    This function is called as a before_insert hook on Patient doctype.
    It generates a unique MRN if one is not already assigned.

    Args:
        doc: Patient document
        method: Hook method name (unused, but required for hook signature)
    """
    # Skip if MRN is already set (e.g., migrated data)
    if getattr(doc, "custom_mrn", None):
        return

    # Get hospital code from patient's hospital if set, otherwise use default
    hospital_code = None
    if hasattr(doc, "custom_hospital") and doc.custom_hospital:
        hospital_code = frappe.db.get_value("Hospital", doc.custom_hospital, "code")

    # Generate MRN
    mrn = get_next_mrn(hospital_code)

    # Set MRN on patient document
    doc.custom_mrn = mrn


def validate_mrn_unique(doc, method=None):
    """Validate that MRN is unique across all patients.

    This is called as a validate hook to ensure no duplicate MRNs exist.

    Args:
        doc: Patient document
        method: Hook method name (unused)

    Raises:
        frappe.DuplicateEntryError: If MRN already exists
    """
    if not getattr(doc, "custom_mrn", None):
        return

    # Check for existing patient with same MRN (excluding current doc)
    existing = frappe.db.get_value(
        "Patient",
        {"custom_mrn": doc.custom_mrn, "name": ("!=", doc.name)},
        "name",
    )

    if existing:
        frappe.throw(
            f"MRN '{doc.custom_mrn}' is already assigned to another patient.",
            frappe.DuplicateEntryError,
        )
