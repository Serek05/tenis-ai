import streamlit as st
import requests

st.set_page_config(page_title="Multi-Sport AI", page_icon="🎯")
st.title("🎯 AI: Tenis & Koszykówka")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

def szukaj_value(sport_key, sport_name):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&apiKey={KLUCZ}"
    
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            st.info(f"Skanuję {len(dane)} meczów w dyscyplinie: {sport_name}...")
            
            for mecz in dane:
                if len(mecz['bookmakers']) > 1:
                    # Sprawdzamy kursy dla OBU zawodników/drużyn (index 0 i 1)
                    for i in [0, 1]:
                        try:
                            wszystkie_kursy = [b['markets'][0]['outcomes'][i]['price'] for b in mecz['bookmakers']]
                            nazwa_zawodnika = mecz['bookmakers'][0]['markets'][0]['outcomes'][i]['name']
                            
                            srednia = sum(wszystkie_kursy) / len(wszystkie_kursy)
                            najlepszy = max(wszystkie_kursy)
                            
                            if 1.20 <= najlepszy <= 3.00:
                                value = (najlepszy / srednia) - 1
                                if value > 0.05:
                                    znaleziono += 1
                                    st.success(f"💎 {sport_name.upper()} VALUE: {nazwa_zawodnika}")
                                    st.write(f"Mecz: {mecz['home_team']} vs {mecz['away_team']}")
                                    st.write(f"Kurs: **{najlepszy}** (Średnia: {srednia:.2f}) | Przewaga: **+{value*100:.1f}%**")
                                    st.divider()
                        except:
                            continue
            
            if znaleziono == 0:
                st.warning(f"Obecnie brak wyraźnych okazji w {sport_name}.")
        else:
            st.error(f"Błąd serwera: {odpowiedz.status_code}")
    except Exception as e:
        st.error(f"Błąd: {e}")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎾 SZUKAJ TENIS"):
        szukaj_value("tennis", "Tenis")
with col2:
    if st.button("🏀 SZUKAJ KOSZ"):
        szukaj_value("basketball", "Koszykówka")
