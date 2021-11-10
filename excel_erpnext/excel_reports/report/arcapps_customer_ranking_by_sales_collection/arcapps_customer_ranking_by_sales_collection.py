# Copyright (c) 2013, Castlecraft Ecommerce Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, scrub
from erpnext.stock.utils import get_incoming_rate
from erpnext.controllers.queries import get_match_cond
from frappe.utils import flt, cint


def execute(filters=None):
    if not filters:
        filters = frappe._dict()
    filters.currency = frappe.get_cached_value(
        "Company", filters.company, "default_currency"
    )

    customer_collection = CustomerCollectionByRankingGenerator(filters)

    data = []

    group_wise_columns = frappe._dict(
        {
            "customer": [
                "customer",
                "base_amount",
                "paid_amount",
                "outstanding_amount",
                "sales_collection_ratio",
                "outstanding_collection_ratio",
                "sales_person",
            ],
        }
    )

    columns = get_columns(group_wise_columns, filters)

    for src in customer_collection.grouped_data:
        row = []
        for col in group_wise_columns.get(scrub(filters.group_by)):
            row.append(src.get(col))

        row.append(filters.currency)
        data.append(row)

    return columns, data


def get_columns(group_wise_columns, filters):
    columns = []
    column_map = frappe._dict(
        {
            "base_amount": _("Net Sales") + ":Currency/currency:100",
            "paid_amount": _("Total Collection") + ":Currency/currency:150",
            "sales_collection_ratio": _("Sales Collection Ratio") + ":Percent:150",
            "outstanding_collection_ratio": _("Outstanding Collection Ratio")
            + ":Percent:180",
            "sales_person": _("Sales person"),
            "outstanding_amount": _("Total Outstanding") + ":Currency/currency:150",
            "customer": _("Customer") + ":Link/Customer:100",
            "customer_group": _("Customer Group") + ":Link/Customer Group:100",
            "territory": _("Territory") + ":Link/Territory:100",
        }
    )

    for col in group_wise_columns.get(scrub(filters.group_by)):
        columns.append(column_map.get(col))

    columns.append(
        {
            "fieldname": "currency",
            "label": _("Currency"),
            "fieldtype": "Link",
            "options": "Currency",
            "hidden": 1,
        }
    )

    return columns


