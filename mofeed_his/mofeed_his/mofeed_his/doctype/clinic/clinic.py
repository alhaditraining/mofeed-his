# Copyright (c) 2025, Al-Mofeed Team and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Clinic(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		clinic_code: DF.Data
		clinic_name: DF.Data
		clinic_type: DF.Literal["", "Outpatient", "Inpatient", "Emergency", "Daycare", "Diagnostic"]
		default_consultation_fee: DF.Currency
		default_followup_fee: DF.Currency
		description: DF.SmallText | None
		hospital: DF.Link
		is_active: DF.Check
		max_patients_per_slot: DF.Int
		slot_duration: DF.Int
		specialty: DF.Literal["", "General Practice", "Internal Medicine", "Pediatrics", "Dermatology", "Orthopedics", "Cardiology", "Neurology", "Ophthalmology", "ENT", "Obstetrics & Gynecology", "General Surgery", "Urology", "Psychiatry", "Dentistry", "Radiology", "Pathology", "Emergency Medicine", "Anesthesiology", "Oncology", "Nephrology", "Gastroenterology", "Pulmonology", "Endocrinology", "Rheumatology", "Physical Therapy"]
		working_days: DF.Literal["", "Sunday to Thursday", "Saturday to Thursday", "Saturday to Wednesday", "All Week"]
		working_hours_end: DF.Time | None
		working_hours_start: DF.Time | None
	# end: auto-generated types

	pass
