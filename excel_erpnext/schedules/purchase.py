import frappe


def process_purchase_orders():
    try:
        frappe.db.begin()
        frappe.db.sql(
            '''
            UPDATE `tabPurchase Order` po
                INNER JOIN (
                    SELECT purchase_order, SUM(qty) as total
                    FROM `tabPurchase Receipt Item`
                    GROUP BY purchase_order
                ) pr ON po.name = pr.purchase_order
                SET po.per_received = pr.total * 100 / po.total_qty
                WHERE po.status NOT IN ("Completed","Cancelled") AND po.per_received < 100;
            ''',
        )
    except Exception as e:
        frappe.db.rollback()
    else:
        frappe.db.commit()
    finally:
        frappe.destroy()
