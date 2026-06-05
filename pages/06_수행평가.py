import streamlit as st

key = st.secrets["RIOT_API_KEY"]

st.write("RGAPI 시작 여부:", key.startswith("RGAPI-"))
st.write("길이:", len(key))
