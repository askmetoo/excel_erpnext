frappe.ui.form.on("Item Price", "before_save", function (frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Item Price",
            filters: [
                ['price_list', "=", cur_frm.doc.price_list],
                ["item_code", "=", cur_frm.doc.item_code],
            ],
            fields: [
                "price_list_rate",
                "name"
            ]
        },
        callback: function (r) { // do this to found price list doc
            var OldPrice = (r.message[0].price_list_rate);
            var OldName = (r.message[0].name);
            var NewPrice = cur_frm.doc.price_list_rate;
            //console.log(OldPrice); console.log(NewPrice); 
            if (OldPrice == NewPrice) {
                frappe.validated = false;
                msgprint('Price already exists');
            }
            else {
                frappe.validated = false;
                frappe.confirm(
                    `Do you want to update the price of ${cur_frm.doc.item_code} from ${OldPrice} to ${NewPrice} in ${cur_frm.doc.price_list}?`,
                    function () { // do this if ok
                        frappe.db.set_value("Item Price", OldName, "price_list_rate", NewPrice);
                        msgprint('Price have been updated successfully');
                    },
                    function () { // do nothing if cancel
                    }
                );
            }
        }
    });
});