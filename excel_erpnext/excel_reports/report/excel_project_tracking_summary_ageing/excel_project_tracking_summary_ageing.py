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
		conditions +=" start_date >= '{}' ".format(filters.get("from_date"))

	if filters.get("to_date"):
		conditions +="AND start_date <= '{}' ".format(filters.get("to_date"))

	if filters.get("project_name"):
		conditions +=" AND name = '{}' ".format(filters.get("project_name"))

	if filters.get("project_status"):
		conditions +=" AND project_status = '{}' ".format(filters.get("project_status"))	

	if filters.get("docstatus"):
		if filters.get("docstatus") == "Draft":
			conditions +=" AND docstatus = 0 "
		elif filters.get("docstatus") == "Submitted":
			conditions +=" AND docstatus = 1 "
		elif filters.get("docstatus") == "Cancelled":
			conditions +=" AND docstatus = 2 "
			
	return frappe.db.sql(
		f"""
		SELECT
			name as id, 
			(case when docstatus=0 then 'Draft'
             when docstatus=1 then 'Submitted'
             else 'Cancelled'
             end) as docstatus, project_name, project_status, start_date, expected_handover_date,
			customer_name, customer_address, customer_contact_person, si_name, customer_mobile, project_category, 
			final_invoice_submission_date, final_handover_date, final_invoice_submitted_by, project_incharge_sales, 
			project_incharge_tech, TIMESTAMPDIFF(DAY, final_invoice_submission_date, "{filters.get("to_date")}") as ageing 
		FROM  `tabExcel Project Tracking Summary` WHERE {conditions}
		""",as_dict=1)

def get_columns():
	return [
		{
			'label': _('ID'),
			'fieldname': 'id',
			'fieldtype': 'Link',
			'options':'Excel Project Tracking Summary',
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
			'width': 120
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
	]	