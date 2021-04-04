# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "excel_erpnext"
app_title = "Excel ERPNext"
app_publisher = "Castlecraft Ecommerce Pvt. Ltd."
app_description = "Extensions for Excel Technologies"
app_icon = "fa fa-cloud"
app_color = "grey"
app_email = "support@castlecraft.in"
app_license = "AGPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/excel_erpnext/css/excel_erpnext.css"
app_include_js = "/assets/excel_erpnext/js/excel_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/excel_erpnext/css/excel_erpnext.css"
# web_include_js = "/assets/excel_erpnext/js/excel_erpnext.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Excel Project Pre Costing" : "public/js/excel_project_pre_costing.js", 
    "Excel LC Details" : "public/js/excel_lc_details.js", 
    "Excel LC Costing" : "public/js/excel_lc_costing.js", 
    "Excel LC No" : "public/js/excel_lc_no.js",
    "Excel MPS Counter" : "public/js/excel_mps_counter.js",
    "Excel LC Pipeline" : "public/js/excel_lc_pipeline.js" 
    }
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "excel_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "excel_erpnext.install.before_install"
# after_install = "excel_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "excel_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "hourly_long": ["excel_erpnext.schedules.purchase.process_purchase_orders"]
}

# scheduler_events = {
# 	"all": [
# 		"excel_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"excel_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"excel_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"excel_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"excel_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "excel_erpnext.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "excel_erpnext.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "excel_erpnext.task.get_dashboard_data"
# }

fixtures = [
	{
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Delivery Note Item-excel_serials",
                    "Customer-excel_customer_bin_id",
                    "Customer-excel_customer_trade_license",
                    "Customer-excel_customer_nid",
                    "Customer-excel_security_cheque_amount",
                    "Customer-excel_customer_tin_id",
                    "Customer-excel_customer_owner_name",
                    "Customer-excel_customer_owner_farther_name",
                    "Customer-excel_customer_owner_permanent_address",
                    "Item-has_excel_serials",
                    "Stock Entry Detail-excel_serials",
                    "Payment Entry-excel_tax_payment",
                    "Payment Entry-excel_territory",
                    "Journal Entry-excel_territory",
                    "Journal Entry Account-excel_party_name",
                    "Stock Entry-excel_territory",
                    "Bin-excel_item_name",
                    "Bin-excel_item_brand",
                    "Bin-excel_item_group",
                    "Purchase Order-excel_actual_supplier",
                    "Purchase Order-excel_actual_supplier_name",
                    "Purchase Order-excel_lc_no",
                    "Purchase Order-excel_lc_date",
                    "Purchase Order-excel_pi_no",
                    "Purchase Order-excel_pi_date",
                    "Purchase Order-excel_excel_supplier_invoice_date", 
                    "Purchase Order-excel_remarks", 
                    "Purchase Order-excel_supplier_invoice_no",
                    "Purchase Invoice-excel_actual_supplier",
                    "Purchase Invoice-excel_actual_supplier_name",
                    "Purchase Invoice-excel_supplier_invoice_no",
                    "Purchase Invoice-excel_excel_supplier_invoice_date",
                    "Purchase Invoice-excel_remarks",                     
                    "Purchase Invoice-excel_lc_no",
                    "Purchase Invoice-excel_lc_date",
                    "Purchase Invoice-excel_pi_no",
                    "Purchase Invoice-excel_pi_date",
                    "Asset-excel_customer_name", 
                    "Asset-excel_asset_user",  
                    "Asset-project",
                    "Journal Entry-project",  
                    "Loan-project",  
                    "Purchase Order-project",  
                    "Employee Advance-project",                                          
                    "Asset-excel_device_model",  
                    "Asset-excel_device_serial", 
                    "Asset-excel_remarks", 
                    "Project-excel_mps_assetss",
                    "Project-excel_mps_project_assets", 
                    "Sales Invoice-excel_customer_name_for_mps_print",
                    "Stock Entry-excel_customer_name",
                    "Stock Entry-excel_customer_address",
                    "Stock Entry-excel_customer_contact",
                    "Stock Entry-excel_customer_mobile",                                                            
                ],
            ],
        ]
    },
]
