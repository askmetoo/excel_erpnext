# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _, scrub
from frappe.utils import getdate, nowdate
from six import iteritems, itervalues
from erpnext.accounts.report.accounts_receivable.accounts_receivable import ReceivablePayableReport

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	return columns, data,None, chart

def get_columns():
	columns = [
                        {
                                "label": (""),
                                "fieldname": "name",
                                "fieldtype": "Data",
                                "width": 150
                        },
			{
                                "label": (""),
                                "fieldname": "value",
                                "fieldtype": "Currency",
                                "options": "Currency",
                                "width": 150
                        },
        ]

	return columns

def get_data(filters=None):
	data = []
	net_sales_condition = net_sales_conditions(filters)
	net_sales = frappe.db.sql(""" SELECT
		SUM(sit.amount)
		FROM `tabSales Invoice` AS si,`tabSales Invoice Item` AS sit
		where {net_sales_condition}
		""".format(net_sales_condition=net_sales_condition))
	row = {
                "name": "Net Sales",
                "value": net_sales[0][0],
        }
	data.append(row)

	whole_net_sales_condition = whole_net_sales_conditions(filters)
	whole_net_sales = frappe.db.sql(""" SELECT Distinct
                SUM(sit.amount)
                FROM `tabSales Invoice` AS si,`tabSales Invoice Item` AS sit
                where {whole_net_sales_condition}
                """.format(whole_net_sales_condition=whole_net_sales_condition))

#	frappe.msgprint(str(whole_net_sales))

	whole_collection_amount = frappe.db.sql(""" SELECT
                                sum(unallocated_amount)
                                FROM `tabPayment Entry`
                                where docstatus = 1 and posting_date <= %s and payment_type = "Receive"
                                """,(filters.get('to_date')))

#	frappe.msgprint(str(whole_collection_amount[0][0]))
	collection_condition,customer = collection_conditions(filters)
	collection = 0
	if customer:
		for i in customer:
			collection_amount = frappe.db.sql(""" SELECT
                                sum(paid_amount)
                                FROM `tabPayment Entry`
                                where docstatus = 1 and posting_date >= %s and posting_date <= %s and party = %s and excel_tax_payment = "No" and payment_type = "Receive"
                                """,(filters.get('from_date'),filters.get('to_date'),str(i['name'])))
			if collection_amount[0][0]:
				collection += collection_amount[0][0]
#                               total_collection += collection_amount[0][0]

	else:
		collection_amount = frappe.db.sql(""" SELECT
                                sum(paid_amount)
                                FROM `tabPayment Entry`
                                where docstatus = 1 and posting_date >= %s and posting_date <= %s and excel_tax_payment = "No" and payment_type = "Receive"
                                """,(filters.get('from_date'),filters.get('to_date')))
		collection  = collection_amount[0][0]
	row = {
                "name": "Collection",
                "value": collection,
        }
	data.append(row)

	debit = 0
	credit = 0
	if filters.get('customer_group') or filters.get('territory'):
