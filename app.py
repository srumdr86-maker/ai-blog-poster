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
                # 구글의 최신 안정화 모델인 2.5 버전으로 교체!
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # 업로드된 이미지를 AI가 읽을 수 있게 변환
                image = Image.open(uploaded_file)
                
                # AI에게 내릴 명령(프롬프트) - 커머스(공동구매) 최적화 버전
                prompt = f"""
                당신은 프로페셔널한 {platform} 인플루언서이자 커머스(공동구매) 판매자입니다.
                첨부된 사진을 자세히 분석하고, 다음 조건에 맞춰 포스팅 글을 작성해 주세요.
                
                - 플랫폼: {platform} (플랫폼 성격에 맞게 해시태그나 이모지 적극 활용)
                - 글투: {tone}
                - 포함할 키워드: {keywords if keywords else '사진에 보이는 특징들'}
                
                [글 작성 구조]
                1. 서론: 사진과 관련된 일상적인 이야기나 공감대로 자연스럽게 시선 끌기
                2. 본론: 사진 속 상황(또는 제품)의 장점과 특징을 매력적으로 어필하기
                3. 결론 (커머스 유도): "현재 한정 수량 공동구매 진행 중!", "프로필 링크에서 구매 가능" 등 자연스러운 판매 유도 멘트와 콜투액션(CTA) 반드시 포함
                
                읽는 사람이 거부감 없이 자연스럽게 구매하고 싶어지도록 매력적으로 써주세요.
                """
                
                # AI에게 사진과 명령 전달 후 결과 받기
                response = model.generate_content([prompt, image])
                
                # 결과 출력
                st.success("✨ 포스팅 초안이 완성되었습니다!")
                st.write("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다. API 키가 정확한지 확인해 주세요. (에러 내용: {e})")
