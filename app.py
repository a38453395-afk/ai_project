import streamlit as st

st.set_page_config(
    page_title="TFT 전적 분석 시스템",
    page_icon="🎮",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 TFT 데이터 분석 시스템")
st.subheader("Riot API를 활용한 롤토체스 전적 분석")

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
### 📖 프로젝트 소개

본 프로젝트는 Riot Games에서 제공하는 TFT API를 활용하여
사용자의 전적 데이터를 수집하고 분석하는 웹 애플리케이션이다.

### 🎯 개발 목적

- 롤토체스 전적 데이터 수집
- 평균 등수 분석
- TOP4 비율 분석
- 플레이 성향 파악
- 데이터 시각화

### 📊 분석 항목

✅ 평균 등수

✅ TOP4 비율

✅ 최근 20경기 분석

✅ 플레이 스타일 분석

✅ 데이터 기반 피드백 제공
""")

with col2:
    st.info("""
👨‍🏫 수행평가 포인트

✔ API 활용

✔ 데이터 수집

✔ 데이터 시각화

✔ 데이터 분석

✔ 웹 프로그래밍
""")

st.markdown("---")
