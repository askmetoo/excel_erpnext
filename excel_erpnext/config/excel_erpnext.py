from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
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
					"name": "Excel Product Teams"
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
			]
		},
		{
			"label": _("Commercials"),
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
			]
		},
	]