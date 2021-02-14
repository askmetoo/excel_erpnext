# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _, scrub
from frappe.utils import getdate, nowdate
from six import iteritems, itervalues

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data,total_brand_contribution = get_data(filters)
	chart = get_chart_data(data,total_brand_contribution)
	return columns, data,None, chart

def get_columns():
	columns = [
                        {
                                "label": ("Rank"),
                                "fieldname": "rank",
                                "fieldtype": "int",
                                "width": 50
                        },
                        {
                                "label": ("Brand"),
                                "fieldname": "brand",
                                "fieldtype": "Link",
                                "options": "Brand",
                                "width": 150
                        },
                        {
                                "label": ("Net Sales"),
                                "fieldname": "net_sales",
                                "fieldtype": "Currency",
                                "options": "currency",
                                "width": 150
                        },
                        {
                                "label": ("Brand Contribution"),
                                "fieldname": "brand_contribution",
                                "fieldtype": "Float",
                                "width": 100
                        }
#			{
#                                "label": ("Sales Invoice"),
#                                "fieldname": "name",
#                                "fieldtype": "Link",
#                                "options": "Sales Invoice",
#                                "width": 150
#                        },
	]

	return columns

def get_data(filters=None):
	data = []
	conditions = get_conditions(filters)
	gl_entries = frappe.db.sql("""
                        SELECT Distinct
                                sit.brand AS brand,
                                sum(sit.amount) AS net_sales,
				st.sales_person as salesperson,
				si.name as name
                        FROM
                                `tabSales Invoice` AS si,`tabSales Invoice Item` AS sit, `tabSales Team` AS st
                        WHERE
                                {conditions}
			GROUP BY
                               sit.brand
			ORDER BY sum(sit.amount) DESC
                        """.format(conditions=conditions),as_dict=1)
#			st.sales_person as salesperson
#			GROUP BY
 #                               sit.brand
  #                      ORDER BY sum(sit.amount) DESC
#			ORDER BY sum(si.rounded_total) DESC
#			 GROUP BY
#                                sit.brand


	total_brand_contribution = 0.0
	rank = 0
	for record in gl_entries:
#		if record.brand:
		total_brand_contribution += record.net_sales

	for record in gl_entries:
		rank = rank + 1
		row = {
                        "rank": rank,
                        "brand": record.brand,
                        "net_sales": record.net_sales,
                        "brand_contribution": (record.net_sales/total_brand_contribution) * 100
#			"name": record.name
		}
		data.append(row)
	return data ,total_brand_contribution

def get_conditions(filters):
	conditions = ""

	conditions += "si.docstatus = 1 and si.name = st.parent and si.name = sit.parent"
	if filters.get("from_date"): conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
	if filters.get("to_date"): conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
	if filters.get("customer_group"): conditions += " and si.customer_group = '%s' " %filters.get('customer_group')
	if filters.get("territory"): conditions += " and si.territory = '%s' " %filters.get("territory")
	if filters.get("salesperson"): conditions += " and st.sales_person = '%s' " %filters.get("salesperson")

	return conditions

def get_chart_data(data ,total_brand_contribution):
	brands = []
	datasets = []
	j = 1
	for i in data:
		if i['brand'] and j <= 20:
			brands.append(i['brand'])
			datasets.append(i['net_sales'])
			j = j +1
	chart = {
                "data": {
                        'labels': brands,
                        'datasets': [
                                {"name" : "Net Sales",'values': datasets},
                        ]
                }
	}
	chart["type"] = "bar"
#	chart["colors"] = ['#6495ED']
	return chart
