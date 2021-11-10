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
    data, total_net_sales, total_collection, total_receivable = get_data(filters)
    chart = get_chart_data(data)
    return columns, data, None, chart


def get_columns():
    columns = [
        {
            "label": ("Territory"),
            "fieldname": "territory",
            "fieldtype": "Link",
            "options": "Territory",
            "width": 100,
        },
        #                        {
        #                               "label": ("Customer Group"),
        #                              "fieldname": "customer_group",
        #                             "fieldtype": "Link",
        #                            "options": "Customer Group",
        #                           "width": 150
        #                  },
        {
            "label": ("Total Account Receivable"),
            "fieldname": "total_account_receivable",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "label": ("Net Sales"),
            "fieldname": "net_sales",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "label": ("Collection"),
            "fieldname": "collection",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "label": ("Sales Collection Ratio"),
            "fieldname": "sales_collection_ratio",
            "fieldtype": "Float",
            #                                "options": "integer",
            "width": 150,
        },
        {
            "label": ("Account Receivable Collection Ratio"),
            "fieldname": "account_receivable_collection_ratio",
            "fieldtype": "Float",
            #                                "options": "integer",
            "width": 100,
        },
        {
            "label": ("Sales Contribution in Company"),
            "fieldname": "sales_contribution",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": ("Collection Contribution in Company"),
            "fieldname": "collection_contribution",
            "fieldtype": "Float",
            "width": 100,
        },
    ]

    return columns


def get_data(filters=None):
    data = []
    conditions = get_conditions(filters)
    gl_entries = frappe.db.sql(
        """
			SELECT Distinct
				si.territory AS territory,
				si.customer_group AS customer_group,
				sum(sit.amount) AS net_sales,
				si.name AS name
			FROM
				`tabSales Invoice` AS si,`tabSales Invoice Item` as sit
			WHERE 
                        	{conditions}
			GROUP BY
                               si.territory
                        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )

    total_net_sales = total_collection = total_receivable = 0.0
    collection_amount = frappe.db.sql(
        """ SELECT
                                sum(paid_amount)
                                FROM `tabPayment Entry`
                                where docstatus = 1 and posting_date >= %s and posting_date <= %s and excel_tax_payment = "No" and party_type = "Customer"
                                """,
        (filters.get("from_date"), filters.get("to_date")),
    )
    if collection_amount[0][0]:
        total_collection += collection_amount[0][0]

    for record in gl_entries:
        if record.net_sales:
            total_net_sales += record.net_sales
        if record.total_account_receivable:
            total_receivable += record.total_account_receivable
    for record in gl_entries:
        debit = 0
        credit = 0
        collection = 0
        customer = frappe.db.sql(
            """select name as name from `tabCustomer` where territory = %s""",
            (record.territory),
            as_dict=1,
        )
        for i in customer:
            gl_entrie = frappe.db.sql(
                """
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
                                order by posting_date, party""",
                (i["name"], filters.get("to_date")),
                as_dict=1,
            )
            for j in gl_entrie:
                if j["debit"]:
                    debit += j["debit"]
                if j["credit"]:
                    credit += j["credit"]
            collection_amount = frappe.db.sql(
                """ SELECT
		                sum(paid_amount)
	        	        FROM `tabPayment Entry`
        	        	where docstatus = 1 and posting_date >= %s and posting_date <= %s and party = %s and excel_tax_payment = "No" and party_type = "Customer"
	                	""",
                (filters.get("from_date"), filters.get("to_date"), str(i["name"])),
            )
            if collection_amount[0][0]:
                collection += collection_amount[0][0]
        # 				total_collection += collection_amount[0][0]
        receivable = debit - credit

        row = {
            "territory": record.territory,
            "customer_group": record.customer_group,
            "total_account_receivable": receivable,
            "net_sales": record.net_sales,
            "collection": collection,
            "sales_collection_ratio": collection / record.net_sales,
            "account_receivable_collection_ratio": collection / receivable
            if receivable > 0
            else 0,
            "sales_contribution": (record.net_sales / total_net_sales) * 100,
            "collection_contribution": (collection / total_collection) * 100
            if collection > 0
            else 0,
        }
        data.append(row)
    return data, total_net_sales, total_collection, total_receivable


def get_conditions(filters):
    conditions = ""

    conditions += "si.docstatus = 1 and si.name = sit.parent"
    if filters.get("from_date"):
        conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
    if filters.get("to_date"):
        conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
    if filters.get("customer_group"):
        conditions += " and si.customer_group = '%s' " % filters.get("customer_group")
    if filters.get("territory"):
        conditions += " and si.territory = '%s' " % filters.get("territory")

    return conditions


def get_chart_data(data):
    brands = []
    net_sales = []
    collection = []
    outstanding = []
    j = 1
    for i in data:
        if i["customer_group"] and j <= 10:
            brands.append(i["customer_group"])
            collection.append(i["collection"])
            net_sales.append(i["net_sales"])
            outstanding.append(i["total_account_receivable"])
            j = j + 1
    chart = {
        "data": {
            "labels": brands,
            "datasets": [
                {"name": "Net Sales", "values": net_sales},
                {"name": "Total Collection", "values": collection},
                {"name": "Account Receivable", "values": outstanding},
            ],
        }
    }
    chart["type"] = "bar"
    chart["colors"] = ["#6495ED", "#D2691E", "#F1F104"]
    return chart
