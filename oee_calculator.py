# -*- coding: utf-8 -*-
"""
Created on Thu May  8 11:20:07 2025

@author: PC
"""

import pandas as pd

def calculate_oee(df, device_id=None, location=None, month=None):
    if device_id:
        df = df[df['Device ID'] == device_id]
    if location:
        df = df[df['Location'] == location]
    if month:
        df = df[df['Month'] == month]

    if df.empty:
        return "No data found for the given filters."

    availability = df['Availability'].mean()
    performance = df['Performance'].mean()
    quality = df['Quality'].mean()

    oee = availability * performance * quality * 100

    return {
        "Availability": round(availability * 100, 2),
        "Performance": round(performance * 100, 2),
        "Quality": round(quality * 100, 2),
        "OEE": round(oee, 2)
    }
