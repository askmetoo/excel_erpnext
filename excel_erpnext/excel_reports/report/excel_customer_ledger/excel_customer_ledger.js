// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Excel Customer Ledger"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1,
			"hidden": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
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
			"fieldname": "excel_territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory",
			"width": "60px"
		},
		{
			"fieldtype": "Break",
		},
		{
			"fieldname": "party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "Party Type",
			"default": "Customer",
			"hidden": 1,
			on_change: function () {
				frappe.query_report.set_filter_value('party', "");
			}
		},
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "MultiSelectList",
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value('party_type');
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
			on_change: function () {
				var party_type = frappe.query_report.get_filter_value('party_type');
				var parties = frappe.query_report.get_filter_value('party');

				if (!party_type || parties.length === 0 || parties.length > 1) {
					frappe.query_report.set_filter_value('party_name', "");
					frappe.query_report.set_filter_value('tax_id', "");
					return;
				} else {
					var party = parties[0];
					var fieldname = erpnext.utils.get_party_name(party_type) || "name";
					frappe.db.get_value(party_type, party, fieldname, function (value) {
						frappe.query_report.set_filter_value('party_name', value[fieldname]);
					});

					if (party_type === "Customer" || party_type === "Supplier") {
						frappe.db.get_value(party_type, party, "tax_id", function (value) {
							frappe.query_report.set_filter_value('tax_id', value["tax_id"]);
						});
					}
				}
			}
		},

		{
			"fieldname": "party_name",
			"label": __("Party Name"),
			"fieldtype": "Data",
			"hidden": 0,
			"read_only": 1,
		},
		{
			"fieldname": "group_by",
			"label": __("Group by"),
			"fieldtype": "Select",
			"options": ["", __("Group by Voucher"), __("Group by Voucher (Consolidated)"),
				__("Group by Account"), __("Group by Party")],
			"default": __("Group by Voucher (Consolidated)"),
			"hidden": 1
		},
		{
			"fieldname": "presentation_currency",
			"label": __("Currency"),
			"fieldtype": "Select",
			"options": erpnext.get_presentation_currency_list(),
			"hidden": 1
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "MultiSelectList",
			"hidden": 1,
			get_data: function (txt) {
				return frappe.db.get_link_options('Cost Center', txt);
			}
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			"hidden": 1,
			get_data: function (txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
	]
}

erpnext.dimension_filters.forEach((dimension) => {
	frappe.query_reports["Excel Customer Ledger"].filters.splice(15, 0, {
		"fieldname": dimension["fieldname"],
		"label": __(dimension["label"]),
		"fieldtype": "Link",
		"options": dimension["document_type"]
	});
});
