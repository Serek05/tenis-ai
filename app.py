import streamlit as st
import requests

st.title("🎾 Moje AI Tenisowe")

# TWOJE DANE (WPISANE NA SZTYWNO)
KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

if st.button("POBIERZ MECZE"):
    try:
        # TO JEST JEDEN GOTOWY LINK - NAJPROSTSZA WERSJA
        
url = "https://api.the-odds-api.com/v4/sports/tennis_atp/odds/?regions=eu&markets=h2h&apiKey=" + KLUCZ

    
        
        odpowiedz = requests.get(url, timeout=15)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            if len(dane) == 0:
                st.warning("Brak meczów na dzisiaj w bazie danych.")
            else:
                st.success("W KOŃCU DZIAŁA! Pobrano dane.")
                st.write(dane[:2]) # Pokaż 2 mecze
        else:
            st.error("Serwer odrzucił klucz. Kod błędu: " + str(odpowiedz.status_code))
            
    except Exception as e:
        st.error("Błąd połączenia: " + str(e))
        
