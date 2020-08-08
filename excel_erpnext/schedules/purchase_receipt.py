def process_pr():
	print('Queuing Now ' * 100)
	d = frappe.new_doc("Excel Background Log")
	d.status = 'Fail'
	d.save()
	frappe.db.commit()
    statuses = frappe.get_list(
        "Excel Background Log",
        fields=["status"],
        filters={"status":"In progress"}
    )

    if len(statuses) > 0:
        return

    background_logs = frappe.get_list(
        "Excel Background Job",
        filters={"status":"Queued"},
        order_by='creation asc'
    )

    if len(background_logs) > 0:
        background_log = frappe.get_doc(
            "Excel Background Job",
            background_logs[0].get('name')
        )

        json_doc = json.loads(background_log.body)
        background_log.status = "In progress"
        background_log.save()
        frappe.db.commit()

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
        	background_log.status = "Complete"
        	background_log.save()
        	frappe.db.commit()

        except Exception as exc:
        	# Delete draft doc
        	if (
        		doc
        		and doc.docstatus == 0
        		and not doc.get('__islocal')
        	):
        		doc.delete()
        		frappe.db.commit()

        	# Save error to custom doctype
        	background_log.error_log = repr(exc)
        	background_log.status = "Fail"
        	background_log.save()
        	frappe.db.commit()
