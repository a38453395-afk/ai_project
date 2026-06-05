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
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="TFT META ANALYZER",
    page_icon="🎮",
    layout="wide"
)

st.title("🏆 TFT META ANALYZER")
st.caption("TFT.GG 스타일 메타 분석 대시보드")

# 예시 메타 데이터
meta_data = [
    ["황금 황소", "S", 58.2, 83.1, 3.4],
    ["펭구 포병", "S", 57.1, 81.5, 3.6],
    ["사신 리롤", "A", 54.8, 76.2, 4.1],
    ["마법사", "A", 53.9, 74.8, 4.2],
    ["난동꾼", "B", 51.5, 69.3, 4.8],
]

df = pd.DataFrame(
    meta_data,
    columns=[
        "덱",
        "티어",
        "승률",
        "TOP4 비율",
        "평균 순위"
    ]
)

st.subheader("📊 현재 메타 티어리스트")
st.dataframe(df, use_container_width=True)

st.subheader("🏆 승률 TOP 덱")

fig = px.bar(
    df,
    x="덱",
    y="승률",
    color="티어",
    text="승률"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

deck = st.selectbox(
    "🎮 덱 선택",
    df["덱"]
)

selected = df[df["덱"] == deck].iloc[0]

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "승률",
        f"{selected['승률']}%"
    )

with c2:
    st.metric(
        "TOP4",
        f"{selected['TOP4 비율']}%"
    )

with c3:
    st.metric(
        "평균 순위",
        selected["평균 순위"]
    )

st.markdown("---")

st.subheader("📖 덱 설명")

descriptions = {
    "황금 황소": "초반 안정성과 후반 고점이 뛰어난 메타 덱",
    "펭구 포병": "강력한 원거리 딜링 중심 덱",
    "사신 리롤": "저코스트 리롤 운영형 덱",
    "마법사": "광역 마법 피해 중심 덱",
    "난동꾼": "높은 체력과 유지력을 활용하는 덱"
}

st.info(descriptions[deck])

st.subheader("🎯 추천 운영")

st.markdown("""
1. 핵심 유닛 확보
2. 아이템 우선 제작
3. 8레벨 타이밍 확보
4. 핵심 2성 완성
""")
