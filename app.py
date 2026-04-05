import streamlit as st
import requests

# TWÓJ KLUCZ (Zostawiony dokładnie tak, jak przyszedł w mailu)
API_KEY = "8e65c70e422cd12b3be347f106596f7d" 

st.title("🎾 Moje AI Tenisowe")

if st.button("Pobierz dzisiejsze mecze"):
    try:
        # PONIŻEJ JEST PEŁNY, POPRAWNY ADRES (ZWRÓĆ UWAGĘ NA api. ORAZ /v4/)
        url = f"https://the-odds-api.com{API_KEY}&regions=eu&markets=h2h"
        
        odpowiedz = requests.get(url, timeout=15)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            if len(dane) == 0:
                st.warning("Brak meczów na dzisiaj w bazie danych.")
            else:
                st.success(f"Sukces! Pobrano {len(dane)} meczów.")
                # Pokazujemy 3 pierwsze mecze, żeby sprawdzić czy działa
                st.write(dane[:3]) 
        elif odpowiedz.status_code == 401:
            st.error("Błąd 401: Twój klucz API jest nieaktywny lub błędny.")
        else:
            st.error(f"Serwer zwrócił błąd nr: {odpowiedz.status_code}")
            
    except Exception as e:
        st.error(f"Błąd połączenia: {e}")
        
        


        
        

