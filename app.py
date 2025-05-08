import streamlit as st
import pandas as pd
from oee_calculator import calculate_oee, extract_filters

st.set_page_config(page_title="OEE Chat Assistant", layout="centered")

@st.cache_data
def load_data():
    return pd.read_excel("sensor_data.xlsx")

df = load_data()

st.title("Gen AI OEE Chat Assistant")

query = st.text_input("Ask about OEE:", placeholder="e.g., OEE of Device D1 in Jan 2024 at Plant A")

if st.button("Submit") and query:
    with st.spinner("Processing..."):
        device, location, month = extract_filters(query)
        result = calculate_oee(df, device, location, month)
        st.success("Result:")
        st.write(result if isinstance(result, dict) else {"Message": result})
