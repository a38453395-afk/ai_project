import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="TFT META ANALYZER",
    page_icon="🎮",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
    background-color:#f7fafc;
}

h1,h2,h3{
    color:black !important;
}

p,div,span,label{
    color:black !important;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# 제목
# =========================

st.title("🎮 TFT META ANALYZER")

st.subheader(
    "롤토체스 메타 분석 시스템"
)

st.markdown("---")

# =========================
# 수행평가 설명
# =========================

col1, col2 = st.columns([2,1])

with col1:

    st.markdown("""
### 📖 프로젝트 소개

본 프로젝트는 롤토체스(TFT)의
메타 데이터를 분석하여

플레이어에게 현재 강력한 덱과
승률 정보를 제공하는 시스템이다.

### 🎯 개발 목적

- 게임 데이터 분석
- 데이터 시각화
- 메타 연구
- 전략 추천
- 사용자 친화적 UI 구현

### 📊 활용 기술

- Python
- Streamlit
- Pandas
- Plotly
""")

with col2:

    st.info("""
👨‍🏫 수행평가 요소

✔ 데이터 분석

✔ 데이터 시각화

✔ UI 설계

✔ Python 활용

✔ Streamlit 활용
""")

st.markdown("---")

# =========================
# 메타 데이터
# =========================

meta_df = pd.DataFrame({
    "덱":[
        "황금 황소",
        "펭구 포병",
        "사신 리롤",
        "마법사",
        "난동꾼",
        "결투가",
        "집행자"
    ],
    "티어":[
        "S",
        "S",
        "A",
        "A",
        "B",
        "B",
        "C"
    ],
    "승률":[
        58.2,
        57.5,
        55.8,
        54.7,
        52.1,
        51.4,
        49.3
    ],
    "TOP4":[
        84,
        82,
        78,
        76,
        71,
        68,
        60
    ]
})

# =========================
# 카드
# =========================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "🏆 S티어 덱",
        "2개"
    )

with c2:
    st.metric(
        "📈 최고 승률",
        "58.2%"
    )

with c3:
    st.metric(
        "⭐ 최고 TOP4",
        "84%"
    )

with c4:
    st.metric(
        "🎮 분석 덱",
        "7개"
    )

st.markdown("---")

# =========================
# 티어표
# =========================

st.header("🏆 TFT 메타 티어리스트")

st.dataframe(
    meta_df,
    use_container_width=True
)

# =========================
# 승률 그래프
# =========================

st.header("📈 덱 승률 분석")

fig = px.bar(
    meta_df,
    x="덱",
    y="승률",
    color="티어",
    text="승률"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# TOP4 그래프
# =========================

st.header("⭐ TOP4 비율")

fig2 = px.bar(
    meta_df,
    x="덱",
    y="TOP4",
    color="티어",
    text="TOP4"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# 덱 선택
# =========================

st.header("🎯 덱 분석")

deck = st.selectbox(
    "분석할 덱 선택",
    meta_df["덱"]
)

selected = meta_df[
    meta_df["덱"] == deck
].iloc[0]

c1,c2,c3 = st.columns(3)

with c1:
    st.metric(
        "승률",
        f"{selected['승률']}%"
    )

with c2:
    st.metric(
        "TOP4",
        f"{selected['TOP4']}%"
    )

with c3:
    st.metric(
        "티어",
        selected["티어"]
    )

# =========================
# 덱 설명
# =========================

descriptions = {

    "황금 황소":
    "현재 가장 안정적인 메타 덱. 초중후반이 모두 강력함.",

    "펭구 포병":
    "원거리 딜러 중심 조합으로 안정적인 순위 확보 가능.",

    "사신 리롤":
    "저코스트 리롤 전략이 핵심.",

    "마법사":
    "광역 마법 피해가 강력한 조합.",

    "난동꾼":
    "높은 체력을 활용한 탱커 조합.",

    "결투가":
    "빠른 공격속도로 적을 제압.",

    "집행자":
    "후반 캐리력이 좋은 조합."
}

st.success(
    descriptions[deck]
)

# =========================
# 플레이 스타일
# =========================

st.header("🧠 플레이 스타일 추천")

if selected["승률"] >= 57:

    style = "👑 상위권 유지형"

elif selected["승률"] >= 53:

    style = "⚔️ 균형형"

else:

    style = "🎲 공격형"

st.info(
    f"추천 플레이 스타일 : {style}"
)

# =========================
# 종합 평가
# =========================

st.header("📄 종합 평가")

st.info(f"""
현재 선택한 덱은 {deck} 입니다.

티어 : {selected['티어']}

승률 : {selected['승률']}%

TOP4 비율 : {selected['TOP4']}%

현재 메타에서 충분히 경쟁력 있는 조합으로 평가됩니다.

본 시스템은 데이터를 기반으로
메타를 분석하고 시각화하여
사용자가 쉽게 전략을 선택할 수 있도록 설계되었습니다.
""")
