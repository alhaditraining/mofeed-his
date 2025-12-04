# Copyright (c) 2025, Al-Mofeed Team and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class ClinicService(Document):
	"""
	Clinic Service child table for mapping services to rates in a Clinic.
	
	Fields:
		- service: Link to Item doctype (required)
		- rate: Currency field for service pricing (non-negative)
	"""
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		rate: DF.Currency
		service: DF.Link
	# end: auto-generated types

	pass
