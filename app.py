import streamlit as st
import requests

st.set_page_config(page_title="AI Skaner 4.2 - Global", page_icon="🌍")
st.title("🌍 AI Skaner 4.2: Global Hunter")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

def szukaj_value(sport_key, sport_name):
    # TO JEST JEDYNY POPRAWNY URL:
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&apiKey={KLUCZ}"
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            st.info(f"Analizuję {len(dane)} meczów: {sport_name}...")
            
            for mecz in dane:
                bookmakers = mecz.get('bookmakers', [])
                if len(bookmakers) < 3: # Min. 3 bukmacherów dla wiarygodności
                    continue
                
                wyniki_meczu = []
                teams = [mecz['home_team'], mecz['away_team']]
                
                for team_name in teams:
                    try:
                        kursy = []
                        for b in bookmakers:
                            if b.get('markets') and len(b['markets']) > 0:
                                outcomes = b['markets'][0].get('outcomes', [])
                                for o in outcomes:
                                    if o['name'] == team_name:
                                        kursy.append(o['price'])
                        
                        if not kursy: continue
                        
                        srednia = sum(kursy) / len(kursy)
                        najlepszy = max(kursy)
                        value = (najlepszy / srednia) - 1
                        
                        # FILTR: Kurs do 3.00, Value powyżej 5%
                        if 1.20 <= najlepszy <= 3.00 and value > 0.05:
                            wyniki_meczu.append({
                                'nazwa': team_name,
                                'kurs': najlepszy,
                                'val': value
                            })
                    except: continue
                
                # ZABEZPIECZENIE: Tylko jeśli Value jest po JEDNEJ stronie
                if len(wyniki_meczu) == 1:
                    res = wyniki_meczu[0]
                    znaleziono += 1
                    st.success(f"💎 OKAZJA: {res['nazwa']}")
                    st.write(f"Mecz: {mecz['home_team']} vs {mecz['away_team']} ({mecz.get('sport_title', 'Inny')})")
                    st.write(f"Kurs: **{res['kurs']}** | Przewaga: **+{res['val']*100:.1f}%**")
                    st.divider()
            
            if znaleziono == 0: st.warning("Brak wiarygodnych okazji w tej chwili.")
        else: st.error(f"Błąd API: {odpowiedz.status_code}. Sprawdź połączenie.")
    except Exception as e: st.error(f"Błąd techniczny: {e}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🎾 TENIS (Global)"): 
        szukaj_value("tennis", "Wszystkie Turnieje")
with c2:
    if st.button("🏀 KOSZ (Global)"): 
        szukaj_value("basketball", "Wszystkie Ligi")
 
