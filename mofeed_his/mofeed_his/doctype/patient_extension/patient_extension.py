# Copyright (c) 2024, Al-Mofeed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PatientExtension(Document):
    """
    PatientExtension is a custom DocType that extends the Patient doctype with
    additional fields specific to Al-Mofeed HIS:
    - national_id
    - city
    - phone_2
    - insurance_company
    - insurance_plan
    - preferred_language
    """

    pass


def get_or_create_patient_extension(patient_name):
    """
    Returns the PatientExtension document for the given patient.
    If it doesn't exist, creates a new one and returns it.

    Args:
        patient_name (str): The name/id of the Patient document

    Returns:
        PatientExtension: The PatientExtension document for the given patient

    Raises:
        frappe.DoesNotExistError: If the patient does not exist
    """
    if not patient_name:
        frappe.throw("Patient name is required")

    # Verify patient exists
    if not frappe.db.exists("Patient", patient_name):
        frappe.throw(
            f"Patient {patient_name} does not exist",
            frappe.DoesNotExistError
        )

    # Try to get existing extension
    extension_name = frappe.db.get_value(
        "Patient Extension",
        {"patient": patient_name},
        "name"
    )

    if extension_name:
        return frappe.get_doc("Patient Extension", extension_name)

    # Create new extension
    extension = frappe.get_doc({
        "doctype": "Patient Extension",
        "patient": patient_name
    })
    extension.insert(ignore_permissions=True)

    return extension
