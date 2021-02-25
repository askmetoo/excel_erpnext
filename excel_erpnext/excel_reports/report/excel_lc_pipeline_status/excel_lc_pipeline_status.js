// Copyright (c) 2016, Castlecraft Ecommerce Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Excel LC Pipeline Status"] = {
	"filters": [
		{
			"fieldname":"pipeline_status",
			"label": __("Pipeline Status"),
			"fieldtype": "Select",
			"options": "Complete\nIn Progress",
            "default": "Complete"
		},
	]
}
