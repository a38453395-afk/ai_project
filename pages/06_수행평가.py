import streamlit as st

API_KEY = st.secrets.get("RIOT_API_KEY")

if API_KEY:
    st.success("✅ API 키 연결 성공!")
else:
    st.error("❌ API 키를 찾을 수 없음")
