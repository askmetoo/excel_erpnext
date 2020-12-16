import frappe


def process_purchase_orders():
    purchase_orders = frappe.get_all(
        "Purchase Order",
        filters = [
            ["status", "!=", "Complete"],
        ],
    )

    for po in purchase_orders:
        if po.get('name'):
            frappe.db.sql(
                '''
                UPDATE `tabPurchase Order` po
                    INNER JOIN (
                        SELECT purchase_order, SUM(qty) as total
                        FROM `tabPurchase Receipt Item`
                        GROUP BY purchase_order
                    ) pr ON po.name = pr.purchase_order
                    SET po.per_received = pr.total * 100 / po.total_qty,
                        po.status = "Complete"
                    WHERE po.name = "%s";
                ''',
                po.get('name'),
            )
