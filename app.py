import streamlit as st
import requests

API_KEY = "8e65c70e422cd12b3be347f106596f7d" 

st.title("🎾 Moje AI Tenisowe")

if st.button("Pobierz dzisiejsze mecze"):
    try:
        url = "https://the-odds-api.com"
        params = {'apiKey': API_KEY, 'regions': 'eu', 'markets': 'h2h'}
        odpowiedz = requests.get(url, params=params, timeout=10)
        if odpowiedz.status_code == 200:
            st.success(f"Pobrano {len(odpowiedz.json())} meczów!")
            st.write(odpowiedz.json())
        else:
            st.error(f"Błąd klucza! Kod: {odpowiedz.status_code}")
    except Exception as e:
        st.error(f"Problem z połączeniem: {e}")
        

