from __future__ import unicode_literals
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ExcelProjectTrackingSummary(Document):

    def invoice_amount(self):
        #Set Total Invoice Amount    
        total_amount = 0.00
        for d in self.get('invoice_table'):
            if d.amount:
                total_amount = total_amount + float(d.amount)
        self.total_invoice_amount =  total_amount
        
        # Update Project Tracking Items    

        self.set("project_tracking_items", [])
        for sin in self.get("invoice_table"):
            if sin.invoice_no:
                inv_items = frappe.db.sql(
                    f"""
                        SELECT inv_items.item_code, inv_items.item_name, inv_items.qty 
                    from `tabSales Invoice Item` inv_items WHERE inv_items.parent = "{sin.invoice_no}"
                    """,as_dict=True)
                for inv in inv_items:
                    item = self.append("project_tracking_items")
                    item.item_code = inv.item_code
                    item.item_name = inv.item_name
                    item.qty = inv.qty

