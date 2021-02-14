// Copyright (c) 2016, Castlecraft Ecommerce Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Excel Purchase History"] = {
	"filters": [
	{
		"fieldname":"date_range",
		"label": __("Date Range"),
		"fieldtype": "DateRange",
		"default": [frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()],
		"reqd": 1
	},
	{
		"fieldname": "item_code",
		"label": __("Item"),
		"fieldtype": "Link",
		"options": "Item",
	},
	{
		"fieldname":"supplier",
		"label": __("Supplier"),
		"fieldtype": "Link",
		"options": "Supplier"
	},
	{
		"fieldname":"excel_lc_no",
		"label": __("LC No"),
		"fieldtype": "Link",
		"options": "Excel LC No"
	},
	{
		"fieldname":"company",
		"label": __("Company"),
		"fieldtype": "Link",
		"options": "Company",
		"hidden": 1,
		"default": frappe.defaults.get_user_default("Company")
	},
	{
		"label": __("Group By"),
		"fieldname": "group_by",
		"fieldtype": "Select",
		"options": ["Supplier", "Item Group", "Item", "Invoice"],
	}
],
"formatter": function(value, row, column, data, default_formatter) {
	value = default_formatter(value, row, column, data);
	if (data && data.bold) {
		value = value.bold();

	}
	return value;
}
}