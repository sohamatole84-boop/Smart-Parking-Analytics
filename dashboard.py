import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys
import os

from database import read_data
from analysis import parking_analysis

st.set_page_config(
    page_title="Smart Parking Analysis",
    page_icon="🚗",
    layout="wide"
)

st.title("Smart Parking Demand and Event Impact Analysis")

st.write(
    "Parking occupancy, peak hours and event impact analysis."
)

# Check whether the actual dataset exists
parking_file = os.path.join("data", "parking_data.csv")

if not os.path.exists(parking_file):
    st.error(
        "Dataset not found: data/parking_data.csv. "
        "Please upload the full dataset to the data folder on GitHub."
    )
    st.stop()

# Run the complete data pipeline
try:
    with st.spinner("Processing the full parking dataset..."):
        subprocess.run(
            [sys.executable, "main.py"],
            check=True
        )
except subprocess.CalledProcessError:
    st.error("Data pipeline failed. Please check the application logs.")
    st.stop()

# Read database
df = read_data("parking_data")
quality = read_data("quality_report")

if df.empty:
    st.error("No parking records found.")
    st.stop()

# Prepare data
df["OccupancyRate"] = pd.to_numeric(
    df["OccupancyRate"], errors="coerce"
)

df["Hour"] = pd.to_numeric(
    df["Hour"], errors="coerce"
)

df["is_event_day"] = (
    df["is_event_day"].astype(str).str.lower() == "true"
)

# Analysis
results = parking_analysis(df)

# KPI section
st.header("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Records",
    results["total_records"]
)

col2.metric(
    "Parking Areas",
    results["total_parking_areas"]
)

col3.metric(
    "Average Occupancy",
    str(results["average_occupancy"]) + "%"
)

st.divider()

# Dataset
st.header("Parking Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# Parking Area Analysis
st.header("Parking Area Analysis")

st.dataframe(
    results["parking_summary"],
    use_container_width=True
)

fig1, ax1 = plt.subplots()

ax1.bar(
    results["parking_summary"]["SystemCodeNumber"],
    results["parking_summary"]["Average_Occupancy"]
)

ax1.set_xlabel("Parking Area")
ax1.set_ylabel("Average Occupancy (%)")
ax1.set_title("Average Occupancy by Parking Area")

plt.xticks(rotation=45)
st.pyplot(fig1)
plt.close(fig1)

# Peak Hour Analysis
st.header("Peak Hour Analysis")

fig2, ax2 = plt.subplots()

ax2.plot(
    results["hourly_summary"]["Hour"],
    results["hourly_summary"]["Average_Occupancy"],
    marker="o"
)

ax2.set_xlabel("Hour")
ax2.set_ylabel("Average Occupancy (%)")
ax2.set_title("Parking Demand by Hour")

st.pyplot(fig2)
plt.close(fig2)

# Event Day Analysis
st.header("Event Day Impact Analysis")

event_summary = results["event_summary"].copy()

event_summary["Day Type"] = event_summary[
    "is_event_day"
].map({
    True: "Event Day",
    False: "Non-Event Day"
})

st.dataframe(
    event_summary,
    use_container_width=True
)

fig3, ax3 = plt.subplots()

ax3.bar(
    event_summary["Day Type"],
    event_summary["Average_Occupancy"]
)

ax3.set_ylabel("Average Occupancy (%)")
ax3.set_title("Event Day vs Non-Event Day")

st.pyplot(fig3)
plt.close(fig3)

# Data Quality Report
st.header("Data Quality Report")

st.dataframe(
    quality,
    use_container_width=True
)

st.success("Dashboard loaded successfully!")
