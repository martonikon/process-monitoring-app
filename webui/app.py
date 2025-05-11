import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Process Monitor", layout="wide")

st.title("🖥️ Process Monitoring Dashboard")

# Sidebar filters
filter_name = st.sidebar.text_input("🔍 Filter by process name")
sort_field = st.sidebar.selectbox("Sort by", ["pid", "name", "cpu_percent", "memory_percent"], index=2)
descending = st.sidebar.checkbox("Descending order", value=True)
show_anomalies = st.sidebar.checkbox("Only show anomalies")

# Query the API
params = {
    "sort": sort_field,
    "desc": descending,
    "filter": filter_name,
    "anomalies": show_anomalies
}

try:
    response = requests.get("http://localhost:8000/processes", params=params)
    response.raise_for_status()
    data = response.json()["processes"]
    df = pd.DataFrame(data)

    if not df.empty:
        df["cpu_percent"] = df["cpu_percent"].round(2)
        df["memory_percent"] = df["memory_percent"].round(2)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No matching processes found.")
except Exception as e:
    st.error(f"Failed to load data: {e}")

