function total_calc(frm, cdt, cdn) { 
    var d = locals[cdt][cdn]; 
    frappe.model.set_value(cdt, cdn, "pad_amount", flt(d.us_dollar)*flt(d.us_dollar_rate)); 
    frm.refresh_field("pad_amount"); 
    
    var e = locals[cdt][cdn]; 
    frappe.model.set_value(cdt, cdn, "excess_tk", e.excess_dollar * e.excess_dollar_rate); 
    frm.refresh_field("excess_tk");
    
    frappe.model.set_value(cdt, cdn, "grand_total", d.pad_amount + d.excess_tk + d.commission + d.cnf + d.atvat + d.freight + d.carriage + d.unloading + d.ait);
    refresh_field ('grand_total');
}

frappe.ui.form.on("Excel LC No", "us_dollar", total_calc);
frappe.ui.form.on("Excel LC No", "us_dollar_rate", total_calc);
frappe.ui.form.on("Excel LC No", "excess_dollar", total_calc);
frappe.ui.form.on("Excel LC No", "excess_dollar_rate", total_calc);
frappe.ui.form.on("Excel LC No", "commission", total_calc);
frappe.ui.form.on("Excel LC No", "cnf", total_calc);
frappe.ui.form.on("Excel LC No", "atvat", total_calc);
frappe.ui.form.on("Excel LC No", "freight", total_calc);
frappe.ui.form.on("Excel LC No", "carriage", total_calc);
frappe.ui.form.on("Excel LC No", "unloading", total_calc);
frappe.ui.form.on("Excel LC No", "ait", total_calc);