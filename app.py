import streamlit as st
import requests

# TUTAJ WKLEJ SWÓJ KLUCZ Z MAILA ZAMIAST ZER
API_KEY = "8e65c70e422cd12b3be347f106596f7d" 

st.title("🎾 Moje AI Tenisowe")
st.write("Witaj! Kliknij przycisk poniżej, aby pobrać aktualne kursy.")

if st.button("Pobierz dzisiejsze mecze"):
    # Łączymy się z bazą kursów
    url = f"https://the-odds-api.com{API_KEY}&regions=eu&markets=h2h"
    odpowiedz = requests.get(url)
    
    if odpowiedz.status_code == 200:
        dane = odpowiedz.json()
        st.success("Dane pobrane pomyślnie!")
        st.write(dane) # Tu zobaczysz listę meczów i kursy
    else:
        st.error("Błąd! Sprawdź czy Twój klucz API jest poprawny.")
