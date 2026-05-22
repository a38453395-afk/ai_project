import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------------
# 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="서울시 인구통계",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시의 인구통계")

# --------------------------------
# 데이터 불러오기
# --------------------------------
@st.cache_data
def load_data():
    encodings = ["utf-8", "cp949", "euc-kr"]

    for enc in encodings:
        try:
            return pd.read_csv("POPULATION.csv", encoding=enc)
        except:
            pass

    return pd.read_csv("POPULATION.csv")

df = load_data()

# --------------------------------
# 행정구 컬럼
# --------------------------------
district_col = df.columns[0]

# --------------------------------
# 행정구 선택
# --------------------------------
district = st.selectbox(
    "🏙️ 행정구를 선택하세요",
    df[district_col].unique()
)

row = df[df[district_col] == district].iloc[0]

# --------------------------------
# 2026.04 연령대 컬럼 추출
# --------------------------------
age_cols = []

for col in df.columns:
    if "2026.04" in str(col):
        if "계" not in str(col):
            age_cols.append(col)

# --------------------------------
# 연령대 / 인구수
# --------------------------------
ages = []
values = []

for col in age_cols:

    age = col.split(".")[-1]
    ages.append(age)

    value = str(row[col]).replace(",", "")

    try:
        value = int(float(value))
    except:
        value = 0

    values.append(value)

# --------------------------------
# 무지개 색상
# --------------------------------
rainbow_colors = [
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "indigo",
    "violet",
    "deeppink",
    "cyan",
    "lime",
    "gold"
]

# --------------------------------
# 꺾은선 그래프
# --------------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ages,
        y=values,
        mode="lines+markers",
        line=dict(
            width=5,
            color="red"
        ),
        marker=dict(
            size=12,
            color=rainbow_colors[:len(ages)]
        ),
        name=district
    )
)

# 무지개 배경
fig.update_layout(
    title={
        "text": "서울시의 인구통계",
        "x": 0.5
    },
    xaxis_title="연령대",
    yaxis_title="인구수",
    height=650,
    plot_bgcolor="rgba(240,240,240,1)",
    paper_bgcolor="white",
    font=dict(
        family="Malgun Gothic"
    )
)

# 배경 무지개 띠
for i, color in enumerate(rainbow_colors):
    fig.add_vrect(
        x0=i-0.5,
        x1=i+0.5,
        fillcolor=color,
        opacity=0.08,
        layer="below",
        line_width=0
    )

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# 표
# --------------------------------
st.subheader("📋 연령대별 인구수")

result_df = pd.DataFrame({
    "연령대": ages,
    "인구수": values
})

st.dataframe(
    result_df,
    use_container_width=True
)
