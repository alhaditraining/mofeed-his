"""
Patient Extension Doctype Controller

This doctype extends the standard Healthcare Patient doctype with Iraqi-specific
fields and Al-Mofeed HIS custom functionality.

Integration with ERPNext/Healthcare:
------------------------------------
1. Patient Link: Each Patient Extension record links 1:1 with a Healthcare Patient.
   The extension is automatically created when a new Patient is registered.

2. MRN Generation: Generates unique Medical Record Numbers using the hospital's
   prefix (e.g., 2025-KRB-00001 for Karbala Hospital).

3. Insurance Integration: Links to ERPNext Customer for insurance companies,
   enabling split billing between patient and insurer.

4. doc_events Hook: The before_patient_insert and after_patient_insert functions
   are called via hooks.py whenever a Patient is created, automatically creating
   the extension record.

5. Custom Fields Sync: Key fields from Patient Extension are synced back to
   custom fields on the Patient doctype for easy access.

Key Methods:
- generate_mrn(): Creates a new MRN based on hospital prefix
- validate_national_id(): Validates Iraqi National ID format
- check_insurance_validity(): Checks if insurance is active
- sync_to_patient(): Syncs extension fields to Patient custom fields
"""

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, today
import re


class PatientExtension(Document):
    """Patient Extension DocType Controller"""

    def validate(self):
        """Validate patient extension data"""
        self.validate_national_id()
        self.validate_insurance()
        self.validate_mrn()

    def before_save(self):
        """Actions before saving"""
        if not self.registration_date:
            self.registration_date = today()

    def after_insert(self):
        """Actions after inserting a new record"""
        self.sync_to_patient()

    def on_update(self):
        """Actions after updating"""
        self.sync_to_patient()

    def validate_national_id(self):
        """Validate Iraqi National ID format"""
        if not self.national_id:
            return

        # Remove spaces and normalize
        self.national_id = self.national_id.strip().replace(" ", "")

        # Basic validation for Iraqi ID formats
        # National ID (Unified Card): typically 12 digits
        # Civil ID: typically 8-12 digits
        if self.national_id_type == "National ID (البطاقة الموحدة)":
            if not re.match(r"^\d{12}$", self.national_id):
                frappe.msgprint(
                    frappe._("National ID should be 12 digits for البطاقة الموحدة"),
                    indicator="orange",
                    alert=True
                )

        # Check for duplicate national ID
        existing = frappe.db.exists(
            "Patient Extension",
            {
                "national_id": self.national_id,
                "name": ["!=", self.name]
            }
        )
        if existing:
            frappe.throw(
                frappe._("A patient with this National ID already exists: {0}").format(existing)
            )

    def validate_insurance(self):
        """Validate insurance information"""
        if self.insurance_company:
            # Check if insurance is expired
            if self.insurance_expiry and getdate(self.insurance_expiry) < getdate(today()):
                frappe.msgprint(
                    frappe._("Insurance has expired on {0}").format(self.insurance_expiry),
                    indicator="orange",
                    alert=True
                )
            
            # Update patient type based on insurance
            if not self.patient_type or self.patient_type == "Cash":
                self.patient_type = "Insured"

    def validate_mrn(self):
        """Validate MRN format"""
        if self.mofeed_mrn:
            # Ensure uppercase
            self.mofeed_mrn = self.mofeed_mrn.upper()
            
            # Validate format: YYYY-PREFIX-NNNNN
            if not re.match(r"^\d{4}-[A-Z]+-\d{5}$", self.mofeed_mrn):
                frappe.msgprint(
                    frappe._("MRN format should be YYYY-PREFIX-NNNNN (e.g., 2025-KRB-00001)"),
                    indicator="orange",
                    alert=True
                )

    def sync_to_patient(self):
        """
        Sync extension fields back to Patient doctype custom fields.
        
        This enables quick access to MRN, insurance, etc. directly on Patient
        without having to fetch the extension record.
        """
        if not self.patient:
            return

        try:
            patient = frappe.get_doc("Patient", self.patient)
            
            # Sync custom fields (these are defined in fixtures)
            update_fields = {}
            
            if hasattr(patient, "mofeed_mrn"):
                update_fields["mofeed_mrn"] = self.mofeed_mrn
            if hasattr(patient, "mofeed_hospital"):
                update_fields["mofeed_hospital"] = self.registration_hospital
            if hasattr(patient, "mofeed_patient_type"):
                update_fields["mofeed_patient_type"] = self.patient_type
            if hasattr(patient, "mofeed_is_vip"):
                update_fields["mofeed_is_vip"] = self.is_vip
            if hasattr(patient, "mofeed_insurance_company"):
                update_fields["mofeed_insurance_company"] = self.insurance_company
            if hasattr(patient, "mofeed_national_id"):
                update_fields["mofeed_national_id"] = self.national_id

            if update_fields:
                frappe.db.set_value("Patient", self.patient, update_fields, update_modified=False)

        except Exception as e:
            frappe.log_error(
                title="Patient Extension Sync Error",
                message=f"Error syncing Patient Extension {self.name} to Patient {self.patient}: {str(e)}"
            )

    def check_insurance_validity(self):
        """
        Check if patient's insurance is currently valid.
        
        Returns:
            dict: Insurance validity status and details
        """
        if not self.insurance_company:
            return {
                "valid": False,
                "reason": "No insurance",
                "coverage": 0
            }

        if self.insurance_expiry and getdate(self.insurance_expiry) < getdate(today()):
            return {
                "valid": False,
                "reason": "Insurance expired",
                "expiry_date": self.insurance_expiry,
                "coverage": 0
            }

        return {
            "valid": True,
            "insurance_company": self.insurance_company,
            "plan": self.insurance_plan,
            "coverage": self.coverage_percentage or 0,
            "copay": self.copay_amount or 0,
            "expiry_date": self.insurance_expiry
        }


