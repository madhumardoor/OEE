import streamlit as st
import pandas as pd

# Assuming this is where the OEE calculation happens
def calculate_oee(df, device, location, month):
    if device:
        df = df[df['Device ID'] == device]
    if location:
        df = df[df['Location'].str.lower() == location.lower()]
    if month:
        # Assuming 'Month' column is in format 'MMM-YYYY'
        df['Month'] = pd.to_datetime(df['Month'], format='%b-%Y')
        df = df[df['Month'].dt.month_name().str.lower() == month.lower()]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        return "No data found for the given filters."
    
    # Calculate OEE components
    availability = df['Availability'].mean()  # Assuming these columns are numerical
    performance = df['Performance'].mean()
    quality = df['Quality'].mean()

    # Calculate OEE
    oee = availability * performance * quality
    oee_percentage = oee * 100
    
    return {
        "Availability": f"{availability:.2%}",
        "Performance": f"{performance:.2%}",
        "Quality": f"{quality:.2%}",
        "OEE": f"{oee_percentage:.2f}%"
    }

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

st.title("Gen AI OEE Chat Assistant")

query = st.text_input("Ask about OEE:", placeholder="e.g., OEE of Device D1 in Jan 2025 at Plant A")

if st.button("Submit") and query:
    with st.spinner("Processing..."):
        device, location, month = extract_filters(query)
        result = calculate_oee(df, device, location, month)
        st.success("Result:")
        st.write(result if isinstance(result, dict) else {"Message": result})
