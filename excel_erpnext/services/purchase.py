import frappe
import json
import base64

from frappe import _

@frappe.whitelist()
def receipt(uuid, filedata, *args, **kwargs):

	json_file = base64.decodestring(filedata.encode('utf-8'))

	if not json_file:
		frappe.local.response['http_status_code'] = 400
		return _("Please upload file")

	if json_file:
		try:
			json_doc = json.loads(json_file)
			print(json_doc)
			frappe.enqueue(
				get_method(),
				json_doc=json_doc,
				user=frappe.session.user,
				uuid=uuid,
			)
			frappe.local.response['http_status_code'] = 202
			return _("accepted")
		except json.decoder.JSONDecodeError as exc:
			frappe.local.response['http_status_code'] = 400
			return _("Invalid JSON")


def enqueue_receipt(json_doc, user, uuid):
	# Set user from request
	frappe.set_user(user)

	# Set background job metadata
	background_log = frappe.new_doc("Excel Background Log")
	background_log.uuid = uuid
	background_log.method = get_method()

	try:
		# Save Purchase Receipt
		doc = frappe.get_doc(frappe._dict(json_doc))
		doc.save()
		frappe.db.commit()

		# Submit Purchase Receipt
		doc.submit()
		frappe.db.commit()

		# Save success to custom doctype
		background_log.success_log = doc.get('name')
		background_log.save()
		frappe.db.commit()

	except Exception as exc:
		# Save error to custom doctype
		background_log.error_log = repr(exc)
		background_log.save()
		frappe.db.commit()

def get_method():
	return 'excel_erpnext.services.purchase.enqueue_receipt'
