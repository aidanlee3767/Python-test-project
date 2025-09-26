# flake8: noqa: E501
import os
from datetime import datetime

import google.generativeai as genai
import pytz
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model
model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro


# --- Utility functions ---
def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="time_ai_app")
    location = geolocator.geocode(city_name)
    if location:
        return (location.latitude, location.longitude)
    return None


def get_local_time(lat, lon):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    if tz_name is None:
        return "Could not determine timezone."
    timezone = pytz.timezone(tz_name)
    local_time = datetime.now(timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def extract_location(user_input):
    prompt = f"Extract the city or location from this sentence: '{user_input}'. If none, return 'None'."
    response = model.generate_content(prompt)
    location = response.text.strip()
    return location if location.lower() != "none" else None


def time_ai(user_input):
    city = extract_location(user_input)
    if not city:
        return "⚠️ Sorry, I couldn't find a location in your request."

    coords = get_coordinates(city)
    if not coords:
        return f"⚠️ Sorry, I couldn't find the location '{city}'."

    return (
        f"🕒 The local time in **{city}** is **{get_local_time(coords[0], coords[1])}**"
    )
