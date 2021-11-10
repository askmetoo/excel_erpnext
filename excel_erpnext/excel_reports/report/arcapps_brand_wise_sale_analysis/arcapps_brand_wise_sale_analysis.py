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
	data = get_data(filters)
	brand_result = get_brand(filters)
	brands = []
	if brand_result:
		for brand in brand_result:
			brands.append(brand)
	chart = get_chart_data(brands,data)
	return columns, data,None, chart

def get_columns():
	columns = [
			{
				"label": ("Territory"),
				"fieldname": "territory",
				"fieldtype": "Link",
				"options": "Territory",
				"width": 100
			},
			{
				"label": ("Customer Group"),
				"fieldname": "customer_group",
				"fieldtype": "Link",
				"options": "Customer Group",
				"width": 150
			},
			{
				"label": ("Salesperson"),
				"fieldname": "sales_person",
				"fieldtype": "Link",
				"options": "Sales Person",
				"width": 150
			},
			{
				"label": ("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 200
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
				"width": 200
			}
		]

	return columns

def get_brand(filters= None):
	return frappe.db.sql("""select name from `tabBrand` """,as_list=1)

def get_data(filters=None):
	out = []
	conditions = get_conditions(filters)
	gl_entries = frappe.db.sql("""
			select
				si.territory as territory,si.customer_group as customer_group,st.sales_person as sales_person,si.customer as customer,sit.brand as brand,sum(sit.amount) as net_sales
			from `tabSales Invoice` si, `tabSales Team` st,`tabSales Invoice Item` sit
			where
			{conditions}
			group by sit.brand
			""".format(conditions=conditions),as_dict=1)

	return gl_entries

def get_conditions(filters):
	conditions = ""

	conditions += "si.docstatus < 2 and si.name = st.parent and si.name = sit.parent"
	if filters.get("from_date"): conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
	if filters.get("to_date"): conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
	if filters.get("customer"): conditions += " and si.customer = '%s' " % filters.get('customer')
	if filters.get("brand"): conditions += " and sit.brand = '%s ' " %filters.get("brand")
	if filters.get("customer_group"): conditions += " and si.customer_group = '%s' " %filters.get("customer_group")
	if filters.get("sales_person"): conditions += " and st.sales_person = '%s' " %filters.get("sales_person")
	if filters.get("territory"): conditions += " and si.territory = '%s' " %filters.get("territory")

	return conditions

def get_chart_data(brands,data):
	brands = []
	datasets = []
	for i in data:
		if i['brand']:
			brands.append(i['brand'])
	res = [] 
	products = []
	[res.append(x) for x in brands if x not in res]
	i = 1
	for brand in res:
		if brand and i <= 20:
			total_sales = sum(i['net_sales'] for i in data if i['brand'] == brand)
			datasets.append(total_sales)
			products.append(brand)
			i = i +1
	chart = {
		"data": {
			'labels': products,
			'datasets': [{'name': 'Brands' ,'values': datasets}]
		}
	}
	chart["type"] = "bar"
	return chart
