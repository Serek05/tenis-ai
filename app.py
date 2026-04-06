import streamlit as st
import requests

st.set_page_config(page_title="Tenis AI - Value Pro", page_icon="📈")
st.title("📈 Precyzyjny Łowca Valuebetów")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"
URL = "https://api.the-odds-api.com/v4/sports/tennis/odds/?regions=eu&markets=h2h&apiKey=" + KLUCZ



if st.button("SZUKAJ OKAZJI (1.20 - 3.00)"):
    try:
        odpowiedz = requests.get(URL, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            st.info(f"Analizuję {len(dane)} meczów pod kątem Twojego zakresu kursów...")
            
            znaleziono = 0
            for mecz in dane:
                if len(mecz['bookmakers']) > 1:
                    kursy_p1 = [b['markets'][0]['outcomes'][0]['price'] for b in mecz['bookmakers']]
                    
                    srednia = sum(kursy_p1) / len(kursy_p1)
                    najlepszy = max(kursy_p1)
                    
                    # FILTR: Kurs musi być między 1.20 a 3.00
                    if 1.20 <= najlepszy <= 3.00:
                        value = (najlepszy / srednia) - 1
                        
                        # Próg 5% przewagi nad bukmacherem
                        if value > 0.05:
                            znaleziono += 1
                            st.success(f"💎 OKAZJA: {mecz['home_team']}")
                            st.write(f"Mecz: {mecz['home_team']} vs {mecz['away_team']}")
                            st.write(f"Najlepszy kurs: **{najlepszy}** (Średnia: {srednia:.2f})")
                            st.write(f"Przewaga nad rynkiem: **+{value*100:.1f}%**")
                            st.divider()
            
            if znaleziono == 0:
                st.warning("Obecnie brak Valuebetów w wybranym zakresie kursów.")
        else:
            st.error("Błąd serwera danych.")
    except Exception as e:
        st.error(f"Błąd: {e}")
