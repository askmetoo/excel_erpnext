from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Dimension Docs"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "ArcApps LC No"
				},
				{
					"type": "doctype",
					"name": "ArcApps Long Term Loans"
				},
				{
					"type": "doctype",
					"name": "ArcApps Office Locations"
				},
				{
					"type": "doctype",
					"name": "ArcApps Other Loans and Advances"
				},
				{
					"type": "doctype",
					"name": "ArcApps Product Team"
				},
				{
					"type": "doctype",
					"name": "ArcApps Securities Deposits and Prepayment"
				},
				{
					"type": "doctype",
					"name": "ArcApps Short Term Investments"
				},
				{
					"type": "doctype",
					"name": "ArcApps Short Term Loan"
				},
				{
					"type": "doctype",
					"name": "ArcApps Dream Project"
				},
				{
					"type": "doctype",
					"name": "ArcApps Child Customers"
				},
			]
		},
		{
			"label": _("Company Reports"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "report",
					"name": "ArcApps Company Performance Summary",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},				
				{
					"type": "report",
					"name": "ArcApps Territory Performance",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Customer Group Performance",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},				
				{
					"type": "report",
					"name": "ArcApps Gross Profit By Costing",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Accounting Reports"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "report",
					"name": "ArcApps Account Wise Ledger",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Gross Profit by Costing",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Customer Ranking By Collection",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
					{
					"type": "report",
					"name": "ArcApps Customer Ranking By Sales",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Cheque in Hand",
					"doctype": "Payment Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Daily Collection",
					"doctype": "Payment Entry",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Sales Person Reports"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "report",
					"name": "ArcApps Customer Ledger",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Sales Person Ranking By Collection",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Sales Person Ranking By Sales",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Product Reports"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "report",
					"name": "ArcApps Brand Performance Summary",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Brand Wise Sales Analysis",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Product Performance Analysis",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Top Fifty Sold Items",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Stock Balance",
					"doctype": "Stock Ledger Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Product Ledger",
					"doctype": "Stock Ledger Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "ArcApps Purchase History",
					"doctype": "Purchase Invoice",
					"is_query_report": True,
				},
			]
		},
		# {
		# 	"label": _("SCM Reports"),
		# 	"icon": "fa fa-cog",
		# 	"items": [
		# 		{
		# 			"type": "report",
		# 			"name": "ArcApps LC Pipeline Status",
		# 			"doctype": "ArcApps LC Pipeline",
		# 			"is_query_report": True,
		# 			"is_hidden":1
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "ArcApps LC Pipeline Summary",
		# 			"doctype": "ArcApps LC Pipeline",
		# 			"is_query_report": True,
		# 			"is_hidden":1
		# 		},
		# 	]
		# },
	]