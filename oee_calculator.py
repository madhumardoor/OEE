# oee_calculator.py
import pandas as pd
import re

def extract_filters(query):
    query = query.lower()

    # Extract device ID (e.g., D1, D2, ...)
    device = next((word.upper() for word in query.split() if re.match(r"D\d+", word)), None)
    
    # Extract month (e.g., "jan", "feb", ...)
    month = next((m for m in ["jan", "feb", "mar", "apr", "may", "jun", "jul",
                              "aug", "sep", "oct", "nov", "dec"] if m in query), None)
    
    # Extract location (e.g., "plant a", "plant b")
    location = next((loc for loc in ["plant a", "plant b"] if loc in query), None)

    return device, location.title() if location else None, month


def calculate_oee(df, device, location, month):
    if device:
        df = df[df['Device ID'] == device]
    if location:
        df = df[df['Location'].str.lower() == location.lower()]
    
    # Parse the 'Month' column to datetime, considering the format 'MMM YYYY'
    if month:
        df['Month'] = pd.to_datetime(df['Month'], format='%b %Y', errors='coerce')
        df = df[df['Month'].dt.month_name().str.lower() == month.lower()]
    
    if df.empty:
        return "No data found for the given filters."
    
    # Calculate OEE components
    availability = df['Availability'].mean()
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
