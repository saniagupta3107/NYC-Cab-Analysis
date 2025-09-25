# 🚕 NYC Cab Service Analysis & Fleet Optimization

This project uses unsupervised machine learning and data analysis to identify spatial and temporal patterns in New York City cab ride data. The goal is to create a data-driven strategy to optimize taxi fleet deployment, reduce passenger wait times, and increase driver efficiency.

The entire analysis is presented as a fully interactive web application built with Streamlit.

## 🚀 Live Demo

You can view and interact with the live Streamlit application here: \
**https://nyc-cab-analysis.streamlit.app/**

## ✨ Key Features

* **Interactive Hotspot Map:** Uses K-Means clustering to identify 8 primary pickup hotspots across NYC.
* **Advanced Density Analysis:** A detailed drill-down into the busiest hotspot using the HDBSCAN algorithm to find the most concentrated pickup areas.
* **Business & Customer Insights:** Exploratory Data Analysis (EDA) to understand key business metrics, including:
    * Distribution of taxi fares.
    * Typical passenger counts per trip.
    * Hourly trends in average fare prices.
* **Interactive Web Application:** The entire project is deployed as a user-friendly web app with interactive controls.


## 🛠️ Technology Stack

* **Language:** Python
* **Data Manipulation:** Pandas
* **Machine Learning:** Scikit-learn (for K-Means), HDBSCAN
* **Data Visualization:** Plotly Express
* **Web App Framework:** Streamlit

## ⚙️ How to Run Locally

To run this application on your own machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/NYC-Cab-Analysis.git](https://github.com/YourUsername/NYC-Cab-Analysis.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd NYC-Cab-Analysis
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
