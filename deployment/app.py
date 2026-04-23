import streamlit as st
from prediction import render_prediction
from eda import render_eda

st.set_page_config(
    page_title="Trash Bag Prediction",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Trash Prediction")

with st.sidebar:
    st.header("Menu")
    page = st.radio("Pilih halaman", ["EDA", "Prediction"], index=0)

if page == "Prediction":
    render_prediction()
else:
    render_eda()