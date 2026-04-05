import streamlit as st
import requests

# TWÓJ KLUCZ WPISANY NA SZTYWNO
MOJ_KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

st.title("🎾 Moje AI Tenisowe")

if st.button("Pobierz dzisiejsze mecze"):
    try:
        # NAJPROSTSZY MOŻLIWY ADRES BEZ TRUDNYCH ZNAKÓW
        url = "https://the-odds-api.com" + MOJ_KLUCZ + "&regions=eu&markets=h2h"
        
        odpowiedz = requests.get(url, timeout=15)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            st.success("W KOŃCU DZIAŁA! Pobrano mecze.")
            st.write(dane[:2]) # Pokazuje tylko 2 mecze
        else:
            st.error("Serwer odrzucił klucz. Kod: " + str(odpowiedz.status_code))
            
    except Exception as e:
        st.error("Błąd: " + str(e))
