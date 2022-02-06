// Copyright (c) 2016, Castlecraft Ecommerce Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Excel Warranty Claim Analysis"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
			width: "60px"
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
			width: "60px"
		},
		{
			fieldname: "territory",
			label: __("Territory"),
			fieldtype: "Link",
			width: "80",
			options: "Territory",
		},
		{
			fieldname: "claim_item",
			label: __("Claim Item"),
			fieldtype: "link",
			options: "Item",
		},
		{
			fieldname: "claim_type",
			label: __("Claim Type"),
			fieldtype: "Select",
			width: "80",
			options: "\nWarranty\nNon Warranty\nThird Party Warranty\nNon Serial Warranty",
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			width: "80",
			options: "Brand",
		},
		{
			fieldname: "claim_status",
			label: __("Claim Status"),
			fieldtype: "Select",
			options: "\nIn Progress\nTo Deliver\nDelivered\nRejected\nAll",
		},
		{
			fieldname: "replaced_item",
			label: __("Replaced Item"),
			fieldtype: "link",
			options: "Item",
		},
		{
			fieldname: "delivery_status",
			label: __("Delivery Status"),
			fieldtype: "Select",
			options: "\nRepaired\nReplaced\nUpgraded\nRejected",
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			width: "80",
			options: "Customer",
		},
		{
			fieldname: "third_party_name",
			label: __("Third Party Name"),
			fieldtype: "Data"
		},
		{
			fieldname: "thrid_party_mobile",
			label: __("Thrid Party Mobile"),
			fieldtype: "Data"
		},
		{
			fieldname: "price_list",
			label: __("Price List"),
			fieldtype: "Link",
			width: "80",
			options: "Price List",
			default: "Standard Selling",
			reqd: 1
		},
	]
};
