
// After change Invoice Amount .........  

frappe.ui.form.on('Excel Project Tracking Invoice Table', 'amount',
	function (frm) {
		return frm.call({
			doc: frm.doc,
			method: "invoice_amount"
		});
	},
);

// After Delete Invoice Item ..... 

frappe.ui.form.on('Excel Project Tracking Invoice Table', {
	invoice_table_remove: function (frm) {
		return frm.call({
			doc: frm.doc,
			method: "invoice_amount",
		});
	},
});


// frappe.ui.form.on('Excel Project Tracking', {
// 	get_items: function(frm){
// 		return frm.call({
// 			doc:frm.doc,
// 			method: "get_items"
// 		});
// 	},
// });