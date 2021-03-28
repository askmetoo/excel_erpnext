# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _, scrub
from frappe.utils import getdate, nowdate,flt
from six import iteritems, itervalues

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data,total_net_sales,total_collection = get_data(filters)
	chart = get_chart_data(data,total_net_sales,total_collection)
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
				"label": ("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 150
			},
			{
                                "label": ("Territory"),
                                "fieldname": "territory",
                                "fieldtype": "Link",
				"options": "Territory",
                                "width": 150
                        },
			{
                                "label": ("Customer"),
                                "fieldname": "customer_name",
                                "fieldtype": "Data",
                                "width": 150
                        },
			{
				"label": ("Total Collection"),
				"fieldname": "total_collection",
				"fieldtype": "Currency",
				"options": "currency",
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
				"label": ("Total Outstanding"),
				"fieldname": "total_outstanding",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150
			},
			{
				"label": ("Sales-Collection Ratio"),
				"fieldname": "sales_collection",
				"fieldtype": "Float",
				"width": 100
			},
			{
				"label": ("Outstanding-Collection Ratio"),
				"fieldname": "outstanding_collection",
				"fieldtype": "Float",
				"width": 100
			},
	]
	return columns
def get_data(filters=None):
	data = []
	conditions = get_conditions(filters)
	gl_entries = frappe.db.sql("""
			SELECT
				si.total AS net_sales,
				si.customer as customer,
				si.customer_name as customer_name,
				si.outstanding_amount AS total_outstanding
			FROM
				`tabSales Invoice` AS si,`tabSales Team` AS st ,`tabSales Invoice Item` AS sit
			WHERE
				{conditions}
			""".format(conditions=conditions),as_dict=1)
	total_net_sales = total_collection = 0.0
	rank = 0
	customers = []
	dataset = []
	for record in gl_entries:
		if record.customer:
                        customers.append(record.customer)

	res = []
	[res.append(x) for x in customers if x not in res]
	collection = 0
	collections = 0

	for customer in res:
		debit = 0
		credit = 0
		rank = rank + 1
		net_sales = sum(i.net_sales for i in gl_entries if i.customer == customer)
		gl_entrie = frappe.db.sql("""
                        select
                                name as name, posting_date as posting_date, account as account, party_type as party_type, party as party, voucher_type as voucher_type, voucher_no as voucher_no,
                                against_voucher_type as against_voucher_type, against_voucher as against_voucher, account_currency as account_currency, remarks as remarks, sum(debit) as debit, sum(credit) as credit
                        from
                                `tabGL Entry`
                        where
                                docstatus < 2
                                and party_type="Customer"
                                and (party = %s)
                                and posting_date <= %s
                                order by posting_date, party"""
                        ,(customer,filters.get('to_date')),as_dict = 1)
		for j in gl_entrie:
			if j['debit']:
				debit += j['debit']
			if j['credit']:
				credit += j['credit']
		collection_amount = frappe.db.sql(""" SELECT
                                sum(paid_amount)
                                FROM `tabPayment Entry`
                                where docstatus = 1 and posting_date >= %s and posting_date <= %s and party = %s and excel_tax_payment = "No" and party_type = "Customer"
                                """,(filters.get('from_date'),filters.get('to_date'),customer))
		if collection_amount[0][0]:
			collection = collection_amount[0][0]
#                               total_collection += collection_amount[0][0]
		outstanding = debit - credit

		total_net_sales += flt(net_sales,2)
		if not outstanding == 0:
			row = {
					"rank": rank,
					"territory": frappe.db.get_value("Customer",customer,"territory"),
					"net_sales": net_sales,
					"total_collection": collection,
					"total_outstanding": outstanding,
					"sales_collection": (net_sales/collection) * 100 if collection > 0 else 0 ,
					"outstanding_collection": (net_sales/outstanding) * 100,
					"customer": customer,
					"customer_name":frappe.db.get_value("Customer",customer,"customer_name")
				}
		else:
			row = {
					"rank": rank,
					"net_sales": net_sales,
					"territory": frappe.db.get_value("Customer",customer,"territory"),
					"total_collection": collection,
					"total_outstanding": outstanding,
					"sales_collection": 0,
					"outstanding_collection": 0,
					"customer": customer,
					"customer_name":frappe.db.get_value("Customer",customer,"customer_name")
			}

		data.append(row)
		collection = 0
	data.sort(key=lambda x: x.get('total_collection'), reverse=True)
	rank = 0
	for i in data:
		rank = rank + 1
		i['rank'] = rank
	return data ,flt(total_net_sales),total_collection

def get_conditions(filters):
	conditions = ""

	conditions += "si.docstatus = 1 and si.name = st.parent and si.name = sit.parent"
	if filters.get("from_date"): conditions += " and si.posting_date >= '%s'" % filters.get("from_date")
	if filters.get("to_date"): conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
	if filters.get("territory"): conditions += " and si.territory = '%s' " %filters.get("territory")
	if filters.get("salesperson"): conditions += " and st.sales_person = '%s' " %filters.get("salesperson")
	if filters.get("brand"): conditions += " and sit.brand = '%s' " %filters.get("brand")
	if filters.get("customer_group"): conditions += " and si.category = '%s' " %filters.get("customer_group")

	return conditions

def get_chart_data(data ,total_net_sales,total_collection):
	brands = []
	net_sales = []
	collection = []
	outstanding = []
	for i in data:
		if i['customer'] and i['rank'] <= 10:
			brands.append(i['customer'])
			collection.append(i['total_collection'])
			net_sales.append(i['net_sales'])
			outstanding.append(i['total_outstanding'])
	chart = {
		"data": {
			'labels': brands,
			'datasets': [
                                {"name" : "Total Collection",'values': collection},
				{"name" : "Net Sales",'values': net_sales},
                                {"name" : "Total Outstanding",'values': outstanding}
                        ]
		}
	}
	chart["type"] = "bar"
	chart["colors"] = ['#6495ED','#D2691E']
	return chart

