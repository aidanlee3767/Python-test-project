"""
Google Gemini Workflow for Simple Agent
File: simple_agent/workflows/main_workflow.py

Uses Google Gemini to handle multi-step queries with function calling
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from simple_agent.controller import AssistantController

# Load environment variables
load_dotenv()


class MainWorkflow:
    """
    Smart Assistant using Google Gemini

    Uses Gemini's function calling to:
    - Understand user queries
    - Choose appropriate tools
    - Execute multiple steps if needed
    """

    def __init__(self):
        """
        Initialize the MainWorkflow with Gemini

        1. Setup Gemini client
        2. Define function declarations
        3. Configure model
        """

        # Get Gemini API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY 환경변수를 설정해주세요.")

        # Initialize Gemini client
        self.client = genai.Client(api_key=api_key)
        self.controller = AssistantController()

        # Define function declarations for Gemini
        self.functions = [
            {
                "name": "get_time",
                "description": "도시나 국가의 현재 시간을 조회합니다. Get current time for a city or country.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "도시 이름 (예: Seoul, Tokyo, London)",
                        }
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "get_cities",
                "description": "국가의 주요 도시 목록을 조회합니다. Get major cities for a country.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {
                            "type": "string",
                            "description": "국가 이름 (예: South Korea, Japan, United States)",
                        }
                    },
                    "required": ["country"],
                },
            },
            {
                "name": "get_multiple_times",
                "description": "여러 도시의 시간을 동시에 조회합니다. Get time for multiple cities at once.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "locations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "도시 이름 목록 (예: ['Seoul', 'Tokyo', 'London'])",
                        }
                    },
                    "required": ["locations"],
                },
            },
            {
                "name": "get_country_by_city",
                "description": "도시가 어느 국가에 속하는지 조회합니다. Get which country a city belongs to.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "도시 이름 (예: Seoul, Tokyo, London)",
                        }
                    },
                    "required": ["city"],
                },
            },
            {
                "name": "get_news",
                "description": "최신 IT 기술 뉴스를 조회합니다. Get latest IT/technology news.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "num_articles": {
                            "type": "integer",
                            "description": "가져올 뉴스 개수 (기본값: 5)",
                            "default": 5,
                        }
                    },
                },
            },
        ]

        print("✅ Gemini 챗봇 초기화 완료!")

    def _execute_function(self, function_name: str, arguments: dict) -> str:
        """
        Execute the requested function

        Args:
            function_name (str): Name of the function to execute
            arguments (dict): Function arguments

        Returns:
            str: Function result
        """
        try:
            if function_name == "get_time":
                location = arguments.get("location")
                result = self.controller.get_time(location, location_type="city")

                if result["status"] == "success":
                    return f"{result['city']}: {result['current_time']} ({result['timezone']})"
                else:
                    return f"오류: {result['message']}"

            elif function_name == "get_cities":
                country = arguments.get("country")
                result = self.controller.get_cities_by_country(country)

                if result["status"] == "success":
                    cities = ", ".join(result["cities"])
                    return f"{result['country']}의 주요 도시: {cities}"
                else:
                    return f"오류: {result['message']}"

            elif function_name == "get_multiple_times":
                locations = arguments.get("locations", [])
                result = self.controller.get_multiple_times(
                    locations, location_type="city"
                )

                if result["status"] == "success":
                    response_lines = []
                    for city, info in result["results"].items():
                        response_lines.append(
                            f"{city}: {info['current_time']} ({info['timezone']})"
                        )
                    return "\n".join(response_lines)
                else:
                    return f"오류: {result['message']}"

            elif function_name == "get_country_by_city":
                city = arguments.get("city")

                # Simple city to country mapping
                city_to_country = {
                    "Seoul": "South Korea",
                    "서울": "South Korea",
                    "Tokyo": "Japan",
                    "도쿄": "Japan",
                    "London": "United Kingdom",
                    "런던": "United Kingdom",
                    "New York": "United States",
                    "뉴욕": "United States",
                    "Sydney": "Australia",
                    "시드니": "Australia",
                    "Busan": "South Korea",
                    "부산": "South Korea",
                }

                country = city_to_country.get(city)
                if country:
                    return f"{city}는 {country}에 속해있습니다."
                else:
                    return f"{city}의 국가 정보를 찾을 수 없습니다."

            elif function_name == "get_news":
                num_articles = arguments.get("num_articles", 5)

                try:
                    articles = get_latest_it_news_json(num_articles)

                    if not articles:
                        return "현재 조회 가능한 뉴스가 없습니다."

                    # Format news articles
                    news_list = []
                    for i, article in enumerate(articles[:num_articles], 1):
                        title = article.get("title", "제목 없음")
                        source = article.get("source", {}).get("name", "출처 없음")
                        url = article.get("url", "")
                        description = article.get("description", "")

                        news_item = f"{i}. {title}\n   출처: {source}"
                        if description:
                            news_item += f"\n   요약: {description[:100]}..."
                        news_item += f"\n   링크: {url}"
                        news_list.append(news_item)

                    return "\n\n".join(news_list)

                except Exception as e:
                    return f"뉴스 조회 중 오류가 발생했습니다: {str(e)}"

            else:
                return f"알 수 없는 함수: {function_name}"

        except Exception as e:
            return f"함수 실행 중 오류: {str(e)}"

    def run(self, user_input: str) -> dict:
        """
        Process user input and return response

        Args:
            user_input (str): User's question or request

        Returns:
            dict: Response with final_response key
        """
        try:
            print(f"\n{'=' * 60}")
            print(f"🤖 Processing: '{user_input}'")
            print(f"{'=' * 60}\n")

            # Create chat with function declarations
            chat = self.client.chats.create(
                model="gemini-2.0-flash-exp",
                config=types.GenerateContentConfig(
                    tools=[types.Tool(function_declarations=self.functions)],
                    temperature=0.1,
                ),
            )

            # Send initial message
            response = chat.send_message(user_input)

            # Handle function calls
            max_iterations = 5
            iteration = 0

            while iteration < max_iterations:
                # Check if model wants to call a function
                if not response.candidates:
                    break

                part = response.candidates[0].content.parts[0]

                # If it's a function call
                if hasattr(part, "function_call") and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    arguments = {k: v for k, v in function_call.args.items()}

                    print(f"🔧 Calling function: {function_name}")
                    print(f"   Arguments: {arguments}")

                    # Execute the function
                    function_result = self._execute_function(function_name, arguments)
                    print(f"   Result: {function_result}\n")

                    # Send function result back to model
                    response = chat.send_message(
                        types.Part.from_function_response(
                            name=function_name, response={"result": function_result}
                        )
                    )

                    iteration += 1
                else:
                    # Final text response
                    break

            # Get final response text
            final_response = (
                response.text if response.text else "응답을 생성할 수 없습니다."
            )

            return {
                "query": user_input,
                "final_response": final_response,
                "status": "success",
            }

        except Exception as e:
            return {
                "query": user_input,
                "final_response": f"처리 중 오류가 발생했습니다: {str(e)}",
                "status": "error",
            }


def main():
    """Test the workflow"""
    print("🧪 MainWorkflow (Google Gemini) 테스트")

    try:
        print("🤖 MainWorkflow 초기화 중...")
        workflow = MainWorkflow()

        # Test cases
        test_cases = [
            "서울 시간 알려줘",
            "도쿄 시간은?",
            "한국의 주요 도시 알려줘",
            "서울과 도쿄의 시간을 동시에 알려줘",
            "서울은 어느 나라야?",
            "도쿄는 어느 국가에 속해있어?",
            "최신 IT 뉴스 3개 알려줘",
            "기술 뉴스 보여줘",
        ]

        print(f"\n🧪 {len(test_cases)}개 테스트 케이스 실행:")
        print("-" * 50)

        for i, test_input in enumerate(test_cases, 1):
            print(f"\n[테스트 {i}/{len(test_cases)}]")
            print(f"👤 사용자: {test_input}")

            try:
                result = workflow.run(test_input)
                print(f"\n🤖 Assistant:\n{result['final_response']}")
            except Exception as e:
                print(f"❌ 오류: {e}")

            print("-" * 50)

        print("\n🎉 테스트 완료!")

    except ValueError as e:
        print(f"❌ 설정 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
