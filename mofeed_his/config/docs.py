"""
Mofeed HIS Documentation Configuration

Configures documentation for the Mofeed HIS module.
"""

from frappe import _


def get_context(context):
    context.brand_html = "Al-Mofeed HIS"
    context.source_link = "https://github.com/alhaditraining/mofeed-his"
    context.docs_base_url = "https://github.com/alhaditraining/mofeed-his/docs"
    context.headline = _("Hospital Information System for Iraq")
    context.sub_heading = _("Built on ERPNext + Healthcare")
