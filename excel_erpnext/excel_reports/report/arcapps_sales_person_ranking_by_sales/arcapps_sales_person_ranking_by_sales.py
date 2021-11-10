# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _, scrub
from erpnext.accounts.utils import get_currency_precision
from frappe.utils import getdate, nowdate, flt
from six import iteritems, itervalues


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data, total_net_sales, total_collection = get_data(filters)
    chart = get_chart_data(data, total_net_sales, total_collection)
    return columns, data, None, chart


def get_columns():
    columns = [
        {"label": ("Rank"), "fieldname": "rank", "fieldtype": "int", "width": 50},
        {
            "label": ("Sales Person"),
            "fieldname": "salesperson",
            "fieldtype": "Link",
            "options": "Sales Person",
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
            "label": ("Total Collection"),
            "fieldname": "total_collection",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "label": ("Total Outstanding"),
            "fieldname": "total_outstanding",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "label": ("Sales-Collection Ratio"),
            "fieldname": "sales_collection",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": ("Outstanding-Collection Ratio"),
            "fieldname": "outstanding_collection",
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
                        SELECT
                                si.total AS net_sales,
                                st.sales_person as salesperson,
				si.outstanding_amount AS total_outstanding,
				si.customer as customer
                        FROM
                                `tabSales Invoice` AS si, `tabSales Team` st
                        WHERE
                                {conditions}
                        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )

    total_net_sales = total_collection = 0.0
    rank = 0
    salespersons = []
    for record in gl_entries:
        if record.salesperson:
            salespersons.append(record.salesperson)

    res = []
    [res.append(x) for x in salespersons if x not in res]
    collection = 0
    collections = 0
    for salesperson in res:
        debit = 0
        credit = 0
        rank = rank + 1
        net_sales = sum(i.net_sales for i in gl_entries if i.salesperson == salesperson)
        outstanding = sum(
            i.total_outstanding for i in gl_entries if i.salesperson == salesperson
        )
        customer = frappe.db.sql(
            """ SELECT
                customer.name as name
                FROM `tabCustomer` as customer,`tabSales Team` as team
                where  customer.name = team.parent and team.sales_person = %s
                """,
            (salesperson),
            as_dict=1,
        )
        # 		frappe.msgprint(str(customer))
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
                                where docstatus = 1 and posting_date >= %s and posting_date <= %s and party = %s and excel_tax_payment = "No" and payment_type = "Receive"
                                """,
                (filters.get("from_date"), filters.get("to_date"), str(i["name"])),
            )
            if collection_amount[0][0]:
                collections += collection_amount[0][0]
        outstanding = debit - credit
        collection = collections
        total_net_sales += flt(net_sales, 2)
        if not outstanding == 0 and not collection < 0:
            total_collection += collection
            row = {
                "rank": rank,
                "net_sales": net_sales,
                "total_collection": collection,
                "total_outstanding": outstanding,
                "sales_collection": (collection / net_sales) * 100,
                "outstanding_collection": (collection / outstanding) * 100,
                "salesperson": salesperson,
            }

        else:
            row = {
                "rank": rank,
                "net_sales": net_sales,
                "total_collection": 0,
                "total_outstanding": outstanding,
                "sales_collection": 0,
                "outstanding_collection": 0,
                "salesperson": salesperson,
            }
        data.append(row)
        collections = 0
    data.sort(key=lambda x: x.get("net_sales"), reverse=True)
    rank = 0
    for i in data:
        rank = rank + 1
        i["rank"] = rank
    return data, total_net_sales, total_collection


def get_conditions(filters):
    conditions = ""

    conditions += "si.docstatus = 1 and si.name = st.parent"
    if filters.get("from_date"):
        conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
    if filters.get("to_date"):
        conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
    if filters.get("territory"):
        conditions += " and si.territory = '%s' " % filters.get("territory")
    if filters.get("salesperson"):
        conditions += " and st.sales_person = '%s' " % filters.get("salesperson")
    if filters.get("customer_group"):
        conditions += " and si.category = '%s' " % filters.get("customer_group")

    return conditions


def get_chart_data(data, total_net_sales, total_collection):
    brands = []
    net_sales = []
    collection = []
    outstanding = []
    for i in data:
        if i["salesperson"] and i["rank"] <= 10:
            brands.append(i["salesperson"])
            collection.append(i["total_collection"])
            net_sales.append(i["net_sales"])
            outstanding.append(i["total_outstanding"])
    chart = {
        "data": {
            "labels": brands,
            "datasets": [
                {"name": "Net Sales", "values": net_sales},
                {"name": "Total Collection", "values": collection},
                {"name": "Total Outstanding", "values": outstanding},
            ],
        }
    }
    chart["type"] = "bar"
    chart["colors"] = ["#6495ED", "#D2691E"]
    return chart
