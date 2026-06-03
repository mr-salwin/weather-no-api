import streamlit as st
import requests
from geopy.geocoders import Nominatim

# --- Configuration & Page Setup ---
st.set_page_config(page_title="SkyCast | Weather App", page_icon="🌤️", layout="centered")

# --- Helper Functions ---
def get_coordinates(city_name):
    """Converts a city name into latitude and longitude using free Geocoding."""
    try:
        # Nominatim requires a unique user_agent string to identify your app
        geolocator = Nominatim(user_agent="my_unique_streamlit_weather_app")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude, location.address
        return None
    except Exception:
        return None

def get_weather_data(lat, lon):
    """Fetches real-time weather from the free, no-key Open-Meteo API."""
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "auto"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_weather_emoji(weather_code):
    """Maps WMO Weather Interpretation Codes to emojis."""
    # 0 = Clear, 1-3 = Partly Cloudy, 45-48 = Fog, 51-67 = Drizzle/Rain, 71-77 = Snow, 95+ = Thunderstorm
    if weather_code == 0:
        return "☀️", "Clear Sky"
    elif weather_code in [1, 2, 3]:
        return "⛅", "Partly Cloudy"
    elif weather_code in [45, 48]:
        return "🌫️", "Foggy"
    elif weather_code in [51, 53, 55, 61, 63, 65]:
        return "🌧️", "Rainy"
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        return "❄️", "Snowy"
    elif weather_code >= 95:
        return "⛈️", "Thunderstorm"
    else:
        return "☁️", "Overcast / Unknown"

# --- UI Layout ---
st.title("SALWIN'S Weather 🥵 🥵 🥵")
st.markdown("Search for any location worldwide. No API keys required!")

# Search Bar
city_input = st.text_input("🔍 Search Location:", placeholder="e.g., Paris, New York, Mumbai")

if city_input:
    with st.spinner("Finding location details..."):
        coord_result = get_coordinates(city_input)
        
    if coord_result:
        lat, lon, full_address = coord_result
        
        with st.spinner("Fetching live forecast..."):
            weather_json = get_weather_data(lat, lon)
            
        if weather_json and "current_weather" in weather_json:
            current = weather_json["current_weather"]
            temp = current["temperature"]
            wind_speed = current["windspeed"]
            emoji, condition_desc = get_weather_emoji(current["weathercode"])
            
            # --- Display Results ---
            st.markdown("---")
            st.subheader("📍 Location Found")
            st.caption(full_address)
            
            # Main Weather Section
            col_main, col_desc = st.columns([1, 2])
            with col_main:
                st.markdown(f"## {temp}°C")
            with col_desc:
                st.markdown(f"### {emoji} {condition_desc}")
                
            st.markdown("### Additional Metrics")
            col1, col2 = st.columns(2)
            col1.metric(label="💨 Wind Speed", value=f"{wind_speed} km/h")
            col2.metric(label="🌐 Coordinates", value=f"{round(lat, 2)}°, {round(lon, 2)}°")
        else:
            st.error("⚠️ Could not retrieve weather data. Try again later.")
    else:
        st.error("⚠️ Location not found! Please check the spelling or add a country name (e.g., 'Kochi, India').")