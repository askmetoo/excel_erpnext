function table_calc(frm) {
    //for total_usd and total_fob_usd
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].total_usd = (frm.doc.lc_costing_items[i].fob_usd * frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");    
    var t_usd = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_usd += flt(d.quantity)*flt(d.fob_usd);
        });
    frm.set_value("total_fob_usd", t_usd);    
    // for fob_weightage
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].fob_weightage = (frm.doc.lc_costing_items[i].total_usd / frm.doc.total_fob_usd);
    }
    frm.refresh_field("lc_costing_items");
    var t_weightage = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_weightage += flt(d.fob_weightage);
    });
    frm.set_value("total_fob_weightage", t_weightage);    
    //for fob_bdt, total_bdt and total_fob_bdt
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].fob_bdt = frm.doc.lc_costing_items[i].fob_usd * frm.doc.conversion_rate;
    }
    frm.refresh_field("lc_costing_items");
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].total_bdt = (frm.doc.lc_costing_items[i].fob_bdt * frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");
    var t_bdt = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_bdt += flt(d.quantity)*flt(d.fob_bdt);
    });
    frm.set_value("total_fob_bdt", t_bdt);
    // Quantity Part
    var t_quantity = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_quantity += flt(d.quantity);
    });
    frm.set_value("total_quantity", t_quantity);
    // for duty
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].duty = ((frm.doc.lc_costing_items[i].fob_weightage * frm.doc.duty_cost) / frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");
    var t_duty = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_duty += flt(d.quantity)*flt(d.duty);
    });
    frm.set_value("total_duty", t_duty);
    // for finance
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].finance = ((frm.doc.lc_costing_items[i].fob_bdt * (frm.doc.finance_cost_percentage/100) * 90) / 365);
    }
    frm.refresh_field("lc_costing_items");
    var t_finance = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_finance += flt(d.quantity)*flt(d.finance);
    });
    frm.set_value("total_finance", t_finance);
    // for INSURANCE
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].insurance = ((frm.doc.lc_costing_items[i].fob_weightage * frm.doc.insurance_cost) / frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");
    var t_insurance = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_insurance += flt(d.quantity)*flt(d.insurance);
    });
    frm.set_value("total_insurance", t_insurance);
    // for TRANSPORT
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].transport = ((frm.doc.lc_costing_items[i].fob_weightage * frm.doc.transport_cost) / frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");
    var t_transport = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_transport += flt(d.quantity)*flt(d.transport);
    });
    frm.set_value("total_transport", t_transport);            
    // for FREIGHT
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].freight = ((frm.doc.lc_costing_items[i].fob_weightage * frm.doc.freight_cost) / frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");
    var t_freight = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_freight += flt(d.quantity)*flt(d.freight);
    });
    frm.set_value("total_freight", t_freight);        
    // for CNF
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].cnf = ((frm.doc.lc_costing_items[i].fob_weightage * frm.doc.cnf_cost) / frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");
    var t_cnf = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_cnf += flt(d.quantity)*flt(d.cnf);
    });
    frm.set_value("total_cnf", t_cnf);
    
    // for MARKETING & OPEX
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].marketing = (frm.doc.lc_costing_items[i].fob_bdt + frm.doc.lc_costing_items[i].duty + frm.doc.lc_costing_items[i].finance + frm.doc.lc_costing_items[i].insurance + frm.doc.lc_costing_items[i].transport + frm.doc.lc_costing_items[i].freight + frm.doc.lc_costing_items[i].cnf) * (frm.doc.marketing_cost_percentage/100);
    }
    frm.refresh_field("lc_costing_items");
    var t_marketing = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_marketing += flt(d.quantity)*flt(d.marketing);
    });
    frm.set_value("total_marketing", t_marketing);
    // for LANDING COST
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].landing_cost = (frm.doc.lc_costing_items[i].fob_bdt + frm.doc.lc_costing_items[i].duty + frm.doc.lc_costing_items[i].finance + frm.doc.lc_costing_items[i].insurance + frm.doc.lc_costing_items[i].transport + frm.doc.lc_costing_items[i].freight + frm.doc.lc_costing_items[i].cnf + frm.doc.lc_costing_items[i].marketing);
    }
    frm.refresh_field("lc_costing_items");
    var t_landing_cost = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_landing_cost += flt(d.quantity)*flt(d.landing_cost);
    });
    frm.set_value("total_landing_cost", t_landing_cost);
    // for Selling Price
    var t_selling_price = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_selling_price += flt(d.quantity)*flt(d.selling_price);
    });
    frm.set_value("total_selling_price", t_selling_price);    
    // for Margin
    for ( let i in frm.doc.lc_costing_items){
        frm.doc.lc_costing_items[i].margin = (frm.doc.lc_costing_items[i].selling_price - frm.doc.lc_costing_items[i].landing_cost);
        frm.doc.lc_costing_items[i].margin_for_total_quantity = (frm.doc.lc_costing_items[i].margin * frm.doc.lc_costing_items[i].quantity);
    }
    frm.refresh_field("lc_costing_items");    
    var t_margin = 0;
    $.each(frm.doc.lc_costing_items || [], function (i, d) {
        t_margin += flt(d.quantity)*flt(d.margin);
    });
    frm.set_value("total_margin", t_margin);
}

frappe.ui.form.on("Excel LC Costing Items", "quantity", table_calc);
frappe.ui.form.on("Excel LC Costing Items", "fob_usd", table_calc);
frappe.ui.form.on("Excel LC Costing Items", "selling_price", table_calc);
frappe.ui.form.on("Excel LC Costing Items", "lc_costing_items_remove", table_calc);
frappe.ui.form.on("Excel LC Costing", "conversion_rate", table_calc);
frappe.ui.form.on("Excel LC Costing", "duty_cost", table_calc);
frappe.ui.form.on("Excel LC Costing", "finance_cost_percentage", table_calc);
frappe.ui.form.on("Excel LC Costing", "insurance_cost", table_calc);
frappe.ui.form.on("Excel LC Costing", "transport_cost", table_calc);
frappe.ui.form.on("Excel LC Costing", "freight_cost", table_calc);
frappe.ui.form.on("Excel LC Costing", "cnf_cost", table_calc);
frappe.ui.form.on("Excel LC Costing", "marketing_cost_percentage", table_calc);

frappe.ui.form.on("Excel LC Costing", {
    total_margin: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn]; 
        frappe.model.set_value(cdt, cdn, "total_margin_percentage", (frm.doc.total_margin / frm.doc.total_landing_cost)*100); 
        frm.refresh_field("total_margin_percentage"); 
    }
});