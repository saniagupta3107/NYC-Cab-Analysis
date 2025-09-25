# Import all the necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import hdbscan
import warnings

warnings.filterwarnings('ignore')

# --- App Configuration ---
st.set_page_config(page_title="NYC Cab Analysis", page_icon="🚕", layout="wide")


# --- Caching Data ---
@st.cache_data
def load_data(file_path):
    """A simple function to load data and handle potential errors."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file {file_path} was not found. Please make sure it's in the same folder as app.py.")
        return None

# --- Main App ---

# --- Title and Introduction ---
st.title("🚕 NYC Cab Service Analysis")
st.markdown("This project analyzes NYC taxi data to identify pickup hotspots and understand business trends, aiming to improve fleet efficiency.")


# --- Load Data ---
df_hotspots = load_data('uber-raw-data-apr14.csv')
df_insights = load_data('cab.csv') # CORRECTED FILENAME for the second dataset

# Only proceed if both datasets were loaded successfully
if df_hotspots is not None and df_insights is not None:

    # --- PART 1: HOTSPOT ANALYSIS ---
    st.header("Part 1: Geographic Hotspot Analysis")

    # --- Interactive Widget: Slider for K-Means ---
    st.subheader("K-Means Clustering of Pickup Locations")
    k_value = st.slider("Select the number of clusters (k) for K-Means:", min_value=2, max_value=15, value=8)

    # CORRECTED a potential column name issue. The standard dataset uses 'Lat' and 'Lon'.
    # Ensure your column names match exactly. Case matters.
    if 'Lat' in df_hotspots.columns and 'Lon' in df_hotspots.columns:
        lat_col, lon_col = 'Lat', 'Lon'
    elif 'Latitude' in df_hotspots.columns and 'Longitude' in df_hotspots.columns:
        lat_col, lon_col = 'Latitude', 'Longitude'
    else:
        st.error("Could not find Latitude/Longitude columns in the Uber dataset. Please check the file.")
        st.stop() # Stops the app from running further if columns aren't found.
        
    # Run K-Means
    X = df_hotspots[[lat_col, lon_col]]
    kmeans = KMeans(n_clusters=k_value, random_state=42, n_init=10)
    kmeans.fit(X)
    df_hotspots['cluster'] = kmeans.labels_

    # Display K-Means Map
    st.markdown(f"**Interactive Map of {k_value} Pickup Hotspots**")
    fig_kmeans_map = px.scatter_mapbox(df_hotspots.sample(50000), 
                                       lat=lat_col, lon=lon_col, color="cluster",
                                       size_max=15, zoom=10, mapbox_style="carto-positron")
    st.plotly_chart(fig_kmeans_map, use_container_width=True)


    # --- PART 2: CUSTOMER & BUSINESS INSIGHTS ---
    st.header("Part 2: Customer & Business Insights")

    # --- Data Cleaning for Part 2 ---
    df_insights['fare_amount'] = pd.to_numeric(df_insights['fare_amount'], errors='coerce')
    df_insights['pickup_datetime'] = pd.to_datetime(df_insights['pickup_datetime'], errors='coerce')
    df_insights.dropna(inplace=True)
    df_insights['hour'] = df_insights['pickup_datetime'].dt.hour
    
    # --- Display Charts in Columns ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution of Taxi Fares")
        fig_fare_hist = px.histogram(df_insights[df_insights['fare_amount'].between(2, 100)], 
                                     x="fare_amount", nbins=50)
        st.plotly_chart(fig_fare_hist, use_container_width=True)

    with col2:
        st.subheader("Number of Trips by Passenger Count")
        passenger_counts = df_insights[df_insights['passenger_count'].between(1, 6)]['passenger_count'].value_counts()
        fig_pass_bar = px.bar(x=passenger_counts.index, y=passenger_counts.values,
                              labels={'x': 'Number of Passengers', 'y': 'Number of Trips'})
        st.plotly_chart(fig_pass_bar, use_container_width=True)

    st.subheader("Average Taxi Fare by Hour of the Day")
    hourly_fares = df_insights.groupby('hour')['fare_amount'].mean().reset_index()
    fig_hourly_line = px.line(hourly_fares, x='hour', y='fare_amount', markers=True)
    st.plotly_chart(fig_hourly_line, use_container_width=True)