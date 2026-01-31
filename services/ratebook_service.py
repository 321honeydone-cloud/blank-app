from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

REQUIRED_COLS = {
    "item_code",
    "category",
    "name",
    "description_customer",
    "minutes",
    "materials_default",
    "taxable",
    "active",
}

@st.cache_data(show_spinner=False)
def load_rate_book(excel_path: str, sheet_name: str) -> pd.DataFrame:
    path = Path(excel_path)
    if not path.exists():
        raise FileNotFoundError(f"Rate book not found at: {excel_path}")

    df = pd.read_excel(path, sheet_name=sheet_name)

    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Rate book missing columns: {sorted(missing)}")

    df["item_code"] = df["item_code"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["name"] = df["name"].astype(str).str.strip()
    df["description_customer"] = df["description_customer"].astype(str).fillna("").str.strip()

    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce").fillna(0.0)
    df["materials_default"] = pd.to_numeric(df["materials_default"], errors="coerce").fillna(0.0)

    df["taxable"] = df["taxable"].astype(str).str.upper().isin(["TRUE", "YES", "1"])
    df["active"] = df["active"].astype(str).str.upper().isin(["TRUE", "YES", "1"])

    df = df.drop_duplicates(subset=["item_code"], keep="last")
    return df
