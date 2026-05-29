import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="날짜별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 날짜별 기온분석")

# CSV 읽기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul(1).csv", encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# -----------------------
# 날짜 선택
# -----------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox(
        "월 선택",
        sorted(df["월"].unique())
    )

with col2:
    day = st.selectbox(
        "일 선택",
        sorted(
            df[df["월"] == month]["일"].unique()
        )
    )

# 데이터 필터링
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

st.write(
    f"📅 선택 날짜 : **{month}월 {day}일**"
)

if filtered.empty:
    st.warning("데이터가 없습니다.")
    st.stop()

# -----------------------
# Plotly 그래프
# -----------------------
fig = go.Figure()

# 최고기온 Glow 효과
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최고기온(℃)"],
        mode="lines",
        line=dict(
            width=12,
            color="rgba(255,255,255,0.15)"
        ),
        showlegend=False,
        hoverinfo="skip"
    )
)

# 최고기온 (무지개)
rainbow_colors = [
    "#ff0000",
    "#ff7f00",
    "#ffff00",
    "#00ff00",
    "#0000ff",
    "#4b0082",
    "#9400d3"
]

for i in range(len(filtered)-1):
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"].iloc[i:i+2],
            y=filtered["최고기온(℃)"].iloc[i:i+2],
            mode="lines",
            line=dict(
                width=5,
                color=rainbow_colors[i % len(rainbow_colors)]
            ),
            showlegend=False
        )
    )

# 범례용 최고기온
fig.add_trace(
    go.Scatter(
        x=[None],
        y=[None],
        mode="lines",
        line=dict(
            color="red",
            width=5
        ),
        name="최고기온"
    )
)

# 최저기온 Glow 효과
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최저기온(℃)"],
        mode="lines",
        line=dict(
            width=12,
            color="rgba(255,215,0,0.25)"
        ),
        showlegend=False,
        hoverinfo="skip"
    )
)

# 황금빛 무지개
gold_rainbow = [
    "#FFD700",
    "#FFEC80",
    "#FFF5B1",
    "#FFE066",
    "#FFC107",
    "#FFB300",
    "#FFD54F"
]

for i in range(len(filtered)-1):
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"].iloc[i:i+2],
            y=filtered["최저기온(℃)"].iloc[i:i+2],
            mode="lines",
            line=dict(
                width=5,
                color=gold_rainbow[i % len(gold_rainbow)]
            ),
            showlegend=False
        )
    )

# 범례용 최저기온
fig.add_trace(
    go.Scatter(
        x=[None],
        y=[None],
        mode="lines",
        line=dict(
            color="gold",
            width=5
        ),
        name="최저기온"
    )
)

# 레이아웃
fig.update_layout(
    title="날짜별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도 (℃)",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        y=1.1
    ),
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 데이터 표시
with st.expander("📊 데이터 보기"):
    st.dataframe(
        filtered[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )
