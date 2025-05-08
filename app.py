# -*- coding: utf-8 -*-
"""
Created on Thu May  8 11:22:19 2025

@author: PC
"""

from flask import Flask, request, jsonify
from oee_calculator import calculate_oee
import pandas as pd

app = Flask(__name__)
df = pd.read_excel('sensor_data.xlsx')

@app.route("/api/oee", methods=["POST"])
def get_oee():
    query = request.json.get("query", "").lower()

    # Simple rule-based extraction (could be replaced with NLP/LLM)
    device_id = extract_from_query(query, "device")
    location = extract_from_query(query, "plant")
    month = extract_from_query(query, "jan feb mar apr may jun jul aug sep oct nov dec")

    result = calculate_oee(df, device_id, location, month)
    return jsonify({"result": result})

def extract_from_query(query, key):
    words = query.split()
    for i, word in enumerate(words):
        if key in word:
            return words[i + 1].upper()
    return None

if __name__ == "__main__":
    app.run(debug=True)
