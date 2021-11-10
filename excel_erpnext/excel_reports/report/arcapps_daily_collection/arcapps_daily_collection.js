// Copyright (c) 2016, Castlecraft Ecommerce Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["ArcApps Daily Collection"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": ("From Date"),
            "fieldtype": "Date",
            "default": get_today(),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": ("To Date"),
            "fieldtype": "Date",
            "default": get_today(),
            "reqd": 1
        },
        // {
        //     "fieldname": "excel_territory",
        //     "label": __("Territory"),
        //     "fieldtype": "Link",
        //     "options": "Territory",
        //     "default": frappe.defaults.get_user_default("Territory")
        // },
    ]
}



