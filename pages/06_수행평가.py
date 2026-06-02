import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# 페이지 설정
# ------------------------
st.set_page_config(
    page_title="TFT.GG STYLE",
    page_icon="🎮",
    layout="wide"
)

# ------------------------
# CSS
# ------------------------
st.markdown("""
<style>

.stApp{
    background-color:#0d1117;
}

h1,h2,h3,h4,label{
    color:white !important;
}

[data-testid="stMetric"]{
    background:#161b22;
    padding:20px;
    border-radius:15px;
    border:1px solid #30363d;
}

[data-testid="stDataFrame"]{
    background:#161b22;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# 제목
# ------------------------
st.markdown(
    "<h1 style='text-align:center;'>🎮 TFT.GG STYLE</h1>",
    unsafe_allow_html=True
)

nickname = st.text_input(
    "소환사명 입력",
    placeholder="예: Faker"
)

if nickname:

    st.markdown(f"""
    <div style="
        background:#161b22;
        padding:20px;
        border-radius:20px;
        margin-bottom:20px;
        color:white;
    ">
        <h2>🎮 {nickname}</h2>
        <h4>🏆 Diamond II</h4>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------
    # 통계 카드
    # ------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("승률", "62%")

    with col2:
        st.metric("TOP4 비율", "74%")

    with col3:
        st.metric("평균 등수", "3.8")

    st.divider()

    # ------------------------
    # 챔피언 이미지
    # ------------------------
    st.subheader("⭐ 대표 챔피언")

    st.image(
        "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Yasuo_0.jpg",
        use_container_width=True
    )

    st.divider()

    # ------------------------
    # 최근 경기 그래프
    # ------------------------
    st.subheader("📈 최근 경기 기록")

    match_df = pd.DataFrame({
        "게임": list(range(1,11)),
        "등수":[1,2,4,3,1,7,2,5,1,4]
    })

    fig = px.line(
        match_df,
        x="게임",
        y="등수",
        markers=True
    )

    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        font_color="white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ------------------------
    # 덱 통계
    # ------------------------
    st.subheader("🏆 자주 사용하는 덱")

    deck_df = pd.DataFrame({
        "덱":[
            "집행자",
            "용술사",
            "난동꾼",
            "요새",
            "마법사"
        ],
        "사용횟수":[
            15,
            12,
            10,
            8,
            5
        ]
    })

    deck_fig = px.bar(
        deck_df,
        x="덱",
        y="사용횟수",
        color="사용횟수"
    )

    deck_fig.update_layout(
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        font_color="white",
        height=500
    )

    st.plotly_chart(
        deck_fig,
        use_container_width=True
    )

    st.divider()

    # ------------------------
    # 최근 전적
    # ------------------------
    st.subheader("📋 최근 경기")

    history_df = pd.DataFrame({
        "등수":[1,2,4,3,1,7,2,5,1,4],
        "덱":[
            "집행자",
            "용술사",
            "집행자",
            "난동꾼",
            "집행자",
            "요새",
            "용술사",
            "마법사",
            "집행자",
            "난동꾼"
        ]
    })

    st.dataframe(
        history_df,
        use_container_width=True
    )
