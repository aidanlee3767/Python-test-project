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


class GeoLocationClient:
    """Client for geolocation services using free APIs."""

    # Database of major cities and their countries
    CITY_COUNTRY_DB = {
        "seoul": {"country": "South Korea", "country_code": "KR"},
        "tokyo": {"country": "Japan", "country_code": "JP"},
        "beijing": {"country": "China", "country_code": "CN"},
        "shanghai": {"country": "China", "country_code": "CN"},
        "mumbai": {"country": "India", "country_code": "IN"},
        "delhi": {"country": "India", "country_code": "IN"},
        "london": {"country": "United Kingdom", "country_code": "GB"},
        "paris": {"country": "France", "country_code": "FR"},
        "berlin": {"country": "Germany", "country_code": "DE"},
        "rome": {"country": "Italy", "country_code": "IT"},
        "madrid": {"country": "Spain", "country_code": "ES"},
        "amsterdam": {"country": "Netherlands", "country_code": "NL"},
        "stockholm": {"country": "Sweden", "country_code": "SE"},
        "oslo": {"country": "Norway", "country_code": "NO"},
        "copenhagen": {"country": "Denmark", "country_code": "DK"},
        "new york": {"country": "United States", "country_code": "US"},
        "los angeles": {"country": "United States", "country_code": "US"},
        "chicago": {"country": "United States", "country_code": "US"},
        "toronto": {"country": "Canada", "country_code": "CA"},
        "vancouver": {"country": "Canada", "country_code": "CA"},
        "sydney": {"country": "Australia", "country_code": "AU"},
        "melbourne": {"country": "Australia", "country_code": "AU"},
        "dubai": {"country": "United Arab Emirates", "country_code": "AE"},
        "singapore": {"country": "Singapore", "country_code": "SG"},
        "hong kong": {"country": "Hong Kong", "country_code": "HK"},
        "moscow": {"country": "Russia", "country_code": "RU"},
        "istanbul": {"country": "Turkey", "country_code": "TR"},
        "cairo": {"country": "Egypt", "country_code": "EG"},
        "lagos": {"country": "Nigeria", "country_code": "NG"},
        "johannesburg": {"country": "South Africa", "country_code": "ZA"},
        "sao paulo": {"country": "Brazil", "country_code": "BR"},
        "rio de janeiro": {"country": "Brazil", "country_code": "BR"},
        "mexico city": {"country": "Mexico", "country_code": "MX"},
        "buenos aires": {"country": "Argentina", "country_code": "AR"},
    }

    def get_city_info(self, city_name: str) -> Dict:
        """Get country information for a city."""
        city_lower = city_name.lower().strip()

        # Check local database first
        if city_lower in self.CITY_COUNTRY_DB:
            return self.CITY_COUNTRY_DB[city_lower]

        # Try online API as fallback
        try:
            return self._fetch_from_api(city_name)
        except Exception as e:
            raise Exception(
                f"City '{city_name}' not found in database and API unavailable: {str(e)}"
            )

    def _fetch_from_api(self, city_name: str) -> Dict:
        """Fallback to free geocoding API."""
        try:
            # Using OpenStreetMap Nominatim API (free, no key required)
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": city_name, "format": "json", "limit": 1, "addressdetails": 1}
            headers = {"User-Agent": "SimpleAssistant/1.0"}

            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()
            if not data:
                raise Exception(f"City '{city_name}' not found")

            address = data[0].get("address", {})
            country = address.get("country", "Unknown")
            country_code = address.get("country_code", "XX").upper()

            return {"country": country, "country_code": country_code}

        except Exception as e:
            raise Exception(f"Failed to fetch city info: {str(e)}")
