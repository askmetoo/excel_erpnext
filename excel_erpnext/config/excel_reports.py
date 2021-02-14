from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Company Reports"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "report",
					"name": "Excel Company Performance Summary",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},				
				{
					"type": "report",
					"name": "Excel Territory Performance",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Customer Group Performance",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},				
				{
					"type": "report",
					"name": "Excel Gross Profit By Costing",
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
					"name": "Excel Account Wise Ledger",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Gross Profit by Costing",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Customer Ranking By Collection",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
					{
					"type": "report",
					"name": "Excel Customer Ranking By Sales",
					"doctype": "Sales Invoice",
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
					"name": "Excel Customer Ledger",
					"doctype": "GL Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Sales Person Ranking By Collection",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Sales Person Ranking By Sales",
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
					"name": "Excel Brand Performance Summary",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Brand Wise Sales Analysis",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Product Performance Analysis",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Top Fifty Sold Items",
					"doctype": "Sales Invoice",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Stock Balance",
					"doctype": "Stock Ledger Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Product Ledger",
					"doctype": "Stock Ledger Entry",
					"is_query_report": True,
				},
				{
					"type": "report",
					"name": "Excel Purchase History",
					"doctype": "Purchase Invoice",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("SCM Reports"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "report",
					"name": "Excel LC Pipeline Status",
					"doctype": "Excel LC Pipeline",
					"is_query_report": True,
				},
			]
		},
	]
