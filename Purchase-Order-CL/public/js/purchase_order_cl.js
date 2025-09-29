frappe.ui.form.on('Purchase Order CL Item', {
    cantidad: function(frm, cdt, cdn) { calculate_line(frm, cdt, cdn); },
    precio_unitario: function(frm, cdt, cdn) { calculate_line(frm, cdt, cdn); },
    descuento_linea: function(frm, cdt, cdn) { calculate_line(frm, cdt, cdn); },
    porc_iva_linea: function(frm, cdt, cdn) { calculate_line(frm, cdt, cdn); }
});

frappe.ui.form.on('Purchase Order CL', {
    porc_iva: function(frm) { frm.trigger('recalculate_totals'); },
    discount_total: function(frm) { frm.trigger('recalculate_totals'); },
    cargos_total: function(frm) { frm.trigger('recalculate_totals'); },
    recalculate_totals: function(frm) {
        frappe.call({
            method: "purchase_order_cl.purchase_order_cl.doctype.purchase_order_cl.purchase_order_cl.calculate_totals",
            doc: frm.doc,
            freeze: true
        }).then(()=> frm.refresh());
    }
});

function calculate_line(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let qty = flt(row.cantidad || 0);
    let price = flt(row.precio_unitario || 0);
    let desc = flt(row.descuento_linea || 0);
    let neto = qty * price - desc;
    if (neto < 0) neto = 0;
    let porc_iva = flt(row.porc_iva_linea || frm.doc.porc_iva || 19);
    let iva = round(neto * (porc_iva/100.0), 2);
    row.subtotal_linea = neto;
    row.iva_linea = iva;
    row.total_linea = neto + iva;
    refresh_field(['items','subtotal_neto','monto_iva','total']);
    frm.trigger('recalculate_totals');
}
