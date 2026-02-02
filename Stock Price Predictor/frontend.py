import streamlit as st
import requests

st.title('Stock Price Predictor')

API_URL = "http://127.0.0.1:8000/predict_stock"

st.markdown("Enter the details below")

symbol = st.text_input('Stock Symbol')
date = st.date_input('Select the date')
open = st.number_input(label='Enter the Open')
high = st.number_input(label='Enter the High')
low = st.number_input(label='Enter the Low')
vol = st.number_input(label='Enter the Volume')

if st.button("Predict"):
    data = {
        "symbol": symbol,
        "date": date.strftime("%Y-%m-%d"),
        "open": float(open),
        "high": float(high),
        "low": float(low),
        "volume": int(vol)
    }

    try:
        response = requests.post(API_URL,json=data)
        if response.status_code==200:
            result = response.json()
            st.success(f"Predicted Stock Price: **{result['Predicted_close']}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
            st.error("Could not connect to fast API server. Make sure it's running on PORT 8000..")