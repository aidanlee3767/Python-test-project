"""Streamlit Web Interface for Smart Personal Assistant

A web-based interface for the smart personal assistant chatbot
using Streamlit framework.
"""

import streamlit as st
from src.simple_agent.workflow.main_workflow import MainWorkflow


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "assistant" not in st.session_state:
        try:
            st.session_state.assistant = MainWorkflow()
        except Exception as e:
            st.error(f"챗봇 초기화 실패: {e}")
            st.session_state.assistant = None


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="스마트 개인 비서",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 스마트 개인 비서 챗봇")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar with features
    with st.sidebar:
        st.header("📋 사용 가능한 기능")
        st.markdown("""
        - 🕐 **시간 조회**: '서울 시간 알려줘'
        - 🌍 **국가 정보**: '도쿄는 어느 나라야?'
        - 🏙️ **도시 조회**: '한국의 주요 도시 알려줘'
        - 📰 **뉴스 검색**: '기술 뉴스 찾아줘'
        - 💡 **복합 질문**: '서울 시간과 국가 정보 알려줘'
        """)
        
        if st.button("대화 기록 삭제", type="secondary"):
            st.session_state.messages = []
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("질문을 입력하세요..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            if st.session_state.assistant is None:
                response = "챗봇이 초기화되지 않았습니다. 페이지를 새로고침해주세요."
            else:
                with st.spinner("답변을 생성하는 중..."):
                    try:
                        result = st.session_state.assistant.run(prompt)
                        response = result.get("final_response", "답변을 생성할 수 없습니다.")
                    except Exception as e:
                        response = f"오류가 발생했습니다: {str(e)}"
            
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()