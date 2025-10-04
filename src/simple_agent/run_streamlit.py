"""Streamlit Application Runner

Provides functionality to run the Streamlit web interface
for the smart personal assistant chatbot.
"""

import os
import subprocess


def run_streamlit():
    """
    Streamlit 앱 실행

    Streamlit 서버를 실행하여 웹 기반 인터페이스를 제공합니다.
    포트 8501에서 실행되며, app.py 파일을 대상으로 합니다.

    Raises:
        KeyboardInterrupt: 사용자가 Ctrl+C로 종료할 때
        Exception: Streamlit 실행 중 기타 오류 발생 시
    """
    print("🚀 Streamlit 앱 실행 중...")
    try:
        # Find project root directory (where app.py is located)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, "..", "..")
        project_root = os.path.abspath(project_root)

        subprocess.run(
            ["streamlit", "run", "app.py", "--server.port", "8501"], cwd=project_root
        )
    except KeyboardInterrupt:
        print("\n👋 Streamlit 앱이 종료되었습니다.")
    except Exception as e:
        print(f"❌ Streamlit 실행 중 오류: {e}")


def main():
    """
    메인 실행 함수

    Streamlit 앱 실행을 위한 환영 메시지를 출력하고
    웹 인터페이스를 시작합니다.
    """
    print("=" * 50)
    print("🤖 스마트 개인 비서 Streamlit 앱")
    print("=" * 50)

    print("\n" + "=" * 50)
    print("🌐 Streamlit 웹 인터페이스 실행")
    print("브라우저에서 http://localhost:8501 로 접속하세요")
    print("종료하려면 Ctrl+C 를 누르세요")
    print("=" * 50)

    # Streamlit 앱 실행
    run_streamlit()


if __name__ == "__main__":
    main()
