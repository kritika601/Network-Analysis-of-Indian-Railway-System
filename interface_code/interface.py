# This code is part of the Railway Route Finder project. 
# It helps generate a Streamlit web application that allows users to find the most optimal train route between two stations.

import streamlit as st
import pandas as pd
import networkx as nx
from route_logic import find_optimal_route
st.set_page_config(page_title="Railway Route Finder", page_icon="🚆", layout="centered")

st.title("🚆 Railway Route Optimizer")
st.markdown("Enter two stations to find the most optimized train route (minimum number of train changes).")

# Load station data only once
station_data = pd.read_csv("cleaned_dataset/cleaned_train_schedule.csv")

# Map names to codes and vice versa
name_to_code = dict(zip(station_data['Station_Name'], station_data['Station_Code']))
code_to_name = dict(zip(station_data['Station_Code'], station_data['Station_Name']))

# Unique, sorted station names for dropdown
station_names = sorted(name_to_code.keys())

# User input via dropdown
source_name = st.selectbox("🔹 From Station:", station_names)
target_name = st.selectbox("🔸 To Station:", station_names)

# Convert names to codes for route logic
source_code = name_to_code[source_name]
target_code = name_to_code[target_name]

# Button to find the route
if st.button("Find Route"):
    result = find_optimal_route(source_code, target_code)

    if result:
        st.success(f"✅ Minimum Trains Required: {result['min_trains']}")
        for i, leg in enumerate(result['route']):
            from_name = code_to_name.get(leg['From'], leg['From'])
            to_name = code_to_name.get(leg['To'], leg['To'])
            st.markdown(
                f"**Step {i+1}:** Take Train `{leg['Train_No']}` from `{from_name}` to `{to_name}`"
            )
    else:
        st.error("❌ No route found.")
