function total_calc(frm, cdt, cdn) { 
    var d = locals[cdt][cdn]; 
    frappe.model.set_value(cdt, cdn, "eta", frappe.datetime.add_days( d.on_board_date , 15));
    //refresh_field("eta");
    frappe.model.set_value(cdt, cdn, "etr", frappe.datetime.add_days( d.eta , 10));
   // refresh_field("eta");
}
frappe.ui.form.on("Excel LC Pipeline", "on_board_date", total_calc);

function total_calc2(frm, cdt, cdn) { 
    var d = locals[cdt][cdn]; 
    frappe.model.set_value(cdt, cdn, "etr", frappe.datetime.add_days( d.eta , 10));
}
frappe.ui.form.on("Excel LC Pipeline", "eta", total_calc2);

frappe.ui.form.on('Excel LC Pipeline', 'before_submit',  function(frm) {
    if (frm.doc.pipeline_status !='Complete') {
        msgprint('The Pipeline Status is not completed yet!');
        validate = false;
    }
});