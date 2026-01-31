import streamlit as st
from config import TRIP_FEE, HOURLY_RATE, TAX_RATE, DEFAULT_RATEBOOK_PATH, DEFAULT_RATEBOOK_SHEET

def render_settings_page():
    st.header("Settings")

    if "ratebook_path" not in st.session_state:
        st.session_state.ratebook_path = DEFAULT_RATEBOOK_PATH
    if "ratebook_sheet" not in st.session_state:
        st.session_state.ratebook_sheet = DEFAULT_RATEBOOK_SHEET

    st.session_state.ratebook_path = st.text_input(
        "Rate book Excel path",
        st.session_state.ratebook_path
    )

    st.session_state.ratebook_sheet = st.text_input(
        "Sheet name",
        st.session_state.ratebook_sheet
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reload rate book"):
            st.cache_data.clear()
            st.success("Rate book cache cleared. It will reload on next page view.")

    with col2:
        st.write(f"Trip fee: ${TRIP_FEE:,.2f}")
        st.write(f"Hourly rate: ${HOURLY_RATE:,.2f}")
        st.write(f"Tax rate (materials only): {TAX_RATE*100:.2f}%")
