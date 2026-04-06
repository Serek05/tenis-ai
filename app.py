import streamlit as st
import requests

st.set_page_config(page_title="Tenis AI", page_icon="🎾")
st.title("🎾 Moje Inteligentne AI Tenisowe")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"
# POPRAWIONY ADRES URL (z api. i pełną ścieżką do tenisa)
URL = "https://api.the-odds-api.com/v4/sports/tennis/odds/?regions=eu&markets=h2h&apiKey=" + KLUCZ


if st.button("ANALIZUJ MECZE I OBLICZ SZANSE"):
    try:
        odpowiedz = requests.get(URL, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            st.success(f"Analizuję {len(dane)} meczów...")
            
            for mecz in dane:
                st.subheader(f"🏆 {mecz['home_team']} vs {mecz['away_team']}")
                
                if len(mecz['bookmakers']) > 0:
                    # Dodane [0], aby brać dane od pierwszego bukmachera na liście
                    kursy = mecz['bookmakers'][0]['markets'][0]['outcomes']
                    
                    col1, col2 = st.columns(2)
                    for wynik in kursy:
                        szansa = (1 / wynik['price']) * 100
                        
                        if wynik['name'] == mecz['home_team']:
                            col1.metric(wynik['name'], f"Kurs: {wynik['price']}", f"{szansa:.1f}% szans")
                        else:
                            col2.metric(wynik['name'], f"Kurs: {wynik['price']}", f"{szansa:.1f}% szans")
                st.divider()
        else:
            st.error(f"Błąd serwera: {odpowiedz.status_code}")
    except Exception as e:
        st.error(f"Błąd: {e}")
        
