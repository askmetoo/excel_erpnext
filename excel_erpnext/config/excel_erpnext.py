from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("IoU and Claims"),
			"icon": "fa fa-cog",
			"items": [
				{
					"label": "IoU (Employee Advance)",
					"type": "doctype",
					"name": "Employee Advance"
				},
				{
					"label": "Conveyances (Expense Claim)",
					"type": "doctype",
					"name": "Expense Claim"
				},
				{
					"type": "report",
					"name": "Employee Advance Summary",
					"doctype": "Employee Advance",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Accounting Dimensions"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Excel LC No"
				},
				{
					"type": "doctype",
					"name": "Excel Long Term Loans"
				},
				{
					"type": "doctype",
					"name": "Excel Office Locations"
				},
				{
					"type": "doctype",
					"name": "Excel Other Loans and Advances"
				},
				{
					"type": "doctype",
					"name": "Excel Product Team"
				},
				{
					"type": "doctype",
					"name": "Excel Securities Deposits and Prepayment"
				},
				{
					"type": "doctype",
					"name": "Excel Short Term Investments"
				},
				{
					"type": "doctype",
					"name": "Excel Short Term Loan"
				},
				{
					"type": "doctype",
					"name": "Excel Dream Project"
				},
				{
					"type": "doctype",
					"name": "Excel Child Customers"
				},
			]
		},
		{
			"label": _("SCM"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Excel LC Costing"
				},
				{
					"type": "doctype",
					"name": "Excel LC Pipeline"
				},
				{
					"type": "doctype",
					"name": "Excel LC Details"
				},
				{		"type": "doctype",
						"name": "Excel SCM Brand List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Supplier and Shipper List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Transport and CnF List"
				},
				{		"type": "doctype",
						"name": "Excel SCM LC Opening Bank List"
				},
				{		"type": "doctype",
						"name": "Excel SCM CNEE List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Insurance Provider List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Freight Forwarder List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Destination List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Shipment Status List"
				},
				{		"type": "doctype",
						"name": "Excel SCM Shipment Mode List"
				},

			]
		},
		{
			"label": _("Corporate Project"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Excel Project Pre Costing"
				},
				
				{
					"type": "doctype",
					"name": "Excel Quotation"
				},
				{
					"type": "doctype",
					"name": "Excel MPS Counter"
				},				
			]
		},
		{
			"label": _("Support Team"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Excel Project Tracking"
				},
				{
					"type": "report",
					"name": "Excel Project Wise Ageing",
					"doctype": "Excel Project Tracking",
					"is_query_report": True,
				},
				{
					"type": "doctype",
					"name": "Excel Daily Task"
				},
				{
					"type": "doctype",
					"name": "Issue"
				},
				{
					"type": "doctype",
					"name": "Task"
				},				
			]
		},
	]