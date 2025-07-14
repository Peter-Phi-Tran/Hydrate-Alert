import streamlit as st
import pandas as pd

def upload_data():
    st.header("Upload Your Sensor Data")
    uploaded = st.file_uploader("Choose a CSV file")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)
    else:
        st.warning("Please upload a CSV to proceed.")
