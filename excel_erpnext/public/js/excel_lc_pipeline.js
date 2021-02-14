function total_calc(frm, cdt, cdn) { 
    var d = locals[cdt][cdn]; 
    frappe.model.set_value(cdt, cdn, "due_amount", flt(d.total_pi_value)-flt(d.advance_tt_value)-flt(d.lc_value)); 
    frm.refresh_field("due_amount"); 
}

frappe.ui.form.on("Excel LC Pipeline", "total_pi_value", total_calc);
frappe.ui.form.on("Excel LC Pipeline", "advance_tt_value", total_calc);
frappe.ui.form.on("Excel LC Pipeline", "lc_value", total_calc);