import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv 

# .env ?뚯씪?먯꽌 ?섍꼍 蹂??濡쒕뱶
load_dotenv()

# langchain ChatOpenAI ?ㅼ젙
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model = "gpt-4o-mini",
    temperature=0.7,
)

# llm ?묐떟 ?앹꽦 ?⑥닔
def generate_response(prompt, system_prompt):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    return response.content

# ?섏씠吏 ?ㅼ젙
st.set_page_config(page_title="AI ?좊줎", page_icon="?쨼")

# ?쒕ぉ 諛??뚭컻
st.title("?쨼 AI ?좊줎")

st.markdown(
    """
    - ???좏뵆由ъ??댁뀡? *?ъ슜?먭?* ?쒖떆??二쇱젣?????李ъ꽦怨?諛섎? ?낆옣??痍⑦븯??    - AI **?먯씠?꾪듃** 媛꾩쓽 ?좊줎??吏꾪뻾?⑸땲??
    """
)

# ?좊줎 二쇱젣 ?낅젰
st.header("?좊줎 二쇱젣 ?낅젰")

topic = st.text_input(
    "?좊줎 二쇱젣瑜??낅젰?섏꽭??", "?멸났吏?μ씠 ?멸컙???쇱옄由щ? ?泥댄빐???쒕떎"
)

# ?좊줎 ?쒖옉 踰꾪듉
if st.button("?좊줎 ?쒖옉"):

    st.session_state.messages = []  # ?좊줎 ?댁슜 湲곕줉

    # ?좊줎 二쇱젣 ?쒖떆
    st.header(f"?좊줎 二쇱젣: {topic}")

    # 李ъ꽦 痢??섍껄 ?앹꽦
    with st.spinner("李ъ꽦 痢??섍껄???앹꽦 以묒엯?덈떎..."):
        pro_prompt = f"""
            ?뱀떊? '{topic}'?????李ъ꽦 ?낆옣??媛吏??좊줎?먯엯?덈떎.
            ?쇰━?곸씠怨??ㅻ뱷???덈뒗 李ъ꽦 痢?二쇱옣???쒖떆?댁＜?몄슂.
            1-2 臾몃떒 ?뺣룄濡?媛꾧껐?섍쾶 ?묒꽦?댁＜?몄슂.
            """
        
        pro_argument = generate_response(
            pro_prompt, "?뱀떊? ?쇰━?곸씠怨??ㅻ뱷???덈뒗 ?좊줎?먯엯?덈떎."
        )

        st.session_state.messages.append({"role": "李ъ꽦 痢?, "content": pro_argument})

    # 諛섎? 痢??섍껄 ?앹꽦
    with st.spinner("諛섎? 痢??섍껄???앹꽦 以묒엯?덈떎..."):
        con_prompt = f"""
            ?뱀떊? '{topic}'?????諛섎? ?낆옣??媛吏??좊줎?먯엯?덈떎.
            ?쇰━?곸씠怨??ㅻ뱷???덈뒗 諛섎? 痢?二쇱옣???쒖떆?댁＜?몄슂.
            1-2 臾몃떒 ?뺣룄濡?媛꾧껐?섍쾶 ?묒꽦?댁＜?몄슂.
            """

        con_argument = generate_response(
            con_prompt, "?뱀떊? ?쇰━?곸씠怨??ㅻ뱷???덈뒗 ?좊줎?먯엯?덈떎."
        )

        st.session_state.messages.append({"role": "諛섎? 痢?, "content": con_argument})

    # ?좊줎 寃곌낵 ?쒖떆
    st.header("?좊줎 寃곌낵")
    for entry in st.session_state.messages:
        st.subheader(entry["role"])
        st.write(entry["content"])
        st.divider()


