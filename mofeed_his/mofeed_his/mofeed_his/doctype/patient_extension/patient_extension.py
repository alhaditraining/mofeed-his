# Copyright (c) 2025, Al-Mofeed Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PatientExtension(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		coverage_percentage: DF.Percent
		district: DF.Data | None
		emergency_contact_name: DF.Data | None
		emergency_contact_phone: DF.Data | None
		emergency_contact_relation: DF.Literal["", "Spouse", "Parent", "Child", "Sibling", "Relative", "Friend", "Other"]
		full_address: DF.SmallText | None
		governorate: DF.Literal["", "Baghdad", "Basra", "Maysan", "Dhi Qar", "Muthanna", "Qadisiyyah", "Babylon", "Karbala", "Najaf", "Wasit", "Diyala", "Saladin", "Kirkuk", "Sulaymaniyah", "Erbil", "Duhok", "Ninawa", "Anbar"]
		has_insurance: DF.Check
		hospital: DF.Link
		insurance_company: DF.Data | None
		insurance_expiry: DF.Date | None
		insurance_id: DF.Data | None
		insurance_plan: DF.Data | None
		is_active: DF.Check
		mother_name: DF.Data | None
		mrn: DF.Data
		national_id: DF.Data | None
		national_id_type: DF.Literal["", "Unified National Card", "Civil Status ID", "Nationality Certificate", "Passport", "Residence Card"]
		nationality: DF.Data | None
		neighborhood: DF.Data | None
		patient_link: DF.Link
		primary_phone: DF.Data | None
		registration_date: DF.Date | None
		secondary_phone: DF.Data | None
		tribe: DF.Data | None
	# end: auto-generated types

	def before_insert(self):
		"""Generate MRN before inserting the document."""
		if not self.mrn:
			self.mrn = self.generate_mrn()

	def generate_mrn(self):
		"""
		Generate a Medical Record Number with facility prefix.
		Format: YYYY-PREFIX-NNNNN (e.g., 2025-KRB-00001)
		"""
		import datetime

		year = datetime.datetime.now().year

		# Get hospital prefix
		prefix = "MFD"  # Default prefix
		if self.hospital:
			hospital = frappe.get_doc("Hospital", self.hospital)
			if hospital.mrn_prefix:
				prefix = hospital.mrn_prefix

		# Get the next sequence number for this hospital and year
		filters = {
			"hospital": self.hospital,
			"mrn": ["like", f"{year}-{prefix}-%"]
		}

		existing_count = frappe.db.count("Patient Extension", filters)
		next_number = existing_count + 1

		return f"{year}-{prefix}-{next_number:05d}"
