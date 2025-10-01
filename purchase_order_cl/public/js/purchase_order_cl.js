frappe.ui.form.on("Purchase Order CL", {
    refresh: function(frm) {
        if(!frm.doc.naming_series) {
            frm.set_value("naming_series", "OC-.####.-YYYY");
        }
    }
});
