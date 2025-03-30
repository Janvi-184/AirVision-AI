import os
import time
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AQICN_API_KEY")


# Dictionary of cities with their corresponding station IDs
cities = {
    "Delhi": "@10114",
    "Mumbai": "@13713",
    "Bangalore": "@11276",
    "Chennai": "@11859",
    "Kolkata": "@11281",
    "Hyderabad": "@14135",
    "Ahmedabad": "@13749",
    "Jaipur": "@11308",
    "Gandhinagar": "@13731",
    "Indore": "@12437",
    "Patna": "@12744",
    "Nagpur": "@12444",
    "Udaipur": "@11314",
    "Lucknow": "@12468"
}

# Function to fetch AQI for a single city
def get_aqi(city):
    if city not in cities:
        return {"error": "City not found"}

    station_id = cities[city]
    url = f"https://api.waqi.info/feed/{station_id}/?token={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") == "ok":
            aqi_value = data["data"].get("aqi", "N/A")  # Get AQI, fallback to "N/A" if missing
            return {
                "city": city,
                "aqi": aqi_value,
                "date": datetime.today().strftime("%Y-%m-%d")
            }
        else:
            return {"error": "API error", "details": data.get("data")}

    except requests.exceptions.RequestException:
        return {"error": "Failed to fetch AQI"}

# Example Usage:
#result = get_aqi("Delhi")
#print(result)
