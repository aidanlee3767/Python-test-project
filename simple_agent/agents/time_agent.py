from datetime import datetime

from simple_agent.utils.api_client import TimeZoneClient


class TimeAgent:
    """Agent for handling time-related queries."""

    def __init__(self):
        self.timezone_client = TimeZoneClient()

    def get_time_by_city(self, city_name: str):
        """Get current time for a specific city."""
        try:
            timezone_str = self.timezone_client.get_timezone_by_city(city_name)
            if not timezone_str:
                return {
                    "status": "error",
                    "message": f"Timezone not found for city: {city_name}",
                    "city": city_name,
                }

            time_info = self.timezone_client.get_current_time(timezone_str)
            if "error" in time_info:
                return {
                    "status": "error",
                    "message": time_info["error"],
                    "city": city_name,
                }

            return {
                "status": "success",
                "city": city_name,
                "timezone": time_info["timezone"],
                "current_time": time_info["current_time"],
                "utc_offset": time_info["utc_offset"],
                "is_dst": time_info["is_dst"],
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        except Exception as e:
            return {"status": "error", "message": str(e), "city": city_name}

    def get_time_by_country(self, country_name: str):
        """Get current time for a specific country."""
        try:
            timezone_str = self.timezone_client.get_timezone_by_country(country_name)
            if not timezone_str:
                return {
                    "status": "error",
                    "message": f"Timezone not found for country: {country_name}",
                    "country": country_name,
                }

            time_info = self.timezone_client.get_current_time(timezone_str)
            if "error" in time_info:
                return {
                    "status": "error",
                    "message": time_info["error"],
                    "country": country_name,
                }

            return {
                "status": "success",
                "country": country_name,
                "timezone": time_info["timezone"],
                "current_time": time_info["current_time"],
                "utc_offset": time_info["utc_offset"],
                "is_dst": time_info["is_dst"],
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        except Exception as e:
            return {"status": "error", "message": str(e), "country": country_name}

    def get_multiple_times(self, locations: list, location_type: str = "city"):
        """Get time information for multiple locations."""
        results = {}

        for location in locations:
            if location_type == "city":
                time_info = self.get_time_by_city(location)
            elif location_type == "country":
                time_info = self.get_time_by_country(location)
            else:
                time_info = {
                    "status": "error",
                    "message": "Invalid location_type. Use 'city' or 'country'",
                }

            if time_info["status"] == "success":
                results[location] = {
                    "timezone": time_info["timezone"],
                    "current_time": time_info["current_time"],
                    "utc_offset": time_info["utc_offset"],
                    "is_dst": time_info["is_dst"],
                }

        return {
            "status": "success",
            "location_type": location_type,
            "locations_processed": len(locations),
            "successful_results": len(results),
            "results": results,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def main():
    """Test the TimeAgent."""
    print("🕐 TimeAgent 테스트")
    agent = TimeAgent()

    # 단일 도시 시간 조회 테스트
    print("\n🌍 도시별 시간 조회 테스트:")
    seoul_time = agent.get_time_by_city("Seoul")
    print(f"Seoul: {seoul_time}")

    tokyo_time = agent.get_time_by_city("Tokyo")
    print(f"Tokyo: {tokyo_time}")

    london_time = agent.get_time_by_city("London")
    print(f"London: {london_time}")

    new_york_time = agent.get_time_by_city("New York")
    print(f"New York: {new_york_time}")

    # 존재하지 않는 도시 테스트
    unknown_time = agent.get_time_by_city("UnknownCity123")
    print(f"Unknown City: {unknown_time}")

    # 국가별 시간 조회 테스트
    print("\n🌏 국가별 시간 조회 테스트:")
    korea_time = agent.get_time_by_country("South Korea")
    print(f"South Korea: {korea_time}")

    usa_time = agent.get_time_by_country("United States")
    print(f"United States: {usa_time}")

    # 다중 위치 시간 조회 테스트
    print("\n🌍 다중 도시 시간 조회 테스트:")
    cities = ["Seoul", "Tokyo", "London", "New York", "Sydney"]
    multiple_results = agent.get_multiple_times(cities, "city")
    print(f"다중 도시 결과: {multiple_results}")

    # 결과 세부 출력
    print("\n📊 세부 결과:")
    if multiple_results["status"] == "success":
        for city, info in multiple_results["results"].items():
            print(f"  {city} → {info['current_time']} ({info['timezone']})")

    print("\n🎉 모든 테스트 완료!")


if __name__ == "__main__":
    main()
