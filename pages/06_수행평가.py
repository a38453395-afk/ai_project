import streamlit as st
import requests

API_KEY = st.secrets["RIOT_API_KEY"]

r = requests.get(
    "https://kr.api.riotgames.com/lol/status/v4/platform-data",
    headers={"X-Riot-Token": API_KEY}
)

st.write("상태코드 =", r.status_code)
st.write(r.text)
