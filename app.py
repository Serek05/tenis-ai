import streamlit as st
import requests

# TWÓJ KLUCZ (Zapisany na sztywno, żeby nie było błędów)
API_KEY = "8e65c70e422cd12b3be347f106596f7d" 

st.title("🎾 Moje AI Tenisowe")

if st.button("Pobierz dzisiejsze mecze"):
    try:
        # TO JEST KLUCZOWA LINIA - MUSI BYĆ IDENTYCZNA:
        url = f"https://the-odds-api.com{API_KEY}&regions=eu&markets=h2h"
        
        odpowiedz = requests.get(url, timeout=15)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            if len(dane) == 0:
                st.warning("Brak meczów na dzisiaj w bazie danych.")
            else:
                st.success(f"Sukces! Pobrano {len(dane)} meczów.")
                # Pokazujemy tylko pierwsze 3 mecze, żeby było czytelnie
                st.write(dane[:3]) 
        else:
            st.error(f"Serwer zwrócił błąd: {odpowiedz.status_code}. Sprawdź klucz API.")
            
    except Exception as e:
        st.error(f"Błąd połączenia: {e}")


        
        

