import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Climate Insights Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    data_path = 'data/climate_change_data.csv'  
    return pd.read_csv(data_path)



# Data cleaning function
def clean_data(data):
    """Function to clean the climate change dataset."""
    
    # Drop rows where essential columns are missing (e.g., 'Temperature', 'CO2 Emissions')
    data = data.dropna(subset=['Temperature', 'CO2 Emissions', 'Sea Level Rise', 'Precipitation', 'Humidity', 'Wind Speed'])
    
    # Fill missing values with a placeholder or the column mean (if it's not critical)
    data['Temperature'] = data['Temperature'].fillna(data['Temperature'].mean())
    data['CO2 Emissions'] = data['CO2 Emissions'].fillna(data['CO2 Emissions'].mean())
    data['Sea Level Rise'] = data['Sea Level Rise'].fillna(data['Sea Level Rise'].mean())
    data['Precipitation'] = data['Precipitation'].fillna(data['Precipitation'].mean())
    data['Humidity'] = data['Humidity'].fillna(data['Humidity'].mean())
    data['Wind Speed'] = data['Wind Speed'].fillna(data['Wind Speed'].mean())
    
    # Remove duplicate rows
    data = data.drop_duplicates()

    # Ensure 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce') 
    
    # Drop rows where 'Date' couldn't be converted to datetime
    data = data.dropna(subset=['Date'])
    
    # Extract 'Year' from 'Date'
    data['Year'] = data['Date'].dt.year
    
    return data

# Load and clean dataset
data = load_data()
data = clean_data(data)


# Title and Intro
st.title("🌍 Climate Insights Dashboard")
st.markdown("Explore key insights about climate change trends using this interactive dashboard.")

# Convert 'Date' column to datetime and extract the year
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Ensure 'Date' column is in datetime format
data['Year'] = data['Date'].dt.year  # Extract the year from the 'Date' column

# Sidebar
st.sidebar.header("Filter Data")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(data['Year'].min()),
    int(data['Year'].max()),
    (2000, 2024)
)

variable = st.sidebar.selectbox(
    "Choose a Variable to Explore",
    ["Temperature", "CO2 Emissions", "Sea Level", "Precipitation", "Humidity", "Wind Speed"]
)

st.sidebar.markdown("📖 [Learn More About Climate Change](https://www.ipcc.ch/)")

# Filter data based on the year range
filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

# Temperature Trends
if variable == "Temperature":
    st.header("Temperature Trends 🌡️")
    temp_fig = px.line(
        filtered_data, 
        x='Year', 
        y='Temperature', 
        title="Global Temperature Trends",
        labels={'Temperature': 'Temperature (°C)'}
    )
    st.plotly_chart(temp_fig, use_container_width=True)

# CO₂ Emissions
elif variable == "CO2 Emissions":
    st.header("CO₂ Emissions 📈")
    co2_fig = px.bar(
        filtered_data, 
        x='Year', 
        y='CO2 Emissions', 
        title="CO₂ Emissions Over the Years",
        labels={'CO2 Emissions': 'CO₂ Emissions (ppm)'}
    )
    st.plotly_chart(co2_fig, use_container_width=True)

# Sea Level Rise
elif variable == "Sea Level":
    st.header("Sea Level Rise 🌊")
    sea_level_fig = px.scatter(
        filtered_data, 
        x='Year', 
        y='Sea Level Rise', 
        title="Sea Level Rise Trends",
        labels={'Sea Level': 'Sea Level (mm)'}
    )
    st.plotly_chart(sea_level_fig, use_container_width=True)

# Precipitation Trends
elif variable == "Precipitation":
    st.header("Precipitation Trends 🌧️")
    precipitation_fig = px.area(
        filtered_data, 
        x='Year', 
        y='Precipitation', 
        title="Global Precipitation Trends",
        labels={'Precipitation': 'Precipitation (mm)'}
    )
    st.plotly_chart(precipitation_fig, use_container_width=True)

# Humidity Trends
elif variable == "Humidity":
    st.header("Humidity Trends 💧")
    humidity_fig = px.line(
        filtered_data, 
        x='Year', 
        y='Humidity', 
        title="Global Humidity Trends",
        labels={'Humidity': 'Humidity (%)'}
    )
    st.plotly_chart(humidity_fig, use_container_width=True)

# Wind Speed Trends
elif variable == "Wind Speed":
    st.header("Wind Speed Trends 🌬️")
    wind_fig = px.line(
        filtered_data, 
        x='Year', 
        y='Wind Speed', 
        title="Global Wind Speed Trends",
        labels={'Wind Speed': 'Wind Speed (km/h)'}
    )
    st.plotly_chart(wind_fig, use_container_width=True)


# Display Summary Statistics
st.header("Summary Statistics 📊")

# Check if data is available and not empty
if not filtered_data.empty:
    summary_stats = filtered_data.describe()

    # Rename columns for clarity
    summary_stats = summary_stats.rename(
        columns={
            "count": "Count",
            "mean": "Mean",
            "std": "Standard Deviation",
            "min": "Minimum",
            "25%": "25th Percentile",
            "50%": "Median",
            "75%": "75th Percentile",
            "max": "Maximum"
        }
    )

    # Display the summary statistics
    st.write(summary_stats)
else:
    st.error("No data available to display summary statistics.")

# Download Filtered Data
st.header("Download Data 📂")
@st.cache
def convert_df(df):
    """Converts DataFrame to CSV."""
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_data)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_climate_data.csv',
    mime='text/csv'
)
