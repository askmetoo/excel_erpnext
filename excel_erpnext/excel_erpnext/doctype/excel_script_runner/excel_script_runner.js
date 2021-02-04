// Copyright (c) 2021, Castlecraft Ecommerce Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Excel Script Runner', {
  refresh(frm) {
    const url = window.location.href;
    const index = url.indexOf("#");
    const hash = url.substring(index + 1);

    const params = hash.split("?").pop();
    const urlSearchParams = new URLSearchParams(params);

    if (
      hash &&
      params &&
      urlSearchParams.get("customer") &&
      urlSearchParams.get("fromDate") &&
      urlSearchParams.get("toDate")
    ) {
      frappe.set_route("query-report", "Excel Customer Ledger", {
        party_type: "Customer",
        party: urlSearchParams.get("customer"),
        from_date: urlSearchParams.get("fromDate"),
        to_date: urlSearchParams.get("toDate"),
      });
    }
  },
});
