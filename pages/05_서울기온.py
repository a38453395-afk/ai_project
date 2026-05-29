import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="날짜별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌈 날짜별 기온분석")

# -----------------------------
# CSV 경로
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "seoul.csv"

# -----------------------------
# 파일 존재 확인
# -----------------------------
if not DATA_FILE.exists():
    st.error(f"❌ CSV 파일 없음: {DATA_FILE}")
    st.stop()

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv(DATA_FILE, encoding="cp949")

    except:
        df = pd.read_csv(DATA_FILE, encoding="utf-8")

    # 컬럼 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연/월/일 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# -----------------------------
# 월 / 일 선택
# -----------------------------
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

# -----------------------------
# 데이터 필터링
# -----------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].sort_values("연도")

# -----------------------------
# 그래프 생성
# -----------------------------
fig = go.Figure()

# 최고기온
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
        marker=dict(size=7)
    )
)

# 최저기온
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
        marker=dict(size=7)
    )
)

# 레이아웃
fig.update_layout(
    title="날짜별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도 (℃)",
    hovermode="x unified",
    template="plotly_dark",
    height=700,
    legend=dict(
        orientation="h",
        y=1.1
    )
)

# 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# 데이터 테이블
with st.expander("📊 데이터 보기"):
    st.dataframe(
        filtered[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )
