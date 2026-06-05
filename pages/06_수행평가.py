import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="TFT 전적 분석 시스템",
    page_icon="🎮",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #f8fbff,
        #eef7ff,
        #ffffff
    );
}

h1,h2,h3{
    color:#1e293b;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# 소개
# =========================

st.title("🎮 TFT 데이터 분석 시스템")

st.subheader(
    "Riot API를 활용한 롤토체스 전적 분석"
)

col1, col2 = st.columns([2,1])

with col1:

    st.markdown("""
### 📖 프로젝트 소개

본 프로젝트는 Riot Games API를 활용하여
롤토체스(TFT) 플레이어의 전적 데이터를
수집하고 분석하는 시스템이다.

### 🎯 개발 목적

- Riot API 활용
- 데이터 수집
- 데이터 분석
- 데이터 시각화
- 플레이 스타일 분석

### 📊 분석 내용

✅ 평균 등수

✅ TOP4 비율

✅ 우승 횟수

✅ 최근 경기 분석

✅ 등수 분포

✅ 플레이 스타일 분석

✅ 종합 평가
""")

with col2:

    st.info("""
👨‍🏫 수행평가 요소

✔ API 활용

✔ 데이터 수집

✔ 데이터 시각화

✔ 데이터 분석

✔ 웹 프로그래밍
""")

st.markdown("---")

# =========================
# API
# =========================

API_KEY = st.secrets["RIOT_API_KEY"]

HEADERS = {
    "X-Riot-Token": API_KEY
}

# =========================
# 검색
# =========================

st.header("🔍 플레이어 검색")

game_name = st.text_input(
    "게임명"
)

tag_line = st.text_input(
    "태그"
)

# =========================
# 조회
# =========================

if st.button("전적 분석 시작"):

    try:

        # ---------------------
        # 계정 조회
        # ---------------------

        account_url = (
            f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        )

        account = requests.get(
            account_url,
            headers=HEADERS
        ).json()

        puuid = account["puuid"]

        st.success("✅ 계정 조회 성공")

        # ---------------------
        # 최근 경기 조회
        # ---------------------

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

            participants = (
                match["info"]["participants"]
            )

            for p in participants:

                if p["puuid"] == puuid:

                    placements.append(
                        p["placement"]
                    )

        # ---------------------
        # 데이터 분석
        # ---------------------

        if len(placements) > 0:

            avg_place = round(
                sum(placements) / len(placements),
                2
            )

            wins = len(
                [x for x in placements if x == 1]
            )

            top4 = len(
                [x for x in placements if x <= 4]
            )

            top4_rate = round(
                top4 / len(placements) * 100,
                1
            )

            win_rate = round(
                wins / len(placements) * 100,
                1
            )

            # ---------------------
            # 카드
            # ---------------------

            st.markdown("## 📊 핵심 지표")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "🏆 평균 등수",
                    avg_place
                )

            with c2:
                st.metric(
                    "⭐ TOP4 비율",
                    f"{top4_rate}%"
                )

            with c3:
                st.metric(
                    "🥇 우승 횟수",
                    wins
                )

            with c4:
                st.metric(
                    "🎮 경기 수",
                    len(placements)
                )

            # ---------------------
            # 플레이 스타일
            # ---------------------

            if avg_place <= 3.5:

                style = "👑 상위권 유지형"

            elif avg_place <= 4.5:

                style = "⚔️ 균형형"

            else:

                style = "🎲 공격적 운영형"

            st.success(
                f"플레이 스타일 분석 결과 : {style}"
            )

            # ---------------------
            # 경기 데이터
            # ---------------------

            df = pd.DataFrame({
                "게임": range(
                    1,
                    len(placements)+1
                ),
                "등수": placements
            })

            # ---------------------
            # 그래프
            # ---------------------

            st.markdown("## 📈 최근 경기 등수 변화")

            fig = px.line(
                df,
                x="게임",
                y="등수",
                markers=True,
                title="최근 경기 등수 변화"
            )

            fig.update_yaxes(
                autorange="reversed"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ---------------------
            # 분포 그래프
            # ---------------------

            st.markdown("## 📊 등수 분포")

            rank_df = pd.DataFrame({
                "등수":[1,2,3,4,5,6,7,8],
                "횟수":[
                    placements.count(1),
                    placements.count(2),
                    placements.count(3),
                    placements.count(4),
                    placements.count(5),
                    placements.count(6),
                    placements.count(7),
                    placements.count(8)
                ]
            })

            fig2 = px.bar(
                rank_df,
                x="등수",
                y="횟수",
                text="횟수",
                title="등수 분포 분석"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            # ---------------------
            # 최근 경기 테이블
            # ---------------------

            st.markdown("## 📋 최근 경기 기록")

            st.dataframe(
                df,
                use_container_width=True
            )

            # ---------------------
            # 종합 평가
            # ---------------------

            score = (
                100 - avg_place * 10
            )

            if score >= 80:
                grade = "A"

            elif score >= 70:
                grade = "B"

            elif score >= 60:
                grade = "C"

            else:
                grade = "D"

            st.markdown("## 📄 종합 평가")

            st.info(f"""
플레이어 분석 결과

평균 등수 : {avg_place}등

TOP4 비율 : {top4_rate}%

우승 횟수 : {wins}회

플레이 스타일 : {style}

종합 등급 : {grade}

최근 경기 데이터를 분석한 결과
안정적인 경기력을 보이고 있으며
데이터 기반 플레이 분석이 가능합니다.
""")

        else:

            st.warning(
                "전적 데이터를 찾을 수 없습니다."
            )

    except Exception as e:

        st.error(
            f"오류 발생 : {e}"
        )
