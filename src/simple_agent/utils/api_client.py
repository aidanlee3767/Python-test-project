# flake8: noqa E501
from datetime import datetime
from typing import Dict

import pytz
import requests


class TimeZoneClient:
    """
    Client for timezone and time-related operations.

    Provides functionality to get timezone information for cities and countries,
    and calculate current time for specific timezones.

    Attributes:
        COUNTRY_TIMEZONES: Mapping of countries to their primary timezones
        CITY_TIMEZONES: Mapping of major cities to their timezones
    """

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
        """
        Get timezone for a city.

        Args:
            city (str): Name of the city (case-insensitive)

        Returns:
            str: Timezone string (e.g., 'Asia/Seoul') or None if not found
        """
        city_lower = city.lower()
        return self.CITY_TIMEZONES.get(city_lower)

    def get_timezone_by_country(self, country: str) -> str:
        """
        Get timezone for a country.

        Args:
            country (str): Name of the country (case-insensitive)

        Returns:
            str: Timezone string (e.g., 'Asia/Seoul') or None if not found
        """
        country_lower = country.lower()
        return self.COUNTRY_TIMEZONES.get(country_lower)

    def get_current_time(self, timezone_str: str) -> Dict:
        """
        Get current time for a timezone.

        Args:
            timezone_str (str): Timezone string (e.g., 'Asia/Seoul')

        Returns:
            Dict: Time information including current time, UTC offset, and DST status,
                 or error information if timezone is invalid
        """
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
    """
    Client for country information operations.

    Provides functionality to get information about countries and their cities.
    Maintains mappings between cities and countries for quick lookups.

    Attributes:
        country_cities: Mapping of countries to their major cities
        city_to_country: Reverse mapping of cities to their countries
    """

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
        """
        Get country for a city.

        Args:
            city_name (str): Name of the city

        Returns:
            dict: Country information or None if city not found
        """
        country = self.city_to_country.get(city_name)
        if country:
            return {"country": country}
        return None

    def get_cities_by_country(self, country_name: str):
        """
        Get major cities for a country.

        Args:
            country_name (str): Name of the country

        Returns:
            list: List of major cities or None if country not found
        """
        return self.country_cities.get(country_name)
