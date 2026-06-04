import streamlit as st
import requests

API_KEY = st.secrets["RIOT_API_KEY"]

headers = {
    "X-Riot-Token": API_KEY
}

st.title("Riot API 테스트")

game_name = st.text_input("게임명")
tag_line = st.text_input("태그")

if st.button("조회"):

    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

    r = requests.get(url, headers=headers)

    st.write("상태코드:", r.status_code)
    st.json(r.json())
