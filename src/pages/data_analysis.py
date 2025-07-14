import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

# st.markdown("<h2>Data Analysis Page</h2>", unsafe_allow_html=True)

# col1, col2, col3, col4, col5, col6 = st.columns(6)

# with col6:
#     st.page_link("pages/data_analysis.py", label=":grey-background[Analyze]")

# # Use the data from session state if available
# if "data" in st.session_state:
#     data = st.session_state["data"]

#     # Step 2: Data Cleaning
#     data['Time'] = pd.to_datetime(data['Time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
#     data_cleaned = data.dropna(subset=['Inj Gas Meter Volume Instantaneous', 'Inj Gas Valve Percent Open'])
#     data_cleaned['Inj Gas Meter Volume Setpoint'] = data_cleaned['Inj Gas Meter Volume Setpoint'].interpolate()

#     # Step 3: Visualization of All Columns
#     st.write("Trend Analysis:")
#     with st.container():
#         fig, ax = plt.subplots(figsize=(12, 6))
#         ax.plot(data_cleaned['Time'], data_cleaned['Inj Gas Meter Volume Instantaneous'], label='Instantaneous Volume', color='green')
#         ax.plot(data_cleaned['Time'], data_cleaned['Inj Gas Meter Volume Setpoint'], label='Setpoint Volume', color='red', linestyle='dashed')
#         ax.plot(data_cleaned['Time'], data_cleaned['Inj Gas Valve Percent Open'], label='Valve Percent Open (%)', color='blue')

#         ax.set_title("Gas Injection Trends")
#         ax.set_xlabel("Time")
#         ax.set_ylabel("Values")
#         ax.legend()
#         ax.grid()

#         st.pyplot(fig)

#     # Step 4: Display Uploaded Data
#     st.write("Uploaded Data:")
#     st.dataframe(data, width=800, height=500)

#     # Step 5: Process Warnings
#     st.success("Warning(s) Log")
#     warnings = []
#     pipeOpen = True
#     ignore = False
#     previousVolume = data.iloc[0]['Inj Gas Meter Volume Instantaneous']
#     previousValve = data.iloc[0]['Inj Gas Valve Percent Open']

#     for index in range(len(data)):
#         valve = data.iloc[index]['Inj Gas Valve Percent Open'] if not pd.isna(data.iloc[index]['Inj Gas Valve Percent Open']) else previousValve
#         volume = data.iloc[index]['Inj Gas Meter Volume Instantaneous'] if not pd.isna(data.iloc[index]['Inj Gas Meter Volume Instantaneous']) else previousVolume

#         if previousVolume == 0 and volume != 0:
#             pipeOpen = True
#         if previousValve == 100 and valve != 100:
#             ignore = False

#         jump = valve - previousValve
#         if valve == 100 and jump < 50:
#             if ignore:
#                 ignore = False
#                 continue
#             else:
#                 if volume == 0 and pipeOpen:
#                     warning_msg = f"Hydrate formation detected on {data.iloc[index]['Time']}"
#                     warnings.append(warning_msg)
#                     st.toast(warning_msg, icon="⚠️")
#                     st.error(warning_msg, icon="🚨")
#                     pipeOpen = False

#         if jump > 50:
#             ignore = True

#         previousVolume = volume
#         previousValve = valve

# else:
#     st.warning("Please upload a file to proceed.")


def data_analysis():
    st.header("Data Analysis")
    st.write("Your data analysis content goes here.")