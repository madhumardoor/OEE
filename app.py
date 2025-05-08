import streamlit as st
import pandas as pd
from oee_calculator import calculate_oee

st.set_page_config(page_title="OEE Chat Assistant", layout="centered")  

@st.cache_data
def load_data():
    return pd.read_excel("sensor_data.xlsx")

df = load_data()

def extract_filters(query):
    query = query.lower()
    device = next((word.upper() for word in query.split() if word.upper().startswith("D")), None)
    month = next((m for m in ["jan", "feb", "mar", "apr", "may", "jun", "jul",
                              "aug", "sep", "oct", "nov", "dec"] if m in query), None)
    location = next((loc for loc in ["plant a", "plant b"] if loc in query), None)
    return device, location.title() if location else None, month

st.title(" Gen AI OEE Chat Assistant")

query = st.text_input("Ask about OEE:", placeholder="e.g., OEE of Device D1 in Jan 2025 at Plant A")

if st.button("Submit") and query:
    with st.spinner("Processing..."):
        device, location, month = extract_filters(query)
        result = calculate_oee(df, device, location, month)
        st.success("Result:")
        st.write(result if isinstance(result, dict) else {"Message": result})
