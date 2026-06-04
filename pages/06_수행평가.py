import streamlit as st

st.write(st.secrets)
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="TFT.GG STYLE",
    page_icon="🎮",
    layout="wide"
)

API_KEY = st.secrets["RIOT_API_KEY"]

HEADERS = {
    "X-Riot-Token": API_KEY
}

# ------------------------
# 디자인
# ------------------------

st.markdown("""
<style>

.stApp{
    background:#f5f7fa;
}

[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:15px;
    border:2px solid #60a5fa;
}

</style>
""", unsafe_allow_html=True)

st.title("🎮 TFT.GG STYLE")

game_name = st.text_input("게임명")
tag_line = st.text_input("태그")

if st.button("검색"):

    try:

        # Riot ID → PUUID
        account_url = (
            f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        )

        account = requests.get(
            account_url,
            headers=HEADERS
        ).json()

        puuid = account["puuid"]

        st.success("소환사 조회 성공")

        # 최근 경기 20개
        match_url = (
            f"https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20"
        )

        match_ids = requests.get(
            match_url,
            headers=HEADERS
        ).json()

        placements = []

        for match_id in match_ids:

            detail_url = (
                f"https://asia.api.riotgames.com/tft/match/v1/matches/{match_id}"
            )

            match = requests.get(
                detail_url,
                headers=HEADERS
            ).json()

            participants = match["info"]["participants"]

            for p in participants:

                if p["puuid"] == puuid:

                    placements.append(
                        p["placement"]
                    )

        if len(placements) > 0:

            avg_place = round(
                sum(placements) / len(placements),
                2
            )

            top4 = len(
                [x for x in placements if x <= 4]
            )

            top4_rate = round(
                top4 / len(placements) * 100,
                1
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "TOP4 비율",
                    f"{top4_rate}%"
                )

            with col2:
                st.metric(
                    "평균 등수",
                    avg_place
                )

            df = pd.DataFrame({
                "게임": list(range(1, len(placements)+1)),
                "등수": placements
            })

            fig = px.line(
                df,
                x="게임",
                y="등수",
                markers=True
            )

            fig.update_yaxes(
                autorange="reversed"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(df)

        else:
            st.warning("최근 경기 기록이 없습니다.")

    except Exception as e:
        st.error(
            f"오류 발생: {e}"
        )
