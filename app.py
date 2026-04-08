import streamlit as st
import requests

st.set_page_config(page_title="AI Skaner 4.0 - Pro", page_icon="🛡️")
st.title("🛡️ AI Skaner 4.0: Anty-Błąd Edition")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

def szukaj_value(sport_key, sport_name):
    # POPRAWIONY ADRES URL:
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&apiKey={KLUCZ}"
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            st.info(f"Analizuję {len(dane)} meczów: {sport_name}...")
            
            for mecz in dane:
                bookmakers = mecz.get('bookmakers', [])
                # ZABEZPIECZENIE 1: Minimum 3 bukmacherów dla wiarygodności średniej
                if len(bookmakers) < 3: 
                    continue
                
                wyniki_meczu = []
                
                for i in range(2): 
                    try:
                        kursy = []
                        for b in bookmakers:
                            if b.get('markets') and len(b['markets']) > 0:
                                outcomes = b['markets'][0].get('outcomes', [])
                                if len(outcomes) > i:
                                    kursy.append(outcomes[i]['price'])
                        
                        if not kursy: continue
                        
                        srednia = sum(kursy) / len(kursy)
                        najlepszy = max(kursy)
                        value = (najlepszy / srednia) - 1
                        
                        # Pobieranie nazwy zawodnika z danych meczu
                        nazwa = mecz['home_team'] if i == 0 else mecz['away_team']
                        
                        if 1.20 <= najlepszy <= 5.00 and value > 0.05:
                            wyniki_meczu.append({
                                'nazwa': nazwa,
                                'kurs': najlepszy,
                                'val': value
                            })
                    except: continue
                
                # ZABEZPIECZENIE 2: Tylko jeśli Value jest po JEDNEJ stronie (rozwiązuje Twój problem)
                if len(wyniki_meczu) == 1:
                    res = wyniki_meczu[0]
                    znaleziono += 1
                    st.success(f"💎 OKAZJA: {res['nazwa']}")
                    st.write(f"Mecz: {mecz['home_team']} vs {mecz['away_team']}")
                    st.write(f"Kurs: **{res['kurs']}** | Przewaga: **+{res['val']*100:.1f}%**")
                    st.divider()
            
            if znaleziono == 0: st.warning("Brak wiarygodnych okazji spełniających filtry.")
        else: st.error(f"Błąd API: {odpowiedz.status_code}. Sprawdź klucz lub limity.")
    except Exception as e: st.error(f"Błąd techniczny: {e}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🎾 TENIS (ATP)"): szukaj_value("tennis_atp", "ATP Tour")
with c2:
    if st.button("🏀 KOSZYKÓWKA (NBA)"): szukaj_value("basketball_nba", "NBA")
