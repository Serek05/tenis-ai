import streamlit as st
import requests

st.set_page_config(page_title="Tenis AI - Value Hunter", page_icon="🎯")
st.title("🎯 Łowca Valuebetów Tenisowych")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"
URL = "https://api.the-odds-api.com/v4/sports/tennis/odds/?regions=eu&markets=h2h&apiKey=" + KLUCZ


if st.button("SZUKAJ VALUEBETÓW"):
    try:
        odpowiedz = requests.get(URL, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            st.info(f"Skanuję {len(dane)} meczów w poszukiwaniu błędów bukmacherów...")
            
            for mecz in dane:
                if len(mecz['bookmakers']) > 1: # Potrzebujemy min. 2 bukmacherów do porównania
                    # Pobieramy kursy od wszystkich dostępnych buków
                    wszystkie_kursy_p1 = [b['markets'][0]['outcomes'][0]['price'] for b in mecz['bookmakers']]
                    wszystkie_kursy_p2 = [b['markets'][0]['outcomes'][1]['price'] for b in mecz['bookmakers']]
                    
                    sredni_kurs_p1 = sum(wszystkie_kursy_p1) / len(wszystkie_kursy_p1)
                    najlepszy_kurs_p1 = max(wszystkie_kursy_p1)
                    
                    # OBLICZANIE VALUE (Wartości)
                    # Jeśli najlepszy kurs jest o 5% wyższy niż średnia rynkowa -> mamy VALUE!
                    value_p1 = (najlepszy_kurs_p1 / sredni_kurs_p1) - 1
                    
                    if value_p1 > 0.05: # Próg 5% wartości
                        st.success(f"💎 VALUEBET WYKRYTY: {mecz['home_team']}")
                        st.write(f"Mecz: {mecz['home_team']} vs {mecz['away_team']}")
                        st.write(f"Kurs u tego buka: **{najlepszy_kurs_p1}** (Średnia rynkowa: {sredni_kurs_p1:.2f})")
                        st.write(f"Zysk matematyczny: **+{value_p1*100:.1f}%**")
                        st.divider()
        else:
            st.error("Błąd bazy danych.")
    except Exception as e:
        st.error(f"Błąd: {e}")
