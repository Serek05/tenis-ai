import streamlit as st
import requests


API_KEY = "8e65c70e422cd12b3be347f106596f7d" 

st.title("🎾 Moje AI Tenisowe")

if st.button("Pobierz dzisiejsze mecze"):
    try:
        # Dodajemy sport=tennis_atp do adresu, żeby serwer wiedział czego szukamy
        url = f"https://the-odds-api.com{API_KEY}&regions=eu&markets=h2h"

        
        odpowiedz = requests.get(url, timeout=10)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            if len(dane) == 0:
                st.warning("Brak meczów na dzisiaj w bazie danych.")
            else:
                st.success(f"Sukces! Pobrano {len(dane)} meczów.")
                st.write(dane)
        elif odpowiedz.status_code == 401:
            st.error("Błąd: Twój klucz API jest nieprawidłowy. Sprawdź maila!")
        else:
            st.error(f"Serwer zwrócił błąd nr: {odpowiedz.status_code}")
            
    except Exception as e:
        st.error(f"Błąd krytyczny: {e}")
        
        

