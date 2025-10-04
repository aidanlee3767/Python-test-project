# flake8: noqa E501
from datetime import datetime
from typing import Dict

import pytz
import requests


class TimeZoneClient:
    """Client for timezone and time-related operations."""

    # Mapping of countries to their primary timezones
    COUNTRY_TIMEZONES = {
        "south korea": "Asia/Seoul",
        "korea": "Asia/Seoul",
        "united states": "America/New_York",
        "usa": "America/New_York",
        "united kingdom": "Europe/London",
        "uk": "Europe/London",
        "japan": "Asia/Tokyo",
        "china": "Asia/Shanghai",
        "france": "Europe/Paris",
        "germany": "Europe/Berlin",
        "india": "Asia/Kolkata",
        "australia": "Australia/Sydney",
        "canada": "America/Toronto",
        "brazil": "America/Sao_Paulo",
        "russia": "Europe/Moscow",
        "italy": "Europe/Rome",
        "spain": "Europe/Madrid",
        "netherlands": "Europe/Amsterdam",
        "sweden": "Europe/Stockholm",
        "norway": "Europe/Oslo",
        "denmark": "Europe/Copenhagen",
    }

    # Mapping of major cities to timezones
    CITY_TIMEZONES = {
        "seoul": "Asia/Seoul",
        "tokyo": "Asia/Tokyo",
        "beijing": "Asia/Shanghai",
        "shanghai": "Asia/Shanghai",
        "mumbai": "Asia/Kolkata",
        "delhi": "Asia/Kolkata",
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "berlin": "Europe/Berlin",
        "rome": "Europe/Rome",
        "madrid": "Europe/Madrid",
        "amsterdam": "Europe/Amsterdam",
        "stockholm": "Europe/Stockholm",
        "oslo": "Europe/Oslo",
        "copenhagen": "Europe/Copenhagen",
        "new york": "America/New_York",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "toronto": "America/Toronto",
        "vancouver": "America/Vancouver",
        "sydney": "Australia/Sydney",
        "melbourne": "Australia/Melbourne",
        "dubai": "Asia/Dubai",
        "singapore": "Asia/Singapore",
        "hong kong": "Asia/Hong_Kong",
    }

    def get_timezone_by_city(self, city: str) -> str:
        """Get timezone for a city."""
        city_lower = city.lower()
        return self.CITY_TIMEZONES.get(city_lower)

    def get_timezone_by_country(self, country: str) -> str:
        """Get timezone for a country."""
        country_lower = country.lower()
        return self.COUNTRY_TIMEZONES.get(country_lower)

    def get_current_time(self, timezone_str: str) -> Dict:
        """Get current time for a timezone."""
        try:
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)

            return {
                "timezone": timezone_str,
                "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "utc_offset": current_time.strftime("%z"),
                "is_dst": current_time.dst() is not None
                and current_time.dst().total_seconds() > 0,
            }
        except Exception as e:
            return {"error": f"Invalid timezone: {str(e)}"}


class CountryClient:
    """Client for country information operations."""

    def __init__(self):
        self.country_cities = {
            "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"],
            "Japan": ["Tokyo", "Osaka", "Kyoto", "Yokohama", "Nagoya"],
            "United Kingdom": [
                "London",
                "Manchester",
                "Birmingham",
                "Liverpool",
                "Edinburgh",
            ],
            "United States": [
                "New York",
                "Los Angeles",
                "Chicago",
                "Houston",
                "Phoenix",
            ],
            "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        }

        # Auto-build reverse lookup
        self.city_to_country = {}
        for country, cities in self.country_cities.items():
            for city in cities:
                self.city_to_country[city] = country

    def get_country_info_by_city(self, city_name: str):
        """Get country for a city."""
        country = self.city_to_country.get(city_name)
        if country:
            return {"country": country}
        return None

    def get_cities_by_country(self, country_name: str):
        """Get major cities for a country."""
        return self.country_cities.get(country_name)