class CustomerCollectionByRankingGenerator(object):
    def __init__(self, filters=None):
        self.data = []
        self.average_buying_rate = {}
        self.filters = frappe._dict(filters)
        self.load_invoice_items()
        self.load_product_bundle()
        self.get_returned_invoice_items()
        self.process()

    def process(self):
        self.grouped = {}
        self.grouped_data = []
        self.currency_precision = cint(frappe.db.get_default("currency_precision")) or 3
        self.float_precision = cint(frappe.db.get_default("float_precision")) or 2
        for row in self.si_list:
            if self.skip_row(row, self.product_bundles):
                continue
            row.base_amount = flt(row.base_net_amount, self.currency_precision)
            row.paid_amount = flt(
                row.base_amount - row.outstanding_amount, self.currency_precision
            )
            row.outstanding_amount = flt(
                row.outstanding_amount, self.currency_precision
            )
            row.sales_person = row.sales_person
            product_bundles = []
            if row.update_stock:
                product_bundles = self.product_bundles.get(row.parenttype, {}).get(
                    row.parent, frappe._dict()
                )
            elif row.dn_detail:
                product_bundles = self.product_bundles.get("Delivery Note", {}).get(
                    row.delivery_note, frappe._dict()
                )
                row.item_row = row.dn_detail

            # get sales collection ratio
            row.sales_collection_ratio = flt(
                (row.paid_amount / row.base_amount) * 100.0, self.currency_precision
            )

            # get outstanding collection ratio
            if row.outstanding_amount:
                row.outstanding_collection_ratio = flt(
                    (row.paid_amount / row.outstanding_amount) * 100.0,
                    self.currency_precision,
                )
            else:
                row.outstanding_collection_ratio = 0.0
            # add to grouped
            self.grouped.setdefault(row.get(scrub(self.filters.group_by)), []).append(
                row
            )

        if self.grouped:
            self.get_average_rate_based_on_group_by()

    def get_average_rate_based_on_group_by(self):
        # sum buying / selling totals for group

        for key in list(self.grouped):
            if self.filters.get("group_by") != "Invoice":
                for i, row in enumerate(self.grouped[key]):
                    if i == 0:
                        new_row = row
                    else:
                        new_row.base_amount += flt(
                            row.base_amount, self.currency_precision
                        )
                        new_row.outstanding_amount += flt(
                            row.outstanding_amount, self.currency_precision
                        )
                        new_row.paid_amount += flt(
                            row.base_amount - row.outstanding_amount,
                            self.currency_precision,
                        )

                new_row = self.set_average_rate(new_row)
                self.grouped_data.append(new_row)
            else:
                for i, row in enumerate(self.grouped[key]):
                    if (
                        row.parent in self.returned_invoices
                        and row.item_code in self.returned_invoices[row.parent]
                    ):
                        returned_item_rows = self.returned_invoices[row.parent][
                            row.item_code
                        ]
                        for returned_item_row in returned_item_rows:
                            row.qty += returned_item_row.qty
                            row.base_amount += flt(
                                returned_item_row.base_amount, self.currency_precision
                            )
                        row.buying_amount = flt(
                            row.qty * row.buying_rate, self.currency_precision
                        )
                    if row.qty or row.base_amount:
                        row = self.set_average_rate(row)
                        self.grouped_data.append(row)

    def set_average_rate(self, new_row):

        new_row.sales_collection_ratio = flt(
            ((new_row.paid_amount / new_row.base_amount) * 100.0),
            self.currency_precision,
        )
        new_row.outstanding_collection_ratio = (
            flt(
                ((new_row.paid_amount / new_row.outstanding_amount) * 100.0),
                self.currency_precision,
            )
            if new_row.paid_amount
            else 0
        )

        return new_row

    def get_returned_invoice_items(self):
        returned_invoices = frappe.db.sql(
            """
			select
				si.name, si_item.item_code, si_item.stock_qty as qty, si_item.base_net_amount as base_amount, si.return_against
			from
				`tabSales Invoice` si, `tabSales Invoice Item` si_item
			where
				si.name = si_item.parent
				and si.docstatus = 1
				and si.is_return = 1
		""",
            as_dict=1,
        )

        self.returned_invoices = frappe._dict()
        for inv in returned_invoices:
            self.returned_invoices.setdefault(
                inv.return_against, frappe._dict()
            ).setdefault(inv.item_code, []).append(inv)

    def skip_row(self, row, product_bundles):
        if self.filters.get("group_by") != "Invoice":
            if not row.get(scrub(self.filters.get("group_by", ""))):
                return True
        elif row.get("is_return") == 1:
            return True

    def get_buying_amount_from_product_bundle(self, row, product_bundle):
        buying_amount = 0.0
        for packed_item in product_bundle:
            if packed_item.get("parent_detail_docname") == row.item_row:
                buying_amount += self.get_buying_amount(row, packed_item.item_code)

        return flt(buying_amount, self.currency_precision)

    def get_buying_amount(self, row, item_code):
        # IMP NOTE
        # stock_ledger_entries should already be filtered by item_code and warehouse and
        # sorted by posting_date desc, posting_time desc
        if item_code in self.non_stock_items:
            # Issue 6089-Get last purchasing rate for non-stock item
            item_rate = self.get_last_purchase_rate(item_code)
            return flt(row.qty) * item_rate

        else:
            my_sle = self.sle.get((item_code, row.warehouse))
            if (row.update_stock or row.dn_detail) and my_sle:
                parenttype, parent = row.parenttype, row.parent
                if row.dn_detail:
                    parenttype, parent = "Delivery Note", row.delivery_note

                for i, sle in enumerate(my_sle):
                    # find the stock valution rate from stock ledger entry
                    if (
                        sle.voucher_type == parenttype
                        and parent == sle.voucher_no
                        and sle.voucher_detail_no == row.item_row
                    ):
                        previous_stock_value = (
                            len(my_sle) > i + 1
                            and flt(my_sle[i + 1].stock_value)
                            or 0.0
                        )
                        if previous_stock_value:
                            return (
                                (previous_stock_value - flt(sle.stock_value))
                                * flt(row.qty)
                                / abs(flt(sle.qty))
                            )
                        else:
                            return flt(row.qty) * self.get_average_buying_rate(
                                row, item_code
                            )
            else:
                return flt(row.qty) * self.get_average_buying_rate(row, item_code)

        return 0.0

    def load_invoice_items(self):
        conditions = ""
        if self.filters.company:
            conditions += " and company = %(company)s"
        if self.filters.from_date:
            conditions += " and posting_date >= %(from_date)s"
        if self.filters.to_date:
            conditions += " and posting_date <= %(to_date)s"
        if self.filters.customer_group:
            conditions += " and customer_group = %(customer_group)s"
        if self.filters.territory:
            conditions += " and territory = %(territory)s"
        if self.filters.brand:
            conditions += " and brand = %(brand)s"

        if self.filters.group_by == "Sales Person":
            sales_person_cols = (
                ", sales.sales_person, sales.allocated_amount, sales.incentives"
            )
            sales_team_table = "left join `tabSales Team` sales on sales.parent = `tabSales Invoice`.name"
        else:
            sales_person_cols = ""
            sales_team_table = ""

        if self.filters.get("sales_invoice"):
            conditions += " and `tabSales Invoice`.name = %(sales_invoice)s"

        if self.filters.get("item_code"):
            conditions += " and `tabSales Invoice Item`.item_code = %(item_code)s"

        self.si_list = frappe.db.sql(
            """
			select
				`tabSales Invoice Item`.parenttype, `tabSales Invoice Item`.parent,
				`tabSales Invoice`.posting_date, `tabSales Invoice`.posting_time,
				`tabSales Invoice`.project, `tabSales Invoice`.update_stock,
				`tabSales Invoice`.customer, `tabSales Invoice`.customer_group,
				`tabSales Invoice`.outstanding_amount,`tabSales Invoice`.total_taxes_and_charges,
				`tabSales Invoice`.total,`tabSales Invoice`.paid_amount,`tabSales Invoice`.territory,
				`tabSales Invoice`.territory, `tabSales Invoice Item`.item_code,
				`tabSales Invoice Item`.item_name, `tabSales Invoice Item`.description,
				`tabSales Invoice Item`.warehouse, `tabSales Invoice Item`.item_group,
				`tabSales Invoice Item`.brand, `tabSales Invoice Item`.dn_detail,
				`tabSales Invoice Item`.delivery_note, `tabSales Invoice Item`.stock_qty as qty,
				`tabSales Invoice Item`.base_net_rate, `tabSales Invoice Item`.base_net_amount,
				`tabSales Invoice Item`.brand,
				
				`tabSales Invoice Item`.name as "item_row", `tabSales Invoice`.is_return
				{sales_person_cols}
			from
				`tabSales Invoice` inner join `tabSales Invoice Item`
					on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
				{sales_team_table}
			where
				`tabSales Invoice`.docstatus=1 and `tabSales Invoice`.is_opening!='Yes' {conditions} {match_cond}
			order by
				`tabSales Invoice`.posting_date desc, `tabSales Invoice`.posting_time desc""".format(
                conditions=conditions,
                sales_person_cols=sales_person_cols,
                sales_team_table=sales_team_table,
                match_cond=get_match_cond("Sales Invoice"),
            ),
            self.filters,
            as_dict=1,
        )

    def load_product_bundle(self):
        self.product_bundles = {}

        for d in frappe.db.sql(
            """select parenttype, parent, parent_item,
			item_code, warehouse, -1*qty as total_qty, parent_detail_docname
			from `tabPacked Item` where docstatus=1""",
            as_dict=True,
        ):
            self.product_bundles.setdefault(d.parenttype, frappe._dict()).setdefault(
                d.parent, frappe._dict()
            ).setdefault(d.parent_item, []).append(d)
