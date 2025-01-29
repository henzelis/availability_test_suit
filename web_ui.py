import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import pandas as pd
import site_avail_engine
from tinydb import TinyDB, Query


# st.title("Real-Time Site Availability Dashboard ")
# st.write("Get live site availability status.")
st.set_page_config(
    page_title="Real-Time Site Availability Dashboard",
    page_icon="✅",
    layout="wide",
)

site_url = st.text_input("Enter Site URL", value="https://www.google.com")
# parameter_options = st.multiselect(
#     "Choose parameters to display:",
#     options=["Response time (ms)", "Availability (%)"],
#     default=["Response time (ms)"]
# )
parameter_options = st.segmented_control(
    "Graphs", options=["Response time (ms)", "Availability (%)"], default=["Response time (ms)"], selection_mode="multi"
)

refresh_time = st.selectbox("Choose refresh time (sec):", [10, 15, 30])


# if st.button("Get Site Status Data"):
#     with placeholder.container():
#         status, response_time, current_time = site_avail_engine.check_website_performance(site_url)
#         st.subheader(f"Site Response Time")
#         current_data = {'availability': status, 'response_time': response_time, 'time': current_time}
#         db = TinyDB('local_db.json')
#         db.insert(current_data)
#         df = pd.DataFrame(db.all())
#         st.line_chart(df.set_index("time")["response_time"])
#     time.sleep(refresh_time)

placeholder = st.empty()
while True:
    with placeholder.container():
        status, response_time, current_time = site_avail_engine.check_website_performance(site_url)
        st.subheader(f"Site Response Time")
        current_data = {'availability': status, 'response_time': response_time, 'time': current_time}
        db = TinyDB('local_db.json')
        db.insert(current_data)
        df = pd.DataFrame(db.all())
        df['time'] = pd.to_datetime(df['time'], format="%m-%d-%Y, %H:%M:%S")
        print(df)
        if "Response time (ms)" in parameter_options:
            st.line_chart(df.set_index("time")["response_time"], x_label='Time', y_label='Response Time')
        if "Availability (%)" in parameter_options:
            st.line_chart(df.set_index("time")["availability"], x_label='Time', y_label='Availability')
    time.sleep(refresh_time)

