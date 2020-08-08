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
			frappe.enqueue(
				get_method(),
				json_doc=json_file,
				user=frappe.session.user,
				uuid=uuid,
			)
			frappe.local.response['http_status_code'] = 202
			return _("accepted")
		except json.decoder.JSONDecodeError as exc:
			frappe.local.response['http_status_code'] = 400
			return _("Invalid JSON")


def enqueue_receipt(json_string, user, uuid):
	# Set background job metadata
	background_log = frappe.new_doc("Excel Background Log")
	background_log.uuid = uuid
	background_log.method = get_method()
	background_log.body = json_string
	background_log.type = 'Purchase Receipt'
	background_log.status = 'Queued'
	background_log.user = user
	background_log.save()
	frappe.db.commit()

def get_method():
	return 'excel_erpnext.services.purchase.enqueue_receipt'
