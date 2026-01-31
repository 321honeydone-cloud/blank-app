import streamlit as st
import pandas as pd
from services.ratebook_service import load_rate_book
from services.pricing_service import calc_line_totals
from config import TRIP_FEE, HOURLY_RATE, TAX_RATE

def render_quote_page():
    st.header("Quote Builder")

    path = st.session_state.get("ratebook_path")
    sheet = st.session_state.get("ratebook_sheet")

    if not path or not sheet:
        st.warning("Set rate book path and sheet name in Settings.")
        return

    try:
        df = load_rate_book(path, sheet)
    except Exception as e:
        st.error(str(e))
        return

    df = df[df["active"]].copy()

    if "quote_items" not in st.session_state:
        st.session_state.quote_items = []

    colA, colB = st.columns([3, 1])
    with colA:
        selected_code = st.selectbox("Add line item", df["item_code"].tolist())
    with colB:
        qty = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0)

    if st.button("Add to quote"):
        item = df[df["item_code"] == selected_code].iloc[0].to_dict()
        item["qty"] = float(qty)
        st.session_state.quote_items.append(item)

    if not st.session_state.quote_items:
        st.info("Add items to start building a quote.")
        st.write(f"Trip fee (once per job): ${TRIP_FEE:,.2f}")
        return

    lines = []
    subtotal_labor = 0.0
    subtotal_mat = 0.0
    subtotal_tax = 0.0

    for item in st.session_state.quote_items:
        totals = calc_line_totals(
            minutes=item["minutes"],
            materials=item["materials_default"],
            qty=item["qty"],
            hourly_rate=HOURLY_RATE,
            tax_rate=TAX_RATE,
            materials_taxable=bool(item.get("taxable", True)),
        )

        lines.append({
            "code": item["item_code"],
            "name": item["name"],
            "qty": item["qty"],
            "minutes_each": item["minutes"],
            "labor": totals["labor"],
            "materials": totals["materials"],
            "tax_materials": totals["tax"],
            "line_total": totals["total"],
        })

        subtotal_labor += totals["labor"]
        subtotal_mat += totals["materials"]
        subtotal_tax += totals["tax"]

    st.dataframe(pd.DataFrame(lines), use_container_width=True)

    total = TRIP_FEE + subtotal_labor + subtotal_mat + subtotal_tax

    st.subheader("Totals")
    st.write(f"Trip fee: ${TRIP_FEE:,.2f}")
    st.write(f"Labor: ${subtotal_labor:,.2f}")
    st.write(f"Materials: ${subtotal_mat:,.2f}")
    st.write(f"Tax (materials only): ${subtotal_tax:,.2f}")
    st.write(f"Total: ${total:,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear quote"):
            st.session_state.quote_items = []
            st.rerun()
    with col2:
        st.caption("Next step: save this quote into SQLite and generate PDF.")
