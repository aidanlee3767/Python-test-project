#!/usr/bin/env python3
"""
스마트 개인 비서 챗봇
사용자의 자연어 질문을 분석해서 적절한 API를 호출하고 답변하는 멀티 기능 챗봇
File: simple_agent/main.py
"""

import traceback

from src.simple_agent.workflow.main_workflow import MainWorkflow


def print_welcome():
    """환영 메시지 출력

    스마트 개인 비서 챗봇의 사용 가능한 기능들과 예제를 출력합니다.
    사용자에게 명령어 형식과 종료 방법을 안내합니다.
    """
    print("=" * 50)
    print("🤖 스마트 개인 비서 챗봇")
    print("=" * 50)
    print("사용 가능한 기능:")
    print("🕐 시간 조회: '서울 시간 알려줘'")
    print("🌍 국가 정보: '도쿄는 어느 나라야?'")
    print("🏙️ 도시 조회: '한국의 주요 도시 알려줘'")
    print("📰 뉴스 검색: '기술 뉴스 찾아줘', 'Seoul 뉴스 알려줘'")
    print("💡 복합 질문: '서울 시간과 국가 정보 알려줘'")
    print("-" * 50)
    print("종료: 'quit' 또는 'exit'")
    print("=" * 50)


def main():
    """메인 실행 함수

    스마트 개인 비서 챗봇을 초기화하고 사용자와의 대화 루프를 시작합니다.
    사용자 입력을 받아 MainWorkflow로 처리하고 응답을 출력합니다.

    Raises:
        KeyboardInterrupt: 사용자가 Ctrl+C로 프로그램을 종료할 때
        Exception: 기타 예상치 못한 오류 발생 시
    """
    # API 키 확인 (필요한 경우)
    # if not os.getenv("NEWS_API_KEY"):
    #     print("⚠️ NEWS_API_KEY 환경변수가 설정되지 않았습니다.")
    #     print("뉴스 기능은 사용할 수 없습니다.")

    print_welcome()

    try:
        assistant = MainWorkflow()
        print("✅ 챗봇 초기화 완료!")

        while True:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ["quit", "exit", "종료"]:
                print("👋 안녕히 가세요!")
                break

            if not user_input:
                continue

            print("\n🤖 Assistant: ")
            response = assistant.run(user_input)
            print(response["final_response"])

    except KeyboardInterrupt:
        print("\n\n👋 안녕히 가세요!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
