import streamlit as st

key = st.secrets["RIOT_API_KEY"]

st.write("길이:", len(key))
st.write("앞 6글자:", key[:6])
