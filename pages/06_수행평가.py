import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="TFT.GG STYLE", layout="wide")

API_KEY = st.secrets["RIOT_API_KEY"]

HEADERS = {
    "X-Riot-Token": API_KEY
}

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

        st.success("계정 조회 성공")

        # 최근 매치 20개
        match_url = (
            f"https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20"
        )

        match_ids = requests.get(
            match_url,
            headers=HEADERS
        ).json()

        st.write("최근 경기 수:", len(match_ids))

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

        if len(placements):

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

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "평균 등수",
                    avg_place
                )

            with c2:
                st.metric(
                    "TOP4 비율",
                    f"{top4_rate}%"
                )

            df = pd.DataFrame({
                "게임": range(1, len(placements)+1),
                "등수": placements
            })

            st.line_chart(
                df.set_index("게임")
            )

            st.dataframe(df)

        else:

            st.warning("전적 없음")

    except Exception as e:

        st.error(str(e))
