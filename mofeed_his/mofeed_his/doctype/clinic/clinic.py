"""
Clinic Doctype Controller

This doctype represents a clinic/department within a hospital in the Al-Mofeed HIS.
Each clinic belongs to a Hospital and has its own specialty, doctors, and schedule.

Integration with ERPNext/Healthcare:
------------------------------------
1. Medical Department: Links to Healthcare's Medical Department doctype for specialty
   classification and standardization.

2. Healthcare Practitioner: Links doctors assigned to this clinic to the standard
   Healthcare Practitioner doctype.

3. Patient Appointment: Appointments are booked to a specific Clinic, which determines
   available doctors, fees, and time slots.

4. Price Lists: Consultation and follow-up fees integrate with ERPNext's pricing
   system for billing.

5. Queue Management: Each clinic maintains its own patient queue for the reception
   and doctor workbench screens.

Key Methods:
- get_available_slots(): Returns available appointment slots for a date
- get_today_queue(): Returns current patient queue for this clinic
- get_clinic_doctors(): Returns list of doctors available at this clinic
"""

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, get_time


class Clinic(Document):
    """Clinic DocType Controller"""

    def validate(self):
        """Validate clinic data before saving"""
        self.validate_clinic_code()
        self.validate_fees()
        self.set_defaults()

    def validate_clinic_code(self):
        """Generate or validate clinic code"""
        if not self.clinic_code:
            # Auto-generate clinic code from name
            self.clinic_code = self.generate_clinic_code()
        else:
            self.clinic_code = self.clinic_code.upper().strip()

    def generate_clinic_code(self):
        """Generate a clinic code from the clinic name"""
        # Take first letters of each word in clinic name
        words = self.clinic_name.split()
        code = "".join([word[0].upper() for word in words[:3]])
        
        # Ensure uniqueness by adding number if needed
        existing = frappe.db.count("Clinic", {"clinic_code": ["like", f"{code}%"]})
        if existing:
            code = f"{code}{existing + 1}"
        
        return code

    def validate_fees(self):
        """Ensure fees are positive if set"""
        if self.consultation_fee and self.consultation_fee < 0:
            frappe.throw(frappe._("Consultation Fee cannot be negative"))
        if self.follow_up_fee and self.follow_up_fee < 0:
            frappe.throw(frappe._("Follow-up Fee cannot be negative"))

    def set_defaults(self):
        """Set default values"""
        if not self.appointment_duration:
            self.appointment_duration = 15  # 15 minutes default
        if not self.max_daily_appointments:
            self.max_daily_appointments = 30

    def get_available_slots(self, date, doctor=None):
        """
        Get available appointment slots for this clinic on a specific date.
        
        Integrates with Patient Appointment to check existing bookings
        and calculate available time slots.
        
        Args:
            date: Date to check (string or date object)
            doctor: Optional - filter by specific doctor
            
        Returns:
            list: List of available time slots with format {'time': '09:00', 'available': True}
        """
        date = getdate(date)
        weekday = date.strftime("%A")
        
        # Get working hours for this day
        working_day = self.get_working_day(weekday)
        if not working_day or not working_day.get("is_working"):
            return []  # Clinic closed on this day
        
        # Get all existing appointments for this clinic on this date
        filters = {
            "mofeed_clinic": self.name,
            "appointment_date": date,
            "status": ["not in", ["Cancelled"]]
        }
        if doctor:
            filters["practitioner"] = doctor
        
        existing_appointments = frappe.get_all(
            "Patient Appointment",
            filters=filters,
            fields=["appointment_time"]
        )
        
        booked_times = [appt.appointment_time for appt in existing_appointments]
        
        # Generate all possible slots
        slots = []
        from datetime import datetime, timedelta
        
        current_time = get_time(working_day.get("start_time", "08:00"))
        end_time = get_time(working_day.get("end_time", "16:00"))
        slot_duration = self.appointment_duration or 15
        
        while current_time < end_time:
            slot_time = current_time.strftime("%H:%M")
            is_available = slot_time not in booked_times
            
            slots.append({
                "time": slot_time,
                "available": is_available,
                "doctor": doctor
            })
            
            # Move to next slot using timedelta for cleaner time arithmetic
            current_dt = datetime.combine(datetime.today(), current_time)
            current_time = (current_dt + timedelta(minutes=slot_duration)).time()
        
        return slots

    def get_working_day(self, weekday):
        """Get working hours for a specific weekday"""
        for day in self.working_days or []:
            if day.weekday == weekday:
                return {
                    "is_working": day.is_working,
                    "start_time": day.start_time,
                    "end_time": day.end_time
                }
        return None

    def get_today_queue(self):
        """
        Get today's patient queue for this clinic.
        
        Integrates with Patient Appointment to show patients who have
        checked in and are waiting to be seen.
        
        Returns:
            list: Ordered list of patients in queue with status
        """
        today = nowdate()
        
        appointments = frappe.get_all(
            "Patient Appointment",
            filters={
                "mofeed_clinic": self.name,
                "appointment_date": today,
                "status": ["in", ["Scheduled", "Checked In", "In Progress"]]
            },
            fields=[
                "name",
                "patient",
                "patient_name",
                "appointment_time",
                "status",
                "practitioner_name",
                "mofeed_check_in_time"
            ],
            order_by="mofeed_check_in_time asc, appointment_time asc"
        )
        
        # Add queue position
        queue = []
        for idx, appt in enumerate(appointments, 1):
            appt["queue_position"] = idx
            appt["wait_time"] = self.calculate_wait_time(appt)
            queue.append(appt)
        
        return queue

    def calculate_wait_time(self, appointment):
        """Calculate how long a patient has been waiting"""
        if not appointment.get("mofeed_check_in_time"):
            return None
        
        from frappe.utils import time_diff_in_hours, now_datetime
        
        check_in = appointment.get("mofeed_check_in_time")
        wait_hours = time_diff_in_hours(now_datetime(), check_in)
        
        if wait_hours < 1:
            return f"{int(wait_hours * 60)} min"
        return f"{wait_hours:.1f} hr"

    def get_clinic_doctors(self, only_available=False):
        """
        Get list of doctors assigned to this clinic.
        
        Integrates with Healthcare Practitioner doctype.
        
        Args:
            only_available: If True, filter to only currently available doctors
            
        Returns:
            list: List of Healthcare Practitioner details
        """
        doctors = []
        
        # Get from doctors child table
        for doc_row in self.doctors or []:
            practitioner = frappe.get_doc("Healthcare Practitioner", doc_row.doctor)
            doctor_data = {
                "name": practitioner.name,
                "practitioner_name": practitioner.practitioner_name,
                "specialty": practitioner.department,
                "is_primary": doc_row.is_primary
            }
            doctors.append(doctor_data)
        
        # Also include default doctor if not in list
        if self.default_doctor:
            if not any(d["name"] == self.default_doctor for d in doctors):
                practitioner = frappe.get_doc("Healthcare Practitioner", self.default_doctor)
                doctors.insert(0, {
                    "name": practitioner.name,
                    "practitioner_name": practitioner.practitioner_name,
                    "specialty": practitioner.department,
                    "is_primary": True
                })
        
        return doctors

    @frappe.whitelist()
    def get_statistics(self, date=None):
        """
        Get statistics for this clinic.
        
        Args:
            date: Date to get stats for (defaults to today)
            
        Returns:
            dict: Statistics including appointments, patients seen, etc.
        """
        date = date or nowdate()
        
        total_appointments = frappe.db.count("Patient Appointment", {
            "mofeed_clinic": self.name,
            "appointment_date": date
        })
        
        checked_in = frappe.db.count("Patient Appointment", {
            "mofeed_clinic": self.name,
            "appointment_date": date,
            "status": "Checked In"
        })
        
        completed = frappe.db.count("Patient Appointment", {
            "mofeed_clinic": self.name,
            "appointment_date": date,
            "status": "Closed"
        })
        
        return {
            "total_appointments": total_appointments,
            "checked_in": checked_in,
            "completed": completed,
            "waiting": checked_in,
            "remaining": total_appointments - completed
        }


@frappe.whitelist()
def get_clinics_for_hospital(hospital):
    """
    Get all active clinics for a hospital.
    
    Args:
        hospital: Hospital name
        
    Returns:
        list: List of clinic details
    """
    return frappe.get_all(
        "Clinic",
        filters={
            "hospital": hospital,
            "is_active": 1
        },
        fields=[
            "name",
            "clinic_name",
            "clinic_name_arabic",
            "specialty_type",
            "default_doctor",
            "consultation_fee",
            "follow_up_fee"
        ],
        order_by="clinic_name asc"
    )
