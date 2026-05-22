import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울시 인구통계",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시의 인구통계")

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("POPULATION.csv", encoding="cp949")
    return df

df = load_data()

# -----------------------------
# 행정구 컬럼 찾기
# -----------------------------
district_col = df.columns[0]

# -----------------------------
# 연령대 컬럼 추출
# (2026.04 기준만 사용)
# -----------------------------
age_columns = [col for col in df.columns if "2026.04" in col]

# 총인구 제외
age_columns = [
    col for col in age_columns
    if "계" not in col
]

# -----------------------------
# 행정구 선택
# -----------------------------
districts = df[district_col].unique()

selected_district = st.selectbox(
    "🏙️ 행정구를 선택하세요",
    districts
)

# -----------------------------
# 선택 데이터
# -----------------------------
selected_row = df[df[district_col] == selected_district].iloc[0]

ages = []
values = []

for col in age_columns:
    age_name = col.split(".")[-1]
    ages.append(age_name)

    value = str(selected_row[col]).replace(",", "")
    values.append(int(float(value)))

# -----------------------------
# 무지개 배경 생성
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

ax.imshow(
    gradient,
    aspect="auto",
    cmap="rainbow",
    extent=[-0.5, len(ages)-0.5, 0, max(values)*1.1],
    alpha=0.35
)

# -----------------------------
# 무지개 색 선 그래프
# -----------------------------
colors = plt.cm.rainbow(
    np.linspace(0, 1, len(ages))
)

for i in range(len(ages)-1):
    ax.plot(
        ages[i:i+2],
        values[i:i+2],
        color=colors[i],
        linewidth=4
    )

ax.scatter(
    ages,
    values,
    c=colors,
    s=100
)

# -----------------------------
# 그래프 꾸미기
# -----------------------------
ax.set_title(
    "서울시의 인구통계",
    fontsize=20,
    fontweight="bold"
)

ax.set_xlabel("연령대", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

ax.grid(True, linestyle="--", alpha=0.4)

plt.xticks(rotation=20)

st.pyplot(fig)

# -----------------------------
# 데이터 표
# -----------------------------
st.subheader("📋 연령대별 인구수")

result_df = pd.DataFrame({
    "연령대": ages,
    "인구수": values
})

st.dataframe(
    result_df,
    use_container_width=True
)
