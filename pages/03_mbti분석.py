import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="🌎 국가별 MBTI 분석",
    page_icon="🌈",
    layout="wide"
)

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# 국가 컬럼 찾기
country_col = df.columns[0]

mbti_cols = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# ---------------------------
# 제목
# ---------------------------
st.title("🌎 국가별 MBTI 비율 분석")
st.markdown(
    "국가를 선택하면 해당 국가의 MBTI 비율을 인터랙티브하게 확인할 수 있습니다."
)

# ---------------------------
# 국가 선택
# ---------------------------
country = st.selectbox(
    "🌍 국가 선택",
    sorted(df[country_col].unique())
)

selected = df[df[country_col] == country].iloc[0]

mbti_data = (
    pd.DataFrame({
        "MBTI": mbti_cols,
        "비율": [selected[x] for x in mbti_cols]
    })
    .sort_values("비율", ascending=False)
)

# ---------------------------
# TOP3 카드
# ---------------------------
top3 = mbti_data.head(3)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥇 1위",
        top3.iloc[0]["MBTI"],
        f"{top3.iloc[0]['비율']:.1%}"
    )

with col2:
    st.metric(
        "🥈 2위",
        top3.iloc[1]["MBTI"],
        f"{top3.iloc[1]['비율']:.1%}"
    )

with col3:
    st.metric(
        "🥉 3위",
        top3.iloc[2]["MBTI"],
        f"{top3.iloc[2]['비율']:.1%}"
    )

st.divider()

# ---------------------------
# 색상 설정
# ---------------------------

rainbow = [
    "#ff0000",
    "#ff7f00",
    "#ffff00",
    "#00ff00",
    "#0000ff",
    "#4b0082",
    "#8b00ff"
]

pink_gradient = [
    "#ffe4ec",
    "#ffd1df",
    "#ffbfd2",
    "#ffadc5",
    "#ff9ab8",
    "#ff88ab",
    "#ff76a0",
    "#ff6495",
    "#ff528a",
    "#ff4081",
    "#ff2f76",
    "#ff1d6b",
    "#ff0b60",
    "#ff0055",
    "#ff4d88"
]

colors = []

for i in range(len(mbti_data)):
    if i == 0:
        colors.append(rainbow[i % len(rainbow)])
    else:
        colors.append(
            pink_gradient[
                min(i-1, len(pink_gradient)-1)
            ]
        )

# ---------------------------
# Plotly 그래프
# ---------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_data["MBTI"],
        y=mbti_data["비율"] * 100,
        marker_color=colors,
        text=[
            f"{x:.1f}%"
            for x in mbti_data["비율"] * 100
        ],
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    title=f"📊 {country} MBTI 비율",
    height=650,
    template="plotly_white",
    xaxis_title="MBTI",
    yaxis_title="비율 (%)",
    hovermode="x",
    font=dict(size=14),
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------
# 데이터 테이블
# ---------------------------
with st.expander("📋 MBTI 데이터 보기"):
    display_df = mbti_data.copy()
    display_df["비율"] = (
        display_df["비율"] * 100
    ).round(2)

    st.dataframe(
        display_df,
        use_container_width=True
    )

# ---------------------------
# 설명
# ---------------------------
st.info(
    f"""
    🌈 {country}에서 가장 높은 MBTI는
    **{top3.iloc[0]['MBTI']}**
    ({top3.iloc[0]['비율']:.1%}) 입니다.
    """
)
