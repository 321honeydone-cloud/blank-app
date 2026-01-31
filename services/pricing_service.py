from __future__ import annotations

def dollars_from_minutes(minutes: float, hourly_rate: float) -> float:
    return (float(minutes) / 60.0) * float(hourly_rate)

def calc_line_totals(minutes: float, materials: float, qty: float, hourly_rate: float, tax_rate: float, materials_taxable: bool):
    qty = float(qty)
    labor = dollars_from_minutes(minutes * qty, hourly_rate)
    mat = float(materials) * qty

    tax = (mat * tax_rate) if materials_taxable else 0.0
    total = labor + mat + tax

    return {
        "labor": labor,
        "materials": mat,
        "tax": tax,
        "total": total,
    }
