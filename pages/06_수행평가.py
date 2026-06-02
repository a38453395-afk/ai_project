import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="TFT.GG",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 TFT.GG 스타일 전적 검색기")

nickname = st.text_input(
    "소환사명 입력"
)

if nickname:

    st.success(f"{nickname} 님의 전적")

    col1, col2, col3 = st.columns(3)

    col1.metric("승률", "62%")
    col2.metric("평균 등수", "3.8")
    col3.metric("TOP4 비율", "74%")

    deck_df = pd.DataFrame({
        "덱": [
            "용술사",
            "집행자",
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

    fig = px.bar(
        deck_df,
        x="덱",
        y="사용횟수",
        color="사용횟수",
        title="자주 사용하는 덱"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    match_df = pd.DataFrame({
        "최근 등수":[
            1,2,4,3,1,7,2,5,1,4
        ]
    })

    fig2 = px.line(
        match_df,
        y="최근 등수",
        markers=True,
        title="최근 경기 기록"
    )

    fig2.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(
        deck_df,
        use_container_width=True
    )
