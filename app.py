import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="AI 블로그 포스팅 도우미", page_icon="📸", layout="centered")

# 2. 사이드바 (설정 메뉴)
with st.sidebar:
    st.header("⚙️ 포스팅 설정")
    # 사용자에게 API 키를 입력받음 (보안을 위해 비밀번호 처리)
    api_key = st.text_input("Google Gemini API 키", type="password", placeholder="AI Studio에서 발급받은 키 입력")
    
    st.divider()
    
    platform = st.selectbox("타겟 플랫폼", ["네이버 블로그", "티스토리", "인스타그램"])
    tone = st.selectbox("글투 (말투)", ["감성적인 에세이 톤", "정보 전달 (전문가 톤)", "친근한 이웃 톤", "유머러스한 톤"])

# 3. 메인 화면
st.title("📸 AI 사진 기반 블로그 포스팅 도우미")
st.markdown("사진을 올리면 AI가 분석하여 찰떡같은 포스팅 초안을 작성해 줍니다!")

# 사진 업로드 창
uploaded_file = st.file_uploader("오늘 찍은 사진을 올려주세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

# 키워드 입력 창
keywords = st.text_input("꼭 들어갔으면 하는 키워드 (선택사항)", placeholder="예: 다낭여행, 가족여행, 다낭디오션에스테이츠")

# 4. 실행 버튼 및 AI 동작 로직
if st.button("🚀 블로그 글 생성하기", type="primary"):
    if not api_key:
        st.error("👈 왼쪽 사이드바에 Google Gemini API 키를 입력해 주세요!")
    elif not uploaded_file:
        st.error("사진을 먼저 업로드해 주세요!")
    else:
        with st.spinner("AI가 사진을 분석하고 글을 작성 중입니다... 잠시만 기다려주세요 ⏳"):
            try:
                # 제미나이 API 설정
                genai.configure(api_key=api_key)
                # 에러가 없는 안정적인 프로(Pro) 모델 사용
                model = genai.
