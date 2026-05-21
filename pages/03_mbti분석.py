import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="MBTI 국가 TOP10",
    page_icon="🌎",
    layout="wide"
)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

country_col = df.columns[0]

mbti_cols = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🌎 MBTI 유형별 국가 TOP10")
st.markdown(
    """
원하는 MBTI를 선택하면  
해당 MBTI 비율이 가장 높은 국가 TOP10을 확인할 수 있습니다.
"""
)

# --------------------------------------------------
# MBTI 선택
# --------------------------------------------------
selected_mbti = st.selectbox(
    "🧠 MBTI 선택",
    mbti_cols
)

# --------------------------------------------------
# TOP10 국가 추출
# --------------------------------------------------
top10 = (
    df[[country_col, selected_mbti]]
    .sort_values(selected_mbti, ascending=False)
    .head(10)
)

top10.columns = ["국가", "비율"]

# --------------------------------------------------
# TOP3 카드
# --------------------------------------------------
st.subheader(f"🏆 {selected_mbti} TOP3 국가")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥇 1위",
        top10.iloc[0]["국가"],
        f"{top10.iloc[0]['비율']:.2%}"
    )

with col2:
    st.metric(
        "🥈 2위",
        top10.iloc[1]["국가"],
        f"{top10.iloc[1]['비율']:.2%}"
    )

with col3:
    st.metric(
        "🥉 3위",
        top10.iloc[2]["국가"],
        f"{top10.iloc[2]['비율']:.2%}"
    )

st.divider()

# --------------------------------------------------
# 색상 설정
# --------------------------------------------------

rainbow_color = "#8A2BE2"

pink_gradient = [
    "#ffd6e7",
    "#ffc2db",
    "#ffaecf",
    "#ff9ac3",
    "#ff86b7",
    "#ff72ab",
    "#ff5e9f",
    "#ff4a93",
    "#ff3687"
]

colors = [rainbow_color] + pink_gradient

# --------------------------------------------------
# 그래프
# --------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=top10["국가"],
        y=top10["비율"] * 100,
        marker_color=colors,

        text=[
            f"{v:.2f}%"
            for v in top10["비율"] * 100
        ],

        textposition="outside",

        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    title=f"🌈 {selected_mbti} 비율이 높은 국가 TOP10",
    template="plotly_white",
    height=650,

    xaxis_title="국가",
    yaxis_title="비율 (%)",

    showlegend=False,

    font=dict(
        size=14
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# 데이터 테이블
# --------------------------------------------------
with st.expander("📋 TOP10 데이터 보기"):

    display_df = top10.copy()

    display_df["비율"] = (
        display_df["비율"] * 100
    ).round(2)

    display_df.columns = [
        "국가",
        "비율 (%)"
    ]

    st.dataframe(
        display_df,
        use_container_width=True
    )

# --------------------------------------------------
# 하단 설명
# --------------------------------------------------
st.success(
    f"✨ {selected_mbti} 비율이 가장 높은 국가는 "
    f"{top10.iloc[0]['국가']} "
    f"({top10.iloc[0]['비율']:.2%}) 입니다."
)