#		customer = frappe.db.sql("""select name as name from `tabCustomer` where customer_group = %s""",(filters.get('customer_group')),as_dict = 1)
		for i in customer:
			gl_entries = frappe.db.sql("""
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
                        ,(i['name'],filters.get('to_date')),as_dict = 1)
			for j in gl_entries:
				if j['debit']:
					debit += j['debit']
				if j['credit']:
					credit += j['credit']
		receivable = debit - credit

	else:
		gl_entries = frappe.db.sql("""
			select
				name as name, posting_date as posting_date, account as account, party_type as party_type, party as party, voucher_type as voucher_type, voucher_no as voucher_no,
				against_voucher_type as against_voucher_type, against_voucher as against_voucher, account_currency as account_currency, remarks as remarks, sum(debit) as debit, sum(credit) as credit
			from
				`tabGL Entry`
			where
				docstatus < 2
				and party_type="Customer"
				and (party is not null and party != '')
				and posting_date <= %s
				order by posting_date, party"""
			,(filters.get('to_date')),as_dict = 1)
		for k in gl_entries:
			if k['debit']:
				debit += k['debit']
			if k['credit']:
				credit += k['credit']
		receivable = debit - credit


	debits = 0
	credits = 0
	if filters.get('supplier_group'):
		customer = frappe.db.sql("""select name as name from `tabSupplier` where supplier_group = %s""",(filters.get('supplier_group')),as_dict = 1)
		for i in customer:
#			frappe.msgprint(str(i['name']))
			gl_entries = frappe.db.sql("""
                        select
                                name as name, posting_date as posting_date, account as account, party_type as party_type, party as party, voucher_type as voucher_type, voucher_no as voucher_no,
                                against_voucher_type as against_voucher_type, against_voucher as against_voucher, account_currency as account_currency, remarks as remarks, sum(debit) as debit, sum(credit) as credit
                        from
                                `tabGL Entry`
                        where
                                docstatus < 2
                                and party_type="Supplier"
                                and (party = %s)
                                and posting_date <= %s
                                order by posting_date, party"""
                        ,(i['name'],filters.get('to_date')),as_dict = 1)
			for j in gl_entries:
#				frappe.throw(str(j))
				if j['debit']:
					debits += j['debit']
				if j['credit']:
					credits += j['credit']
		payables = credits - debits

	else:
		gl_entries = frappe.db.sql("""
                        select
                                name as name, posting_date as posting_date, account as account, party_type as party_type, party as party, voucher_type as voucher_type, voucher_no as voucher_no,
                                against_voucher_type as against_voucher_type, against_voucher as against_voucher, account_currency as account_currency, remarks as remarks, sum(debit) as debit, sum(credit) as credit
                        from
                                `tabGL Entry`
                        where
                                docstatus < 2
                                and party_type="Supplier"
                                and (party is not null and party != '')
                                and posting_date <= %s
                                order by posting_date, party"""
                        ,(filters.get('to_date')),as_dict = 1)
		for k in gl_entries:
			debits += k['debit']
			credits += k['credit']
		payables = credits - debits
	row = {
                "name": "Total Account Receivable",
                "value": receivable,
	}
	data.append(row)

	payable_condition = payable_conditions(filters)
	payable = frappe.db.sql(""" SELECT
                SUM(outstanding_amount)
                FROM `tabPurchase Invoice`
                where {payable_condition}
                """.format(payable_condition=payable_condition))
	row = {
                "name": "Total Account Payable",
                "value": payables,
	}
	data.append(row)

	return data 

def net_sales_conditions(filters):
	conditions = ""

	conditions += "si.docstatus = 1 and si.name = sit.parent"
	if filters.get("from_date"): conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
	if filters.get("to_date"): conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
	if filters.get("customer_group"): conditions += " and si.customer_group = '%s' " %filters.get('customer_group')
	if filters.get("territory"): conditions += " and si.territory = '%s' " %filters.get("territory")
	net_sales_conditions = conditions

	return net_sales_conditions

def whole_net_sales_conditions(filters):
	conditions = ""

	conditions += "si.docstatus = 1 and si.name = sit.parent"
#        if filters.get("from_date"): conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
	if filters.get("to_date"): conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
	if filters.get("customer_group"): conditions += " and si.customer_group = '%s' " %filters.get('customer_group')
	if filters.get("territory"): conditions += " and si.territory = '%s' " %filters.get("territory")
	whole_net_sales_conditions = conditions

	return whole_net_sales_conditions

def collection_conditions(filters):
	conditions = ""
	customer= []
	conditions += "docstatus = 1 and excel_tax_payment = 'No' and payment_type = 'Receive' "
	if filters.get("customer_group") and filters.get("territory"):
		customer = frappe.db.sql(""" SELECT
                name
                FROM `tabCustomer`
                where customer_group = %s and territory = %s
                """,(filters.get('customer_group'),filters.get('territory')),as_dict = 1)

	elif filters.get("customer_group"):
		customer = frappe.db.sql(""" SELECT
                name
                FROM `tabCustomer`
                where customer_group = %s
                """,(filters.get('customer_group')),as_dict = 1)

	elif filters.get("territory"):
                customer = frappe.db.sql(""" SELECT
                name
                FROM `tabCustomer`
                where territory = %s
                """,(filters.get('territory')),as_dict = 1)

	if filters.get("from_date"): conditions += " and posting_date >= '%s' " % filters.get("from_date")
	if filters.get("to_date"): conditions += " and posting_date <= '%s' " % filters.get("to_date")
	collection_conditions = conditions

	return collection_conditions,customer

def receivable_conditions(filters):
	conditions = ""

	conditions += "docstatus = 1 "
	if filters.get("to_date"): conditions += " and posting_date <= '%s' " % filters.get("to_date")
	if filters.get("customer_group"): conditions += " and customer_group = '%s' " %filters.get('customer_group')
	if filters.get("territory"): conditions += " and territory = '%s' " %filters.get("territory")
	receivable_conditions = conditions

	return receivable_conditions

def payable_conditions(filters):
        conditions = ""

        conditions += "docstatus = 1  "
        if filters.get("to_date"): conditions += " and posting_date <= '%s' " % filters.get("to_date")
#        if filters.get("customer_group"): conditions += " and customer_group = '%s' " %filters.get('customer_group')
#        if filters.get("territory"): conditions += " and territory = '%s' " %filters.get("territory")
        payable_conditions = conditions

        return payable_conditions

def get_chart_data(data):
	brands = []
	datasets = []
	for i in data:
		if i['name']:
			brands.append(i['name'])
			datasets.append(i['value'])
	chart = {
                "data": {
                        'labels': brands,
                        'datasets': [
                                {"name" : "Net Sales",'values': datasets},
                        ]
                }
        }
	chart["type"] = "bar"
	chart["colors"] = ['#6495ED','#FF5733','#BAB6B5','#F1F104']
	return chart

