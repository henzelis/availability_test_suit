import streamlit as st
from streamlit_folium import st_folium
import folium
import time
import pandas as pd
import site_avail_engine
from tinydb import TinyDB, Query


# st.title("Real-Time Site Availability Dashboard ")
# st.write("Get live site availability status.")
st.set_page_config(
    page_title="Real-Time Site Availability Dashboard",
    page_icon="✅",
    layout="wide"
)


sel_col1, sel_col2 = st.columns(2)

with sel_col1:
    site_url = st.text_input("Enter Site URL", value="https://www.google.com")
    parameter_options = st.segmented_control(
        "Graphs", options=["Response time (ms)", "Availability (%)"],
        default=["Response time (ms)", "Availability (%)"],
        selection_mode="multi"
    )
# parameter_options = st.multiselect(
#     "Choose parameters to display:",
#     options=["Response time (ms)", "Availability (%)"],
#     default=["Response time (ms)"]
# )
with sel_col2:
    refresh_time = st.selectbox("Choose refresh time (sec):", [10, 15, 30])
    if st.button("Clear Database"):
        db = TinyDB('local_db.json', indent=4, separators=(',', ': '))
        query_db = Query()
        db.remove(query_db.site_url == site_url)

site_geo_data = site_avail_engine.get_url_coordinates(site_url)
tiles_list = ["NASAGIBS.ViirsEarthAtNight2012", "Esri.WorldGrayCanvas"]
m = folium.Map(tiles=tiles_list[-1], location=[site_geo_data['latitude'], site_geo_data['longitude']], zoom_start=16)
folium.Marker(location=[site_geo_data['latitude'], site_geo_data['longitude']], popup=site_geo_data['city'],
              tooltip=site_geo_data['region'], icon=folium.Icon(color="green")).add_to(m)

# call to render Folium map in Streamlit
# st_data = st_folium(m, width=725)


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

st.subheader(f"Site {site_url} Response Time")

col1, col2 = st.columns(2)
with col1:
    st_data = st_folium(m, width=725)

with col2:
    placeholder = st.empty()
while True:
    with placeholder.container():


        status, response_time, current_time = site_avail_engine.check_website_performance(site_url)
        current_data = {'site_url': site_url, 'availability': status, 'response_time': response_time, 'time': current_time}
        db = TinyDB('local_db.json', indent=4, separators=(',', ': '))
        db.insert(current_data)
        query_db = Query()
        df = pd.DataFrame(db.search(query_db.site_url == site_url))
        df['time'] = pd.to_datetime(df['time'], format="%m-%d-%Y, %H:%M:%S")
        print(df)
        # st.snow()
        if "Response time (ms)" in parameter_options:
            # with col2:
            st.subheader("Response Time")
            st.line_chart(df.set_index("time")["response_time"], x_label='Time', y_label='Response Time', width=800,
                          height=300, use_container_width=False)
        if "Availability (%)" in parameter_options:
            # with col2:
            st.subheader("Availability")
            st.line_chart(df.set_index("time")["availability"], x_label='Time', y_label='Availability', width=800,
                          height=300, use_container_width=False)
    time.sleep(refresh_time)


