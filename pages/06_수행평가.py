import streamlit as st
import requests
import pandas as pd

# Streamlit Secrets
API_KEY = st.secrets["RIOT_API_KEY"]

st.set_page_config(
    page_title="TFT.GG Mini",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 TFT 전적 검색기")

game_name = st.text_input("소환사명")
tag_line = st.text_input("태그")

if st.button("검색"):

    try:

        # Riot ID → PUUID
        account_url = (
            f"https://asia.api.riotgames.com/riot/account/v1/accounts"
            f"/by-riot-id/{game_name}/{tag_line}"
        )

        headers = {
            "X-Riot-Token": API_KEY
        }

        account = requests.get(
            account_url,
            headers=headers
        ).json()

        puuid = account["puuid"]

        # 최근 20게임
        match_url = (
            f"https://asia.api.riotgames.com/tft/match/v1/matches"
            f"/by-puuid/{puuid}/ids?count=20"
        )

        match_ids = requests.get(
            match_url,
            headers=headers
        ).json()

        placements = []
        traits = []

        for match_id in match_ids:

            detail_url = (
                f"https://asia.api.riotgames.com/tft/match/v1/matches/{match_id}"
            )

            match = requests.get(
                detail_url,
                headers=headers
            ).json()

            participants = match["info"]["participants"]

            for p in participants:

                if p["puuid"] == puuid:

                    placements.append(
                        p["placement"]
                    )

                    comp = []

                    for t in p["traits"]:

                        if t["tier_current"] > 0:
                            comp.append(t["name"])

                    traits.append(
                        ", ".join(comp[:5])
                    )

        avg_place = round(
            sum(placements) / len(placements),
            2
        )

        top4 = len(
            [x for x in placements if x <= 4]
        )

        win_rate = round(
            top4 / len(placements) * 100,
            1
        )

        st.metric(
            "Top4 비율",
            f"{win_rate}%"
        )

        st.metric(
            "평균 등수",
            avg_place
        )

        df = pd.DataFrame({
            "등수": placements,
            "덱": traits
        })

        st.subheader("최근 경기")

        st.dataframe(
            df,
            use_container_width=True
        )

    except Exception as e:
        st.error(
            "검색 실패. 닉네임/태그 또는 API 키를 확인하세요."
        )
