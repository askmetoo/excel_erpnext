function table_calc(frm, cdt, cdn) {
    //Purchase Part
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].purchase_amount = (frm.doc.excel_project_pre_costing_items[i].purchase_rate * frm.doc.excel_project_pre_costing_items[i].quantity);
        }
        frm.refresh_field("excel_project_pre_costing_items");
        
        var t_purchase = 0;
        $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
        t_purchase += flt(d.quantity)*flt(d.purchase_rate);
            });
        frm.set_value("total_purchase_amount", t_purchase);    

    //Sales Part        
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].sales_amount = (frm.doc.excel_project_pre_costing_items[i].sales_rate * frm.doc.excel_project_pre_costing_items[i].quantity);
        }
        frm.refresh_field("excel_project_pre_costing_items");
        
        var t_sales = 0;
        $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
            t_sales += flt(d.quantity)*flt(d.sales_rate);
            });
        frm.set_value("total_sales_amount", t_sales);
    //VAT AIT Part                
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].vat_ait = (frm.doc.excel_project_pre_costing_items[i].sales_amount * frm.doc.vat_ait_rate)/100;
        }
        frm.refresh_field("excel_project_pre_costing_items");            
        
        var t_vat_ait = 0;
        $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
            t_vat_ait += (frm.doc.excel_project_pre_costing_items[i].sales_amount * frm.doc.vat_ait_rate)/100;
            });
        frm.set_value("total_vat_ait", t_vat_ait);
    //Net Sales
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].net_sales = (frm.doc.excel_project_pre_costing_items[i].sales_amount - frm.doc.excel_project_pre_costing_items[i].vat_ait );
        }
        frm.refresh_field("excel_project_pre_costing_items");    

        var t_net_sales = 0;
        $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
            t_net_sales += flt(d.sales_amount)- flt(d.vat_ait);
            });
        frm.set_value("total_net_sales", t_net_sales );     

        // var t_commission = 0;
        // $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
        //     t_commission += flt(d.commission);
        //     });
        // frm.set_value("total_commission", t_commission); 
    
    //GP
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].gp = (frm.doc.excel_project_pre_costing_items[i].net_sales - frm.doc.excel_project_pre_costing_items[i].purchase_amount - frm.doc.excel_project_pre_costing_items[i].purchase_vat);
        }
        frm.refresh_field("excel_project_pre_costing_items");   

        var t_gp = 0;
        $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
            t_gp += flt(d.net_sales)- flt(d.purchase_amount) - flt(d.purchase_vat);
            });
        frm.set_value("total_gp", t_gp - frm.doc.total_commission);

    //margin    
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].margin = ((frm.doc.excel_project_pre_costing_items[i].gp / frm.doc.excel_project_pre_costing_items[i].net_sales)*100);
        }
        frm.refresh_field("excel_project_pre_costing_items");  
        
    }
frappe.ui.form.on("Excel Project Pre Costing", "purchase_vat_rate", function(frm) { 
    //Purchase VAT Part                
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].purchase_vat = (frm.doc.excel_project_pre_costing_items[i].purchase_amount * frm.doc.purchase_vat_rate)/100;
        }
    frm.refresh_field("excel_project_pre_costing_items"); 


    //GP
        for ( let i in frm.doc.excel_project_pre_costing_items){
            frm.doc.excel_project_pre_costing_items[i].gp = (frm.doc.excel_project_pre_costing_items[i].net_sales - frm.doc.excel_project_pre_costing_items[i].purchase_amount - frm.doc.excel_project_pre_costing_items[i].purchase_vat);
        }
        frm.refresh_field("excel_project_pre_costing_items");   

        var t_gp = 0;
        $.each(frm.doc.excel_project_pre_costing_items || [], function (i, d) {
            t_gp += flt(d.net_sales)- flt(d.purchase_amount) - flt(d.purchase_vat);
            });
        frm.set_value("total_gp", t_gp);
});


frappe.ui.form.on("Excel Project Pre Costing Items", "quantity", table_calc);
frappe.ui.form.on("Excel Project Pre Costing Items", "sales_rate", table_calc);
frappe.ui.form.on("Excel Project Pre Costing Items", "purchase_rate", table_calc);
frappe.ui.form.on("Excel Project Pre Costing", "total_commission", table_calc);
frappe.ui.form.on("Excel Project Pre Costing Items", "purchase_vat", table_calc);
frappe.ui.form.on("Excel Project Pre Costing", "vat_ait_rate", table_calc);
frappe.ui.form.on("Excel Project Pre Costing Items", "excel_project_pre_costing_items_remove", table_calc);

frappe.ui.form.on("Excel Project Pre Costing", {
    total_gp: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn]; 
        frappe.model.set_value(cdt, cdn, "total_margin", (frm.doc.total_gp / frm.doc.total_net_sales)*100); 
        frm.refresh_field("total_margin"); 
    }
});

frappe.ui.form.on("Excel Project Pre Costing Supplier", "supplier_purchase_amount", function(frm) { 
        var t_s_p_t = 0;
        $.each(frm.doc.excel_project_pre_costing_supplier || [], function (i, d) {
            t_s_p_t += flt(d.supplier_purchase_amount);
            });
        frm.set_value("supplier_purchase_total", t_s_p_t);
});

frappe.ui.form.on("Excel Project Pre Costing Supplier", "excel_project_pre_costing_supplier_remove", function(frm) { 
        var t_s_p_t = 0;
        $.each(frm.doc.excel_project_pre_costing_supplier || [], function (i, d) {
            t_s_p_t += flt(d.supplier_purchase_amount);
            });
        frm.set_value("supplier_purchase_total", t_s_p_t);
});

frappe.ui.form.on("Excel Project Pre Costing", "costing_type", function (frm, cdt, cdn) {
    if (frm.doc.costing_type == "Pre Costing")    
        frappe.model.set_value(cdt, cdn, "naming_series", "PRECOST-.#####"); 
    else if (frm.doc.costing_type == "Final Costing") 
        frappe.model.set_value(cdt, cdn, "naming_series", "FINALCOST-.#####"); 
        frm.refresh_field("naming_series"); 
    }
);

