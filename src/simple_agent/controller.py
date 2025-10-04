"""
Controller for Simple Agent System
Coordinates all agents and handles user queries
"""

from src.simple_agent.agents.country_agent import CountryAgent
from src.simple_agent.agents.time_agent import TimeAgent

# from simple_agent.agents.news_agent import NewsAgent  # Uncomment when ready


class AssistantController:
    """
    Main controller for the assistant system.

    Coordinates all agents and handles user queries by routing them to
    appropriate specialized agents (TimeAgent, CountryAgent, etc.).

    Attributes:
        time_agent: Agent for handling time-related queries
        country_agent: Agent for handling country and city-related queries
    """

    def __init__(self):
        """Initialize all agents."""
        self.time_agent = TimeAgent()
        self.country_agent = CountryAgent()
        # self.news_agent = NewsAgent()  # Uncomment when ready

        print("✅ AssistantController initialized")
        print("   - TimeAgent: Ready")
        print("   - CountryAgent: Ready")
        # print("   - NewsAgent: Ready")

    def get_time(self, location, location_type="city"):
        """
        Get current time for a location.

        Args:
            location (str): City or country name
            location_type (str): "city" or "country"

        Returns:
            dict: Time information
        """
        if location_type == "city":
            return self.time_agent.get_time_by_city(location)
        elif location_type == "country":
            return self.time_agent.get_time_by_country(location)
        else:
            return {
                "status": "error",
                "message": "Invalid location_type. Use 'city' or 'country'",
            }

    def get_multiple_times(self, locations, location_type="city"):
        """
        Get time for multiple locations.

        Args:
            locations (list): List of location names
            location_type (str): "city" or "country"

        Returns:
            dict: Time information for all locations
        """
        return self.time_agent.get_multiple_times(locations, location_type)

    def get_cities_by_country(self, country_name):
        """
        Get major cities for a country.

        Args:
            country_name (str): Country name

        Returns:
            dict: List of major cities
        """
        return self.country_agent.get_cities_by_country(country_name)

    # def get_latest_news(self, category="technology", country="us", num_articles=10):
    #     """
    #     Get latest news articles.
    #
    #     Args:
    #         category (str): News category
    #         country (str): Country code
    #         num_articles (int): Number of articles
    #
    #     Returns:
    #         dict: News articles
    #     """
    #     return self.news_agent.get_latest_news(category, country, num_articles)

    def process_query(self, query_type, **kwargs):
        """
        Process a query based on type.

        Args:
            query_type (str): Type of query ("time", "cities", "news")
            **kwargs: Additional arguments for the query

        Returns:
            dict: Query results
        """
        try:
            if query_type == "time":
                location = kwargs.get("location")
                location_type = kwargs.get("location_type", "city")

                if not location:
                    return {
                        "status": "error",
                        "message": "Location is required for time queries",
                    }

                return self.get_time(location, location_type)

            elif query_type == "multiple_times":
                locations = kwargs.get("locations")
                location_type = kwargs.get("location_type", "city")

                if not locations:
                    return {"status": "error", "message": "Locations list is required"}

                return self.get_multiple_times(locations, location_type)

            elif query_type == "cities":
                country = kwargs.get("country")

                if not country:
                    return {
                        "status": "error",
                        "message": "Country is required for cities query",
                    }

                return self.get_cities_by_country(country)

            # elif query_type == "news":
            #     category = kwargs.get("category", "technology")
            #     country = kwargs.get("country", "us")
            #     num_articles = kwargs.get("num_articles", 10)
            #
            #     return self.get_latest_news(category, country, num_articles)

            else:
                return {
                    "status": "error",
                    "message": f"Unknown query type: {query_type}",
                    "available_types": ["time", "multiple_times", "cities"],
                }

        except Exception as e:
            return {"status": "error", "message": f"Error processing query: {str(e)}"}


def main():
    """Test the controller."""
    print("🎮 Testing AssistantController\n")

    controller = AssistantController()

    # Test 1: Get time for a city
    print("\n" + "=" * 50)
    print("Test 1: Get time for Seoul")
    print("=" * 50)
    result = controller.process_query("time", location="Seoul", location_type="city")
    print(result)

    # Test 2: Get multiple times
    print("\n" + "=" * 50)
    print("Test 2: Get multiple city times")
    print("=" * 50)
    cities = ["Seoul", "Tokyo", "London"]
    result = controller.process_query(
        "multiple_times", locations=cities, location_type="city"
    )
    print(result)

    # Test 3: Get cities by country
    print("\n" + "=" * 50)
    print("Test 3: Get cities in South Korea")
    print("=" * 50)
    result = controller.process_query("cities", country="South Korea")
    print(result)

    # Test 4: Invalid query type
    print("\n" + "=" * 50)
    print("Test 4: Invalid query type")
    print("=" * 50)
    result = controller.process_query("invalid_type")
    print(result)

    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    main()
