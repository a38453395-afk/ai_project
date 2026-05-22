import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="서울시의 인구통계",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시의 인구통계")

# --------------------
# CSV 읽기
# --------------------
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

# 디버그용
with st.expander("CSV 컬럼 확인"):
    st.write(df.columns.tolist())

# --------------------
# 행정구 컬럼
# --------------------
district_col = df.columns[0]

district = st.selectbox(
    "행정구 선택",
    df[district_col].unique()
)

row = df[df[district_col] == district].iloc[0]

# --------------------
# 연령대 컬럼 찾기
# --------------------
age_cols = []

patterns = [
    r"0.*9",
    r"10.*19",
    r"20.*29",
    r"30.*39",
    r"40.*49",
    r"50.*59",
    r"60.*69",
    r"70.*79",
    r"80.*89",
    r"90.*99",
    r"100"
]

for col in df.columns:

    text = str(col)

    for p in patterns:

        if re.search(p, text):
            age_cols.append(col)
            break

# 중복 제거
age_cols = list(dict.fromkeys(age_cols))

# --------------------
# 데이터 생성
# --------------------
ages = []
values = []

for col in age_cols:

    ages.append(str(col))

    try:
        value = int(str(row[col]).replace(",", ""))
    except:
        value = 0

    values.append(value)

# 컬럼 못 찾았을 때
if len(ages) == 0:
    st.error("연령대 컬럼을 찾지 못했습니다.")
    st.stop()

# --------------------
# 그래프
# --------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ages,
        y=values,
        mode="lines+markers",
        line=dict(width=5),
        marker=dict(size=10)
    )
)

fig.update_layout(
    title="서울시의 인구통계",
    xaxis_title="연령대",
    yaxis_title="인구수",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 표
result = pd.DataFrame({
    "연령대": ages,
    "인구수": values
})

st.dataframe(result, use_container_width=True)
