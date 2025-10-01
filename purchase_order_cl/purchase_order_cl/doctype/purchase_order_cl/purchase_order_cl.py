import frappe
from frappe.model.document import Document
from frappe.utils import flt

def dv_rut(rut):
    if not rut:
        return False
    rut = str(rut).replace('.', '').replace(' ', '').upper()
    if '-' in rut:
        cuerpo, dv = rut.split('-')
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
        cuerpo //= 10
        multip += 1
        if multip == 8:
            multip = 2
    mod = 11 - (suma % 11)
    dig = '0' if mod == 11 else 'K' if mod == 10 else str(mod)
    return dig == str(dv).upper()

class PurchaseOrderCL(Document):
    def validate(self):
        self.validate_rut()
        self.calculate_totals()

    def validate_rut(self):
        rut = self.get('rut_proveedor')
        if rut and not dv_rut(rut):
            frappe.throw(f'RUT proveedor inválido: {rut}')

    def calculate_totals(self):
        subtotal = 0.0
        taxes_total = 0.0
        for row in self.get('items') or []:
            qty = flt(getattr(row, 'qty', 0), 6)
            rate = flt(getattr(row, 'rate', 0), 2)
            disc = flt(getattr(row, 'discount_amount', 0), 2)
            net = max(qty * rate - disc, 0.0)
            porc = flt(getattr(row, 'porc_iva', None) or self.get('porc_iva') or 19, 2)
            iva = round(net * (porc / 100.0), 2)
            total_line = round(net + iva, 2)
            row.amount = flt(net, 2)
            row.iva_linea = flt(iva, 2)
            row.total_linea = flt(total_line, 2)
            subtotal += net
            taxes_total += iva
        discount_total = flt(self.get('discount_total') or 0, 2)
        charges_total = flt(self.get('charges_total') or 0, 2)
        neto_final = max(subtotal - discount_total + charges_total, 0.0)
        total = round(neto_final + taxes_total, 2)
        self.subtotal_neto = flt(subtotal, 2)
        self.taxes_total = flt(taxes_total, 2)
        self.grand_total = flt(total, 2)
        self.discount_total = flt(discount_total, 2)
        self.charges_total = flt(charges_total, 2)
