# Copyright (c) 2025, Al-Mofeed Team and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Hospital(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		address_line_1: DF.Data | None
		address_line_2: DF.Data | None
		city: DF.Data | None
		country: DF.Link | None
		email: DF.Data | None
		governorate: DF.Data | None
		hospital_code: DF.Data
		hospital_name: DF.Data
		hospital_type: DF.Literal["", "General Hospital", "Specialized Hospital", "Medical Center", "Clinic", "Polyclinic"]
		is_active: DF.Check
		mrn_prefix: DF.Data
		phone: DF.Data | None
		website: DF.Data | None
	# end: auto-generated types

	pass
