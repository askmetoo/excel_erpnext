# Copyright (c) 2013, Castlecraft Ecommerce Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):

	conditions= ""

	if filters.get("from_date"):
		conditions +=" epr.start_date >= '{}' ".format(filters.get("from_date"))

	if filters.get("to_date"):
		conditions +="AND epr.start_date <= '{}' ".format(filters.get("to_date"))

	if filters.get("project_name"):
		conditions +=" AND epr.name = '{}' ".format(filters.get("project_name"))

	if filters.get("project_status"):
		conditions +=" AND epr.project_status = '{}' ".format(filters.get("project_status"))	

	if filters.get("docstatus"):
		if filters.get("docstatus") == "Draft":
			conditions +=" AND epr.docstatus = 0 "
		elif filters.get("docstatus") == "Submitted":
			conditions +=" AND epr.docstatus = 1 "
		elif filters.get("docstatus") == "Cancelled":
			conditions +=" AND epr.docstatus = 2 "
			
	return frappe.db.sql(
		f"""
		SELECT
			epr.name, 
			(case when epr.docstatus=0 then 'Draft'
             when epr.docstatus=1 then 'Submitted'
             else 'Cancelled'
             end) as docstatus, epr.project_name, epr.project_status, epr.start_date, epr.expected_handover_date,
			epr.customer_name, epr.customer_address, epr.customer_contact_person, epr.si_name, epr.customer_mobile, epr.project_category, 
			epr.final_invoice_submission_date, epr.final_handover_date, epr.final_invoice_submitted_by, epr.project_incharge_sales, 
			epr.project_incharge_tech, TIMESTAMPDIFF(DAY, epr.final_invoice_submission_date, "{filters.get("to_date")}") as ageing,
			epti.invoice_no, epti.invoice_date, epti.customer_name, epti.amount
		FROM  `tabExcel Project Tracking` epr, `tabExcel Project Tracking Invoice Table` 
		epti WHERE {conditions} AND epr.name = epti.parent ORDER BY epr.name DESC
		""",as_dict=1)

def get_columns():
	return [
		{
			'label': _('ID'),
			'fieldname': 'name',
			'fieldtype': 'Link',
			'options':'Excel Project Tracking',
			'width': 120
		},
		{
			'label': _('Project Name'),
			'fieldname': 'project_name',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Doc Status'),
			'fieldname': 'docstatus',
			'fieldtype': 'Data',
			'width': 80
		},
		{
			'label': _('Start Date'),
			'fieldname': 'start_date',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Final Handover Date'),
			'fieldname': 'final_handover_date',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Final Invoice Submission'),
			'fieldname': 'final_invoice_submission_date',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Age (Days)'),
			'fieldname': 'ageing',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Customer Name'),
			'fieldname': 'customer_name',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Project Status'),
			'fieldname': 'project_status',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Project Category'),
			'fieldname': 'project_category',
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'label': _('SI Name'),
			'fieldname': 'si_name',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Project Incharge Sales'),
			'fieldname': 'project_incharge_sales',
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'label': _('Project Incharge Tech'),
			'fieldname': 'project_incharge_tech',
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'label': _('Linked Invoice'),
			'fieldname': 'invoice_no',
			'fieldtype': 'Data',
			'width': 120
		},
		{
			'label': _('Inv Date'),
			'fieldname': 'invoice_date',
			'fieldtype': 'Data',
			'width': 100
		},
				{
			'label': _('Inv Customer'),
			'fieldname': 'customer_name',
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'label': _('Inv Amount'),
			'fieldname': 'amount',
			'fieldtype': 'data',
			'width': 100
		},
	]	