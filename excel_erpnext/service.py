import frappe

@frappe.whitelist(methods=["POST"])
def set_invoice_field(invoice_name, value):
	inv = frappe.get_doc("Sales Invoice", invoice_name)
	inv.check_permission(permtype="write")
	frappe.db.set_value("Sales Invoice", invoice_name, "mrp_sales_grand_total", value)
