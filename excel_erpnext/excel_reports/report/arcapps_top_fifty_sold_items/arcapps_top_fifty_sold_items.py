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
    data, total_net_sales = get_data(filters)
    chart = get_chart_data(data, total_net_sales)
    return columns, data, None, chart


def get_columns():
    columns = [
        {"label": ("Rank"), "fieldname": "rank", "fieldtype": "int", "width": 50},
        {
            "label": ("Brand"),
            "fieldname": "brand",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150,
        },
        {
            "label": ("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": ("Net Sales"),
            "fieldname": "net_sales",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
    ]
    return columns


def get_data(filters=None):
    data = []
    conditions = get_conditions(filters)
    gl_entries = frappe.db.sql(
        """
                        SELECT
				sit.brand as brand,
				sit.item_name as item_name,
				sum(sit.amount) as net_sales
                        FROM
                                `tabSales Invoice` AS si, `tabSales Team` st,`tabSales Invoice Item` sit
                        WHERE
                                {conditions}
                        GROUP BY
                                sit.item_name
                        ORDER BY sum(sit.amount) DESC
			Limit 50
                        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )

    total_net_sales = 0.0
    rank = 0
    for record in gl_entries:
        #               if record.brand:
        total_net_sales += record.net_sales

    for record in gl_entries:
        rank = rank + 1
        row = {
            "rank": rank,
            "brand": record.brand,
            "net_sales": record.net_sales,
            "item_name": record.item_name,
        }
        data.append(row)
    return data, total_net_sales


def get_conditions(filters):
    conditions = ""

    conditions += "si.docstatus = 1 and si.name = st.parent and si.name = sit.parent"
    if filters.get("from_date"):
        conditions += " and si.posting_date >= '%s' " % filters.get("from_date")
    if filters.get("to_date"):
        conditions += " and si.posting_date <= '%s' " % filters.get("to_date")
    if filters.get("customer"):
        conditions += " and si.customer = '%s' " % filters.get("customer")
    if filters.get("customer_group"):
        conditions += " and si.customer_group = '%s' " % filters.get("customer_group")
    if filters.get("territory"):
        conditions += " and si.territory = '%s' " % filters.get("territory")
    if filters.get("salesperson"):
        conditions += " and st.sales_person = '%s' " % filters.get("salesperson")

    return conditions


def get_chart_data(data, total_net_sales):
    brands = []
    net_sales = []
    for i in data:
        if i["item_name"] and i["rank"] <= 10:
            brands.append(i["item_name"])
            net_sales.append(i["net_sales"])
    chart = {
        "data": {
            "labels": brands,
            "datasets": [{"name": "Net Sales", "values": net_sales}],
        }
    }
    chart["type"] = "bar"
    chart["colors"] = ["#FF5733"]
    return chart
