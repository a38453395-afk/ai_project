import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

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
# CSV 경로 설정
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "seoul.csv"

# -----------------------------------
# CSV 파일 존재 확인
# -----------------------------------
if not DATA_FILE.exists():

    st.error(
        f"""
❌ seoul.csv 파일을 찾을 수 없습니다.

현재 찾는 위치:
{DATA_FILE}

📌 해결 방법:
1. 파일 이름을 seoul.csv 로 변경
2. Home.py 와 같은 위치에 넣기
"""
    )

    st.stop()

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():

    # CSV 읽기
    try:
        df = pd.read_csv(DATA_FILE, encoding="cp949")

    except:
        df = pd.read_csv(DATA_FILE, encoding="utf-8")

    # 컬럼명 공백 제거
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
# 월 / 일 선택
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
# 데이터 필터링
# -----------------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].sort_values("연도")

# 데이터 없을 때
if filtered.empty:

    st.warning("⚠️ 해당 날짜 데이터가 없습니다.")
    st.stop()

# -----------------------------------
# 그래프 생성
# -----------------------------------
fig = go.Figure()

# 최고기온 Glow 효과
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

# 최고기온 메인 라인
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
        marker=dict(
            size=8
        )
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
            color="rgba(255,215,0,0.2)"
        ),
        showlegend=False,
        hoverinfo="skip"
    )
)

# 최저기온 메인 라인
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
        marker=dict(
            size=8
        )
    )
)

# -----------------------------------
# 레이아웃 설정
# -----------------------------------
fig.update_layout(

    title={
        "text": "🌡️ 날짜별 기온분석",
        "x": 0.5,
        "xanchor": "center"
    },

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

# -----------------------------------
# 그래프 출력
# -----------------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# 데이터 테이블
# -----------------------------------
with st.expander("📊 데이터 보기"):

    st.dataframe(
        filtered[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )
