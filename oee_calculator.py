import pandas as pd

def calculate_oee(df, device, location, month):
    # Normalize text columns
    df['Device ID'] = df['Device ID'].str.strip().str.upper()
    df['Location'] = df['Location'].str.strip().str.title()
    df['Month'] = pd.to_datetime(df['Month'], format="%b %Y", errors='coerce')

    # Parse input filters
    if device:
        device = device.strip().upper()
        df = df[df['Device ID'] == device]

    if location:
        location = location.strip().title()
        df = df[df['Location'] == location]

    if month:
        month = month.strip().capitalize()
        try:
            month_num = pd.to_datetime(month, format='%b').month
            df = df[df['Month'].dt.month == month_num]
        except ValueError:
            return {"Message": f"Invalid month filter: {month}"}

    # If no matching data
    if df.empty:
        return {"Message": "No data found for the given filters."}

    # Calculate OEE
    availability = df['Availability'].mean()
    performance = df['Performance'].mean()
    quality = df['Quality'].mean()

    oee = availability * performance * quality
    return {
        "Availability": f"{availability:.2%}",
        "Performance": f"{performance:.2%}",
        "Quality": f"{quality:.2%}",
        "OEE": f"{oee * 100:.2f}%"
    }
def extract_filters(query):
    query = query.lower()
    device = next((word.upper() for word in query.split() if word.upper().startswith("D")), None)
    months = {
        "jan": "Jan", "feb": "Feb", "mar": "Mar", "apr": "Apr",
        "may": "May", "jun": "Jun", "jul": "Jul", "aug": "Aug",
        "sep": "Sep", "oct": "Oct", "nov": "Nov", "dec": "Dec"
    }
    month = next((months[m] for m in months if m in query), None)
    location = next((loc.title() for loc in ["plant a", "plant b"] if loc in query), None)
    return device, location, month
