import os
import pandas as pd
import requests
from dotenv import load_dotenv
import streamlit as st
import plotly.express as px
from datetime import datetime

# Load environment variables
load_dotenv()
DATA_URL = os.getenv("DATA_URL_INDIA")
GITHUB_REPO_PATH = os.getenv("GITHUB_REPO_PATH")

# File paths
DATA_PATH = os.path.join(GITHUB_REPO_PATH, "data", "netflix_india_weekly.csv")
OUTPUT_PATH = os.path.join(GITHUB_REPO_PATH, "outputs", "monthly_watch_hours.csv")

# Function to fetch data
def fetch_data():
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        with open(DATA_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Netflix India data downloaded successfully.")
    else:
        st.error("Failed to fetch data from Netflix Top 10 portal.")

# Function to process data
def prepare_monthly_data():
    df = pd.read_csv(DATA_PATH)
    df['Week'] = pd.to_datetime(df['Week'])
    df['Month'] = df['Week'].dt.to_period('M').astype(str)
    monthly_data = df.groupby('Month')['Hours Viewed'].sum().reset_index()
    monthly_data.columns = ['Month', 'Total Hours Viewed']
    monthly_data.to_csv(OUTPUT_PATH, index=False)
    return monthly_data

# Streamlit Dashboard
def run_dashboard():
    st.title("📺 Netflix India Monthly Watch Hours Dashboard")
    st.markdown("Source: [Netflix Top 10 India Data](https://top10.netflix.com)")
    st.markdown("---")

    if not os.path.exists(DATA_PATH):
        fetch_data()

    monthly_data = prepare_monthly_data()

    st.subheader("Monthly Watch Hours (in Millions)")
    fig = px.bar(monthly_data, x='Month', y='Total Hours Viewed',
                 title='Netflix India Monthly Watch Hours',
                 labels={'Total Hours Viewed': 'Watch Hours (Millions)'})
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(monthly_data)

    st.success(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_dashboard()
