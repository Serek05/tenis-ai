import streamlit as st
import requests

st.title("🎾 Moje AI Tenisowe")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

if st.button("ANALIZUJ DZISIEJSZE MECZE"):
    try:
        # PAMIĘTAJ O TYCH SPACJACH NA POCZĄTKU LINII:
        url = "https://api.the-odds-api.com/v4/sports/tennis/odds/?regions=eu&markets=h2h&apiKey=" + KLUCZ
        odpowiedz = requests.get(url, timeout=15)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            st.success(f"Sukces! Znaleziono {len(dane)} meczów.")
            st.write(dane[:2])
        else:
            st.error(f"Błąd serwera: {odpowiedz.status_code}")
            
    except Exception as e:
        st.error(f"Błąd: {e}")
