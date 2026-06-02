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
# 밝은 테마 CSS
# ------------------------
st.markdown("""
<style>

.stApp{
    background-color:#f5f7fa;
}

h1,h2,h3,h4,label{
    color:#1e293b !important;
}

[data-testid="stMetric"]{
    background:white;
    padding:20px;
    border-radius:20px;
    border:2px solid #60a5fa;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
}

div[data-testid="stDataFrame"]{
    background:white;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# 제목
# ------------------------
st.markdown("""
<h1 style='text-align:center;color:#2563eb;'>
🎮 TFT.GG STYLE
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;color:gray;margin-bottom:20px;'>
롤체지지 스타일 전적 검색기
</div>
""", unsafe_allow_html=True)

# ------------------------
# 검색창
# ------------------------
nickname = st.text_input(
    "🔍 소환사명 입력",
    placeholder="예: Faker"
)

if nickname:

    # ------------------------
    # 프로필 카드
    # ------------------------
    st.markdown(f"""
    <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        border:2px solid #60a5fa;
        box-shadow:0 4px 12px rgba(0,0,0,0.1);
        margin-bottom:20px;
    ">
        <h2 style="color:#2563eb;">
            🎮 {nickname}
        </h2>

        <h4 style="color:#f59e0b;">
            🏆 Diamond II
        </h4>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------
    # 통계 카드
    # ------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "승률",
            "62%"
        )

    with col2:
        st.metric(
            "TOP4 비율",
            "74%"
        )

    with col3:
        st.metric(
            "평균 등수",
            "3.8"
        )

    st.divider()

    # ------------------------
    # 대표 챔피언
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
        markers=True,
        title="최근 10게임"
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        font_color="black",
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
        color="사용횟수",
        title="TOP 5 덱"
    )

    deck_fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        font_color="black",
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

else:
    st.info("소환사명을 입력해보세요 😎")
