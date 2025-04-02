import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

st.title("📈 AI-Powered Forex Trading Bot")

model = load_model('models/dqn_forex_model.h5')
uploaded_file = st.file_uploader("Upload Forex Data (CSV)", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data", data.head())

    if st.button("Run AI Trading Strategy"):
        state = np.array(data.iloc[0, 1:6]).reshape(1, -1)
        action = np.argmax(model.predict(state))
        action_text = ["Buy", "Sell", "Hold"][action]
        
        st.success(f"AI Recommendation: {action_text}")
