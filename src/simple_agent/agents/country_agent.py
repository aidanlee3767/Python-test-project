from datetime import datetime

from src.simple_agent.utils.api_client import CountryClient


class CountryAgent:
    """
    Agent for handling country-related queries.

    Provides functionality to get information about countries and their cities.
    Uses a CountryClient to access geographical data.

    Attributes:
        country_client: Client for country and city operations
    """

    def __init__(self):
        self.country_client = CountryClient()

    def get_cities_by_country(self, country_name: str):
        """
        Get major cities for a specific country.

        Args:
            country_name (str): Name of the country to get cities for

        Returns:
            dict: List of major cities, city count, and operation status
        """
        try:
            cities = self.country_client.get_cities_by_country(country_name)
            if not cities:
                return {
                    "status": "error",
                    "message": f"Cities not found for country: {country_name}",
                    "country": country_name,
                }

            return {
                "status": "success",
                "country": country_name,
                "cities": cities,
                "city_count": len(cities),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        except Exception as e:
            return {"status": "error", "message": str(e), "country": country_name}


def main():
    """Test the CountryAgent."""
    print("🌍 CountryAgent 테스트")
    agent = CountryAgent()

    # 국가별 주요 도시 조회 테스트
    print("\n🗺️ 국가별 주요 도시 조회 테스트:")
    korea_cities = agent.get_cities_by_country("South Korea")
    print(f"South Korea cities: {korea_cities}")

    usa_cities = agent.get_cities_by_country("United States")
    print(f"United States cities: {usa_cities}")

    japan_cities = agent.get_cities_by_country("Japan")
    print(f"Japan cities: {japan_cities}")

    uk_cities = agent.get_cities_by_country("United Kingdom")
    print(f"United Kingdom cities: {uk_cities}")

    # 존재하지 않는 국가 테스트
    unknown_cities = agent.get_cities_by_country("Unknown Country")
    print(f"Unknown Country: {unknown_cities}")

    print("\n🎉 모든 테스트 완료!")


if __name__ == "__main__":
    main()
