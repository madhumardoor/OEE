import pandas as pd

def calculate_oee(df, device, location, month):
    # Filter by device
    if device:
        df = df[df['Device ID'].str.upper() == device]

    # Filter by location
    if location:
        df = df[df['Location'].str.lower() == location.lower()]

    # Filter by full month name and year
    if month:
        df = df.copy()
        df['Month'] = df['Month'].str.strip().str.lower()  # Normalize
        full_month = f"{month.lower()} 2024"
        df = df[df['Month'] == full_month]

    # If no matching data
    if df.empty:
        return {"Message": "No data found for the given filters."}

    # Calculate averages
    availability = df['Availability'].mean()
    performance = df['Performance'].mean()
    quality = df['Quality'].mean()

    oee = availability * performance * quality
    oee_percentage = oee * 100

    return {
        "Availability": f"{availability:.2%}",
        "Performance": f"{performance:.2%}",
        "Quality": f"{quality:.2%}",
        "OEE": f"{oee_percentage:.2f}%"
    }

def extract_filters(query):
    query = query.lower()
    device = next((word.upper() for word in query.split() if word.upper().startswith("D")), None)
    month = next((m for m in ["jan", "feb", "mar", "apr", "may", "jun", "jul",
                              "aug", "sep", "oct", "nov", "dec"] if m in query), None)
    location = next((loc for loc in ["plant a", "plant b"] if loc in query), None)
    return device, location.title() if location else None, month
