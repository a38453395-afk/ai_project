from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "seoul.csv"

@st.cache_data
def load_data():

    try:
        df = pd.read_csv(CSV_FILE, encoding="cp949")

    except:
        df = pd.read_csv(CSV_FILE, encoding="utf-8")

    return df

df = load_data()
