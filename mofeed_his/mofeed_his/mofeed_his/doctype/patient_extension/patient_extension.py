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
		Uses database MAX to avoid race conditions.
		"""
		import datetime
		import re

		year = datetime.datetime.now().year

		# Get hospital prefix
		prefix = "MFD"  # Default prefix
		if self.hospital:
			hospital = frappe.get_doc("Hospital", self.hospital)
			if hospital.mrn_prefix:
				prefix = hospital.mrn_prefix

		# Pattern for this hospital and year
		mrn_pattern = f"{year}-{prefix}-%"

		# Get the maximum MRN number for this hospital and year using SQL
		# This is more reliable than counting for concurrent insertions
		result = frappe.db.sql("""
			SELECT MAX(mrn) as max_mrn
			FROM `tabPatient Extension`
			WHERE hospital = %s AND mrn LIKE %s
		""", (self.hospital, mrn_pattern), as_dict=True)

		next_number = 1
		if result and result[0].max_mrn:
			# Extract the number from the MRN (e.g., "2025-KRB-00005" -> 5)
			match = re.search(r'-(\d+)$', result[0].max_mrn)
			if match:
				next_number = int(match.group(1)) + 1

		return f"{year}-{prefix}-{next_number:05d}"
