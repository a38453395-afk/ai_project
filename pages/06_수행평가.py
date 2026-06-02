import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="🐾 입양하세요 펫 티어리스트",
    page_icon="🐾",
    layout="wide"
)

st.title("🐾 입양하세요 종합 펫 티어리스트")

# ------------------------
# 데이터
# ------------------------

pets = [
    ("Shadow Dragon","S"),
    ("Bat Dragon","S"),
    ("Frost Dragon","S"),
    ("Giraffe","S"),
    ("Owl","S"),

    ("Parrot","A"),
    ("Evil Unicorn","A"),
    ("Crow","A"),
    ("Arctic Reindeer","A"),
    ("Monkey King","A"),

    ("Turtle","B"),
    ("Kangaroo","B"),
    ("Albino Monkey","B"),
    ("Diamond Unicorn","B"),
    ("Golden Dragon","B"),

    ("Dragon","C"),
    ("Unicorn","C"),
    ("Griffin","C"),
    ("Cerberus","C"),
    ("Robo Dog","C")
]

df = pd.DataFrame(
    pets,
    columns=["펫","티어"]
)

tier_score = {
    "S":4,
    "A":3,
    "B":2,
    "C":1
}

df["점수"] = df["티어"].map(tier_score)

# ------------------------
# 펫 선택
# ------------------------

selected_pet = st.selectbox(
    "🐶 펫 선택",
    df["펫"]
)

pet_info = df[df["펫"] == selected_pet].iloc[0]

tier = pet_info["티어"]

if tier == "S":
    st.success(f"🏆 {selected_pet} : S 티어")
elif tier == "A":
    st.info(f"⭐ {selected_pet} : A 티어")
elif tier == "B":
    st.warning(f"✨ {selected_pet} : B 티어")
else:
    st.error(f"📉 {selected_pet} : C 티어")

# ------------------------
# 검색
# ------------------------

search = st.text_input("🔍 펫 검색")

if search:
    filtered = df[
        df["펫"].str.contains(
            search,
            case=False
        )
    ]
else:
    filtered = df

# ------------------------
# 그래프
# ------------------------

fig = px.bar(
    filtered,
    x="펫",
    y="점수",
    color="티어",
    title="입양하세요 종합 펫 티어리스트",
    category_orders={
        "티어":["S","A","B","C"]
    }
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------
# 티어표
# ------------------------

st.subheader("📋 전체 티어표")

st.dataframe(
    filtered,
    use_container_width=True
)

# ------------------------
# 티어별 보기
# ------------------------

selected_tier = st.selectbox(
    "티어별 보기",
    ["S","A","B","C"]
)

tier_df = df[df["티어"] == selected_tier]

st.dataframe(
    tier_df,
    use_container_width=True
)
