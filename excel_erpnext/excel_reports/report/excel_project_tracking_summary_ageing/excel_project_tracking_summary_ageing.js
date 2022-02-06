// Copyright (c) 2016, Castlecraft Ecommerce Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Excel Project Tracking Summary Ageing"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname": "project_name",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Excel Project Tracking"
		},
		{
			"fieldname": 'project_status',
			"label": __('Project Status'),
			"fieldtype": 'Select',
			"options": ["", "Work in Progress", "Completed", "Pending"]
		},
		{
			"fieldname": 'docstatus',
			"label": __('Doc Status'),
			"fieldtype": 'Select',
			"options": ["", "Draft", "Submitted", "Cancelled"]
		},
	]
};