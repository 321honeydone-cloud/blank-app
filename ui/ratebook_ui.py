import streamlit as st
import pandas as pd
from services.ratebook_service import load_rate_book

def render_ratebook_page():
    st.header("Rate Book")

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

    q = st.text_input("Search", "")
    if q.strip():
        mask = (
            df["name"].str.contains(q, case=False, na=False) |
            df["category"].str.contains(q, case=False, na=False) |
            df["item_code"].str.contains(q, case=False, na=False)
        )
        df = df[mask]

    category = st.selectbox("Category", ["All"] + sorted(df["category"].unique().tolist()))
    if category != "All":
        df = df[df["category"] == category]

    show_cols = ["item_code", "category", "name", "minutes", "materials_default", "taxable"]
    st.dataframe(df[show_cols], use_container_width=True)
