function table_calc(frm) {
    for ( let i in frm.doc.excel_mps_counter_table){
        frm.doc.excel_mps_counter_table[i].total_bw = (frm.doc.excel_mps_counter_table[i].current_bw - frm.doc.excel_mps_counter_table[i].previous_bw);
    }
    frm.refresh_field("excel_mps_counter_table");    
    var t_bw = 0;
    $.each(frm.doc.excel_mps_counter_table || [], function (i, d) {
        t_bw += flt(d.current_bw)-flt(d.previous_bw);
        });
    frm.set_value("total_bw", t_bw);  
    
    for ( let i in frm.doc.excel_mps_counter_table){
        frm.doc.excel_mps_counter_table[i].total_color = (frm.doc.excel_mps_counter_table[i].current_color - frm.doc.excel_mps_counter_table[i].previous_color);
    }
    frm.refresh_field("excel_mps_counter_table");    
    var t_color = 0;
    $.each(frm.doc.excel_mps_counter_table || [], function (i, d) {
        t_color += flt(d.current_color)-flt(d.previous_color);
        });
    frm.set_value("total_color", t_color);  
}

frappe.ui.form.on("Excel MPS Counter Table", "current_bw", table_calc);
frappe.ui.form.on("Excel MPS Counter Table", "previous_bw", table_calc);
frappe.ui.form.on("Excel MPS Counter Table", "current_color", table_calc);
frappe.ui.form.on("Excel MPS Counter Table", "previous_color", table_calc);
frappe.ui.form.on("Excel MPS Counter Table", "excel_mps_counter_table_remove", table_calc);