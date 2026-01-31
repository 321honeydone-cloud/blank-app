import streamlit as st
from ui.settings_ui import render_settings_page
from ui.ratebook_ui import render_ratebook_page
from ui.quote_ui import render_quote_page

st.set_page_config(page_title="HoneyDone Manager", layout="wide")

PAGES = {
    "Settings": render_settings_page,
    "Rate Book": render_ratebook_page,
    "Quote Builder": render_quote_page,
}

st.sidebar.title("HoneyDone Manager")
choice = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[choice]()
