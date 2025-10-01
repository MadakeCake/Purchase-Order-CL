from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt

def dv_rut(rut):
    rut = str(rut).replace(".", "").replace(" ", "")
    if "-" in rut:
        cuerpo, dv = rut.split("-")
    else:
        cuerpo, dv = rut[:-1], rut[-1]
    try:
        cuerpo = int(cuerpo)
    except:
        return False
    suma = 0
    multip = 2
    while cuerpo > 0:
        suma += (cuerpo % 10) * multip
        cuerpo = cuerpo // 10
        multip += 1
        if multip == 8:
            multip = 2
    mod = 11 - (suma % 11)
    if mod == 11:
        dig = "0"
    elif mod == 10:
        dig = "K"
    else:
        dig = str(mod)
    return dig.upper() == dv.upper()

class PurchaseOrderCL(Document):
    def validate(self):
        self.validate_rut()
        self.calculate_totals()

    def validate_rut(self):
        if self.rut_proveedor:
            if not dv_rut(self.rut_proveedor):
                frappe.throw("RUT proveedor inválido: {}".format(self.rut_proveedor))

    def calculate_totals(self):
        subtotal_neto = 0.0
        total_iva = 0.0
        for row in self.items:
            qty = flt(row.cantidad, 2)
            price = flt(row.precio_unitario, 2)
            desc = flt(row.descuento_linea, 2)
            neto = (qty * price) - desc
            if neto < 0:
                neto = 0
            row.subtotal_linea = flt(neto, 2)
            porc_iva = flt(row.porc_iva_linea or self.porc_iva or 0)
            iva_line = round(neto * (porc_iva/100.0), 2)
            row.iva_linea = flt(iva_line, 2)
            row.total_linea = flt(neto + iva_line, 2)
            subtotal_neto += row.subtotal_linea
            total_iva += row.iva_linea

        subtotal_neto = flt(subtotal_neto, 2)
        descuento_total = flt(self.descuento_total or 0, 2)
        cargos_total = flt(self.cargos_total or 0, 2)
        neto_final = subtotal_neto - descuento_total + cargos_total
        if neto_final < 0:
            neto_final = 0

        total_iva = flt(total_iva, 2)
        total = flt(neto_final + total_iva, 2)

        self.subtotal_neto = subtotal_neto
        self.monto_iva = total_iva
        self.total = total
