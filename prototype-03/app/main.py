import streamlit as st

from workflow.graph import create_debate_graph
from workflow.state import DebateState
from utils.state_manager import init_session_state, reset_session_state
from langfuse.langchain import CallbackHandler


def render_input_form():

    with st.form("debate_form", border=False):
        # 토론 주제 입력
        st.text_input(
            label="토론 주제를 입력하세요:",
            value="인공지능은 인간의 일자리를 대체할 수 있습니다.",
            key="ui_topic",
        )

        max_rounds = st.slider("토론 라운드 수", min_value=1, max_value=5, value=1)
        st.session_state.max_rounds = max_rounds
        st.form_submit_button(
            "토론 시작",
            on_click=lambda: st.session_state.update({"app_mode": "debate"}),
        )


def start_debate():

    topic = st.session_state.ui_topic
    max_rounds = st.session_state.max_rounds

    # 그래프 생성
    debate_graph = create_debate_graph()

    # 초기 상태 설정
    initial_state: DebateState = {
        "topic": topic,
        "messages": [],
        "current_round": 1,
        "max_rounds": max_rounds,
    }

    # 토론 시작
    with st.spinner("토론이 진행 중입니다... 완료까지 잠시 기다려주세요."):

        langfuse_handler = CallbackHandler()
        result = debate_graph.invoke(
            initial_state, config={"callbacks": [langfuse_handler]}
        )

        # 결과를 세션 스테이트에 저장
        st.session_state.messages = result["messages"]

    # 토론 결과 모드로 전환
    st.session_state.app_mode = "results"
    st.rerun()


def display_debate_results():

    # 토론 내용 표시
    topic = st.session_state.ui_topic
    st.header(f"토론 주제: {topic}")
    for i, entry in enumerate(st.session_state.messages):
        round_num = (i // 2) + 1

        if round_num <= st.session_state.max_rounds:

            if i % 2 == 0:
                st.subheader(f"라운드 {round_num} / {st.session_state.max_rounds}")

            if entry["role"] == "PRO_AGENT":
                st.subheader("찬성")
            elif entry["role"] == "CON_AGENT":
                st.subheader("반대")
        else:
            st.header("심판")
        st.write(entry["content"])
        st.divider()

    if st.button("새 토론 시작"):
        reset_session_state()
        st.session_state.app_mode = "input"
        st.rerun()


def render_ui():
    # 페이지 설정
    st.set_page_config(page_title="AI 토론", page_icon="🤖")

    # 제목 및 소개
    st.title("🤖 AI 토론 - 멀티 에이전트")
    st.markdown(
        """
        ### 프로젝트 소개
        이 애플리케이션은 3개의 AI 에이전트(찬성, 반대, 심판)가 사용자가 제시한 주제에 대해 토론을 진행합니다.
        각 AI는 서로의 의견을 듣고 반박하며, 마지막에는 심판 AI가 토론 결과를 평가합니다.
        """
    )

    render_input_form()

    current_mode = st.session_state.get("app_mode")

    if current_mode == "debate":
        start_debate()
    if current_mode == "results":
        display_debate_results()


if __name__ == "__main__":
    # 세션 상태 초기화
    init_session_state()

    render_ui()