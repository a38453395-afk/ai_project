import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="TFT.GG STYLE",
    page_icon="🎮",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background-color:#f5f7fa;
}

.block-container{
    padding-top:1rem;
}

h1,h2,h3,h4{
    color:#1e293b;
}

[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:15px;
    border:2px solid #60a5fa;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------
st.markdown("""
<h1 style='text-align:center;color:#2563eb;'>
🎮 TFT.GG STYLE
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;font-size:18px;color:gray'>
롤체지지 스타일 전적 검색기
</div>
""", unsafe_allow_html=True)

st.write("")

nickname = st.text_input(
    "🔍 소환사명 입력",
    placeholder="예: Faker"
)

if nickname:

    # -----------------------------
    # 프로필 카드
    # -----------------------------
    st.markdown(f"""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    border:2px solid #60a5fa;
    box-shadow:0px 5px 15px rgba(0,0,0,0.08);
    ">
    
    <h2 style='color:#2563eb'>
    🎮 {nickname}
    </h2>

    <h3 style='color:#f59e0b'>
    🏆 DIAMOND II
    </h3>

    <p>
    🔥 최근 상승세 +127 LP
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------
    # 통계 카드
    # -----------------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "승률",
            "62%"
        )

    with c2:
        st.metric(
            "TOP4 비율",
            "74%"
        )

    with c3:
        st.metric(
            "평균 등수",
            "3.8"
        )

    st.divider()
        # -----------------------------
    # 주력 챔피언
    # -----------------------------
    st.subheader("⭐ 주력 챔피언")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image(
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt1e4f6c7b4f4a0f75/64d2d6b6e5f9e85a4c7d2d7a/TFT_Champions.jpg",
            use_container_width=True
        )
        st.caption("🌪️ 야스오 ⭐⭐⭐")

    with col2:
        st.image(
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt1e4f6c7b4f4a0f75/64d2d6b6e5f9e85a4c7d2d7a/TFT_Champions.jpg",
            use_container_width=True
        )
        st.caption("💥 징크스 ⭐⭐")

    with col3:
        st.image(
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt1e4f6c7b4f4a0f75/64d2d6b6e5f9e85a4c7d2d7a/TFT_Champions.jpg",
            use_container_width=True
        )
        st.caption("🏹 애쉬 ⭐⭐")

    with col4:
        st.image(
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt1e4f6c7b4f4a0f75/64d2d6b6e5f9e85a4c7d2d7a/TFT_Champions.jpg",
            use_container_width=True
        )
        st.caption("🛡️ 레오나 ⭐⭐⭐")

    st.divider()

    # -----------------------------
    # 추천 아이템
    # -----------------------------
    st.subheader("🧪 추천 아이템")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.metric("⚔️ 무한의 대검", "+35 AD")

    with i2:
        st.metric("🏹 고속 연사포", "+공속")

    with i3:
        st.metric("🔥 라바돈", "+주문력")

    st.divider()
    # -----------------------------
    # 추천 배치도
    # -----------------------------
    st.subheader("🗺️ 추천 배치도")

    st.markdown("""
    <div style="
    background:white;
    padding:20px;
    border-radius:20px;
    border:2px solid #60a5fa;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
    ">

    <h4>전열</h4>

    🛡️ 레오나 &nbsp;&nbsp;&nbsp;&nbsp; 🛡️ 세트

    <br><br>

    <h4>중열</h4>

    ⚔️ 야스오 &nbsp;&nbsp;&nbsp;&nbsp; ⚔️ 요네

    <br><br>

    <h4>후열</h4>

    🏹 애쉬 &nbsp;&nbsp;&nbsp;&nbsp; 💥 징크스

    </div>
    """, unsafe_allow_html=True)

    st.divider()
        # -----------------------------
    # 최근 경기 그래프
    # -----------------------------
    st.subheader("📈 최근 경기 기록")

    match_df = pd.DataFrame({
        "게임": list(range(1, 11)),
        "등수": [1, 2, 4, 3, 1, 7, 2, 5, 1, 4]
    })

    fig = px.line(
        match_df,
        x="게임",
        y="등수",
        markers=True,
        title="최근 10게임 성적"
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

    # -----------------------------
    # 자주 사용하는 덱
    # -----------------------------
    st.subheader("🏆 자주 사용하는 덱")

    deck_df = pd.DataFrame({
        "덱": [
            "집행자",
            "용술사",
            "난동꾼",
            "요새",
            "마법사"
        ],
        "사용횟수": [
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

    # -----------------------------
    # 최근 전적
    # -----------------------------
    st.subheader("📋 최근 경기")

    history_df = pd.DataFrame({
        "등수": [1,2,4,3,1,7,2,5,1,4],
        "사용 덱": [
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
        ],
        "LP 변화": [
            "+42",
            "+31",
            "+18",
            "+24",
            "+39",
            "-28",
            "+33",
            "-12",
            "+44",
            "+17"
        ]
    })

    st.dataframe(
        history_df,
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # 플레이어 분석
    # -----------------------------
    st.subheader("🎯 플레이 스타일 분석")

    st.success("""
    ✔️ 공격적인 플레이 선호

    ✔️ 평균 순위 상위권 유지

    ✔️ 집행자 계열 덱 선호

    ✔️ 후반 운영 능력 우수
    """)

else:

    st.info("🔍 소환사명을 입력해보세요!")