# =============================================================================
# Document Event Handlers (called from hooks.py)
# =============================================================================

def before_patient_insert(doc, method):
    """
    Called before a new Patient is inserted.
    
    Generates MRN and prepares Patient Extension.
    
    Args:
        doc: Patient document
        method: Event method name
    """
    # Get the default hospital for current user
    hospital = get_default_hospital()
    
    if hospital:
        # Generate MRN
        mrn = generate_mrn_for_hospital(hospital)
        
        # Store in custom field on Patient (if exists)
        if hasattr(doc, "mofeed_mrn"):
            doc.mofeed_mrn = mrn
        if hasattr(doc, "mofeed_hospital"):
            doc.mofeed_hospital = hospital


def after_patient_insert(doc, method):
    """
    Called after a new Patient is inserted.
    
    Creates the Patient Extension record.
    
    Args:
        doc: Patient document
        method: Event method name
    """
    # Check if extension already exists
    if frappe.db.exists("Patient Extension", {"patient": doc.name}):
        return

    hospital = getattr(doc, "mofeed_hospital", None) or get_default_hospital()
    mrn = getattr(doc, "mofeed_mrn", None)

    if not mrn and hospital:
        mrn = generate_mrn_for_hospital(hospital)

    try:
        extension = frappe.new_doc("Patient Extension")
        extension.patient = doc.name
        extension.mofeed_mrn = mrn
        extension.registration_hospital = hospital
        extension.registration_date = today()
        extension.patient_type = "Cash"  # Default
        
        # Copy fields from Patient if available
        if hasattr(doc, "mofeed_national_id") and doc.mofeed_national_id:
            extension.national_id = doc.mofeed_national_id
        
        extension.insert(ignore_permissions=True)
        
        frappe.msgprint(
            frappe._("Patient registered with MRN: {0}").format(mrn),
            indicator="green",
            alert=True
        )

    except Exception as e:
        frappe.log_error(
            title="Patient Extension Creation Error",
            message=f"Error creating Patient Extension for {doc.name}: {str(e)}"
        )


def validate_patient(doc, method):
    """
    Called when Patient is validated.
    
    Performs additional validation for Al-Mofeed requirements.
    
    Args:
        doc: Patient document
        method: Event method name
    """
    # Ensure required fields for Iraqi context
    if not doc.mobile:
        frappe.msgprint(
            frappe._("Mobile number is recommended for appointment reminders"),
            indicator="orange"
        )


# =============================================================================
# Helper Functions
# =============================================================================

def get_default_hospital():
    """
    Get the default hospital for the current user.
    
    Returns:
        str: Hospital name or None
    """
    user = frappe.session.user
    
    # Check user settings for default hospital
    # This would be set in a User Settings custom field
    
    # For now, return the first active hospital
    hospitals = frappe.get_all(
        "Hospital",
        filters={"is_active": 1},
        limit=1
    )
    
    return hospitals[0].name if hospitals else None


def generate_mrn_for_hospital(hospital_name):
    """
    Generate a new MRN for the specified hospital.
    
    Args:
        hospital_name: Name of the hospital
        
    Returns:
        str: Generated MRN (e.g., 2025-KRB-00001)
    """
    hospital = frappe.get_doc("Hospital", hospital_name)
    return hospital.get_next_mrn()


@frappe.whitelist()
def get_patient_extension(patient):
    """
    Get Patient Extension for a patient.
    
    Args:
        patient: Patient name
        
    Returns:
        dict: Patient Extension data or None
    """
    extension = frappe.db.get_value(
        "Patient Extension",
        {"patient": patient},
        [
            "name",
            "mofeed_mrn",
            "patient_type",
            "is_vip",
            "national_id",
            "insurance_company",
            "insurance_plan",
            "coverage_percentage",
            "medical_alerts"
        ],
        as_dict=True
    )
    
    return extension


@frappe.whitelist()
def check_duplicate_patient(national_id=None, mobile=None):
    """
    Check for duplicate patients based on national ID or mobile.
    
    Args:
        national_id: National ID to check
        mobile: Mobile number to check
        
    Returns:
        dict: Duplicate check results
    """
    duplicates = []
    
    if national_id:
        existing = frappe.get_all(
            "Patient Extension",
            filters={"national_id": national_id},
            fields=["patient", "patient_name", "mofeed_mrn"]
        )
        if existing:
            duplicates.extend([
                {**e, "match_field": "National ID"}
                for e in existing
            ])
    
    if mobile:
        existing = frappe.get_all(
            "Patient",
            filters={"mobile": mobile},
            fields=["name", "patient_name"]
        )
        if existing:
            for e in existing:
                if not any(d["patient"] == e["name"] for d in duplicates):
                    duplicates.append({
                        "patient": e["name"],
                        "patient_name": e["patient_name"],
                        "match_field": "Mobile"
                    })
    
    return {
        "has_duplicates": len(duplicates) > 0,
        "duplicates": duplicates
    }
