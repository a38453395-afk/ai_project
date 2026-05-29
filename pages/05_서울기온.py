import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="날짜별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌈 날짜별 기온분석")

# -----------------------------------
# CSV 경로
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "seoul.csv"

# -----------------------------------
# 파일 존재 확인
# -----------------------------------
if not DATA_FILE.exists():

    st.error(f"❌ CSV 파일 없음\n\n{DATA_FILE}")
    st.stop()

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv(DATA_FILE, encoding="cp949")

    except:
        df = pd.read_csv(DATA_FILE, encoding="utf-8")

    # 컬럼 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=["날짜"])

    # 숫자 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    # 결측값 제거
    df = df.dropna(
        subset=["최고기온(℃)", "최저기온(℃)"]
    )

    # 연/월/일 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

# 데이터 로드
df = load_data()

# -----------------------------------
# 날짜 선택
# -----------------------------------
col1, col2 = st.columns(2)

with col1:

    month = st.selectbox(
        "📅 월 선택",
        sorted(df["월"].unique())
    )

with col2:

    available_days = sorted(
        df[df["월"] == month]["일"].unique()
    )

    day = st.selectbox(
        "📌 일 선택",
        available_days
    )

# -----------------------------------
# 미래 연도 선택
# -----------------------------------
future_year = st.number_input(
    "🔮 미래 연도 예측",
    min_value=2026,
    max_value=2100,
    value=2035
)

# -----------------------------------
# 데이터 필터링
# -----------------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].sort_values("연도")

# -----------------------------------
# 예측 계산
# -----------------------------------
x = filtered["연도"]
y_max = filtered["최고기온(℃)"]
y_min = filtered["최저기온(℃)"]

# 선형 회귀
max_coef = np.polyfit(x, y_max, 1)
min_coef = np.polyfit(x, y_min, 1)

pred_max = np.poly1d(max_coef)(future_year)
pred_min = np.poly1d(min_coef)(future_year)

# -----------------------------------
# 예측 결과 출력
# -----------------------------------
st.subheader(f"🔮 {future_year}년 예측 결과")

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "🌈 예상 최고기온",
        f"{pred_max:.1f} ℃"
    )

with col4:
    st.metric(
        "✨ 예상 최저기온",
        f"{pred_min:.1f} ℃"
    )

# -----------------------------------
# 그래프 생성
# -----------------------------------
fig = go.Figure()

# 최고기온 Glow
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최고기온(℃)"],
        mode="lines",
        line=dict(
            width=12,
            color="rgba(255,0,150,0.15)"
        ),
        showlegend=False,
        hoverinfo="skip"
    )
)

# 최고기온 메인
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온 🌈",
        line=dict(
            width=5,
            color="#ff1493"
        ),
        marker=dict(size=8),

        # 마우스 올렸을 때 표시
        hovertemplate=
        "<b>연도:</b> %{x}<br>" +
        "<b>최고기온:</b> %{y:.1f}℃<extra></extra>"
    )
)

# 최저기온 Glow
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최저기온(℃)"],
        mode="lines",
        line=dict(
            width=12,
            color="rgba(255,215,0,0.2)"
        ),
        showlegend=False,
        hoverinfo="skip"
    )
)

# 최저기온 메인
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온 ✨",
        line=dict(
            width=5,
            color="#FFD700"
        ),
        marker=dict(size=8),

        # 마우스 올렸을 때 표시
        hovertemplate=
        "<b>연도:</b> %{x}<br>" +
        "<b>최저기온:</b> %{y:.1f}℃<extra></extra>"
    )
)

# -----------------------------------
# 미래 예측 점 추가
# -----------------------------------
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers+text",
        name="예상 최고기온 🔮",
        marker=dict(
            size=16,
            color="cyan"
        ),
        text=[f"{pred_max:.1f}℃"],
        textposition="top center",

        hovertemplate=
        "<b>예측 연도:</b> %{x}<br>" +
        "<b>예상 최고기온:</b> %{y:.1f}℃<extra></extra>"
    )
)

fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers+text",
        name="예상 최저기온 🔮",
        marker=dict(
            size=16,
            color="lime"
        ),
        text=[f"{pred_min:.1f}℃"],
        textposition="bottom center",

        hovertemplate=
        "<b>예측 연도:</b> %{x}<br>" +
        "<b>예상 최저기온:</b> %{y:.1f}℃<extra></extra>"
    )
)

# -----------------------------------
# 레이아웃
# -----------------------------------
fig.update_layout(

    title={
        "text": "🌡️ 날짜별 기온분석",
        "x": 0.5
    },

    xaxis_title="연도",
    yaxis_title="온도 (℃)",

    template="plotly_dark",

    hovermode="closest",

    height=750,

    legend=dict(
        orientation="h",
        y=1.1
    )
)

# -----------------------------------
# 그래프 출력
# -----------------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# 데이터 보기
# -----------------------------------
with st.expander("📊 데이터 보기"):

    st.dataframe(
        filtered[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )
