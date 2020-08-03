import frappe
import json

from frappe import _

@frappe.whitelist()
def receipt(*args, **kwargs):

	json_file = frappe.request.files.get('json_file')

	if not json_file:
		frappe.local.response['http_status_code'] = 400
		return _("Please upload file")

	if json_file:
		if json_file.filename == '':
			return _('No file selected')

		try:
			pr_json = json.loads(json_file.read().decode('utf-8'))

		except json.decoder.JSONDecodeError as exc:
			frappe.local.response['http_status_code'] = 400
			return _("Invalid JSON")

		frappe.enqueue(
			'excel_erpnext.services.purchase.enqueue_receipt',
			json_array=pr_json,
			user=frappe.session.user,
		)

	frappe.local.response['http_status_code'] = 202
	return _("accepted")

def enqueue_receipt(json_array, user):
	frappe.set_user(user)
	for doc in json_array:
		doc = frappe.get_doc(frappe._dict(doc))
		doc.save()
		doc.submit()

	frappe.db.commit()
