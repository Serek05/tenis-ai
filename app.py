import streamlit as st
import requests

st.title("🎾 Moje AI Tenisowe")

# TWOJE DANE KONFIGURACYJNE
KLUCZ = "8e65c70e422cd12b3be347f106596f7d"
ADRES = "https://the-odds-api.com"

if st.button("POBIERZ MECZE"):
    try:
        # Budujemy zapytanie krok po kroku, żeby telefon nic nie zepsuł
        parametry = {
            "apiKey": KLUCZ,
            "regions": "eu",
            "markets": "h2h"
        }
        odpowiedz = requests.get(ADRES, params=parametry)
        
        if odpowiedz.status_code == 200:
            mecze = odpowiedz.json()
            st.success(f"UDAŁO SIĘ! Znaleziono {len(mecze)} meczów.")
            st.write(mecze[:3]) # Pokaż 3 pierwsze mecze
        else:
            st.error(f"Błąd serwera: {odpowiedz.status_code}")
            
    except Exception as e:
        st.error(f"Błąd połączenia: {e}")
        
