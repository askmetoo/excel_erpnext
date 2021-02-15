frappe.ui.form.on('Excel LC Pipeline', 'before_submit',  function(frm) {
    if (frm.doc.pipeline_status !='Completed') {
        msgprint('The Pipeline Status is not completed yet!');
        validate = false;
    }
});