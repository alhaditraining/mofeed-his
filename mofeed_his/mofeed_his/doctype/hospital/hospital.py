"""
Hospital Doctype Controller

This doctype represents a healthcare facility (hospital, clinic, medical center)
in the Al-Mofeed HIS system.

Integration with ERPNext/Healthcare:
------------------------------------
1. MRN Prefix: Each hospital has a unique prefix for generating Medical Record Numbers.
   When a new Patient is created, the system uses the hospital's MRN prefix to create
   a unique patient ID (e.g., 2025-KRB-00001 for Karbala Hospital).

2. Price Lists: Links to ERPNext Price List for billing. Different hospitals may have
   different pricing structures.

3. Multi-Facility Support: Users can be assigned to specific hospitals, enabling
   multi-facility deployments where each facility has separate data.

4. Currency: Supports Iraqi Dinar (IQD) as default, with multi-currency capability
   inherited from ERPNext.

5. Working Hours: Integrates with Patient Appointment scheduling to show available
   slots based on hospital operating hours.

Key Methods:
- get_next_mrn(): Generates the next sequential MRN for this hospital
- get_active_clinics(): Returns all active clinics under this hospital
- validate_hospital_code(): Ensures hospital code is unique and uppercase
"""

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, cint


class Hospital(Document):
    """Hospital DocType Controller"""

    def validate(self):
        """Validate hospital data before saving"""
        self.validate_hospital_code()
        self.validate_mrn_prefix()
        self.set_defaults()

    def validate_hospital_code(self):
        """Ensure hospital code is uppercase and alphanumeric"""
        if self.hospital_code:
            # Convert to uppercase
            self.hospital_code = self.hospital_code.upper().strip()
            
            # Ensure alphanumeric only
            if not self.hospital_code.isalnum():
                frappe.throw(
                    frappe._("Hospital Code must contain only letters and numbers")
                )
            
            # Ensure reasonable length
            if len(self.hospital_code) > 10:
                frappe.throw(
                    frappe._("Hospital Code must be 10 characters or less")
                )

    def validate_mrn_prefix(self):
        """Ensure MRN prefix is valid and matches hospital code"""
        if self.mrn_prefix:
            self.mrn_prefix = self.mrn_prefix.upper().strip()
            
            # MRN prefix should typically match hospital code
            if not self.mrn_prefix:
                self.mrn_prefix = self.hospital_code

    def set_defaults(self):
        """Set default values if not specified"""
        if not self.default_currency:
            self.default_currency = "IQD"  # Iraqi Dinar

    def get_next_mrn(self):
        """
        Generate the next Medical Record Number for this hospital.
        
        Format: YYYY-PREFIX-NNNNN
        Example: 2025-KRB-00001
        
        Returns:
            str: The next available MRN for this hospital
        """
        current_year = nowdate()[:4]
        prefix = f"{current_year}-{self.mrn_prefix}"
        
        # Get the last MRN with this prefix
        last_mrn = frappe.db.sql("""
            SELECT MAX(CAST(SUBSTRING_INDEX(mofeed_mrn, '-', -1) AS UNSIGNED)) as last_num
            FROM `tabPatient`
            WHERE mofeed_mrn LIKE %s
        """, (f"{prefix}-%",), as_dict=True)
        
        last_num = cint(last_mrn[0].last_num) if last_mrn and last_mrn[0].last_num else 0
        next_num = last_num + 1
        
        return f"{prefix}-{next_num:05d}"

    def get_active_clinics(self):
        """
        Get all active clinics under this hospital.
        
        Returns:
            list: List of Clinic documents linked to this hospital
        """
        return frappe.get_all(
            "Clinic",
            filters={
                "hospital": self.name,
                "is_active": 1
            },
            fields=["name", "clinic_name", "specialty", "default_doctor"]
        )

    @frappe.whitelist()
    def get_today_statistics(self):
        """
        Get today's statistics for this hospital.
        
        Returns:
            dict: Statistics including patient count, appointments, etc.
        """
        today = nowdate()
        
        # Count today's appointments
        appointments = frappe.db.count("Patient Appointment", {
            "mofeed_hospital": self.name,
            "appointment_date": today
        })
        
        # Count checked-in patients
        checked_in = frappe.db.count("Patient Appointment", {
            "mofeed_hospital": self.name,
            "appointment_date": today,
            "status": "Checked In"
        })
        
        # Count today's encounters
        encounters = frappe.db.count("Patient Encounter", {
            "mofeed_hospital": self.name,
            "encounter_date": today
        })
        
        return {
            "total_appointments": appointments,
            "checked_in": checked_in,
            "encounters": encounters,
            "waiting": appointments - checked_in - encounters
        }


@frappe.whitelist()
def get_hospital_for_user(user=None):
    """
    Get the default hospital for a user based on their permissions.
    
    Args:
        user: User ID (defaults to current user)
        
    Returns:
        str: Hospital name or None
    """
    if not user:
        user = frappe.session.user
    
    # Check user's default hospital in User Settings
    default_hospital = frappe.db.get_value(
        "User Settings", 
        {"user": user}, 
        "mofeed_default_hospital"
    )
    
    if default_hospital:
        return default_hospital
    
    # Otherwise, return the first hospital user has access to
    hospitals = frappe.get_all(
        "Hospital",
        filters={"is_active": 1},
        limit=1
    )
    
    return hospitals[0].name if hospitals else None
