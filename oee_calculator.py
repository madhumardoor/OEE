import pandas as pd

# Assuming this is where the OEE calculation happens
def calculate_oee(df, device, location, month):
    # Filter by device if specified
    if device:
        df = df[df['Device ID'] == device]
    
    # Filter by location if specified
    if location:
        df = df[df['Location'].str.lower() == location.lower()]
    
    # Parse the 'Month' column to datetime, considering the format 'MMM YYYY'
    if month:
        df['Month'] = pd.to_datetime(df['Month'], format='%b %Y', errors='coerce')
        # Filter by month
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
