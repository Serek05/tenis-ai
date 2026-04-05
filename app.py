import streamlit as st
import requests

# TWÓJ KLUCZ (Wpisany poprawnie)
API_KEY = "8e65c70e422cd12b3be347f106596f7d" 

st.title("🎾 Moje AI Tenisowe")

if st.button("Pobierz dzisiejsze mecze"):
    try:
        # PONIŻEJ JEST POPRAWNY ADRES (Zwróć uwagę na ukośniki i ?apiKey=)
        url = f"https://the-odds-api.com{API_KEY}&regions=eu&markets=h2h"
        
        odpowiedz = requests.get(url, timeout=15)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            if len(dane) == 0:
                st.warning("Brak meczów na dzisiaj w bazie danych.")
            else:
                st.success(f"Sukces! Pobrano {len(dane)} meczów.")
                st.write(dane[:3]) # Pokazuje pierwsze 3 mecze
        else:
            st.error(f"Błąd serwera: {odpowiedz.status_code}. Sprawdź klucz API.")
            
    except Exception as e:
        st.error(f"Błąd połączenia: {e}")
        


        
        

