import streamlit as st
import requests

st.set_page_config(page_title="AI Skaner 4.4 - Niche Hunter", page_icon="🕵️")
st.title("🕵️ AI Skaner 4.4: Łowca Nisz")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

def szukaj_value(sport_key, sport_name):
    # TO JEST JEDYNY POPRAWNY ADRES URL:
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&apiKey={KLUCZ}"
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            st.info(f"Skanuję nisze: {sport_name}...")
            
            for mecz in dane:
                bookmakers = mecz.get('bookmakers', [])
                if len(bookmakers) < 3: continue
                
                wyniki_meczu = []
                teams = [mecz['home_team'], mecz['away_team']]
                if 'soccer' in sport_key:
                    teams.append('Draw')

                for t_name in teams: 
                    try:
                        kursy = []
                        for b in bookmakers:
                            for m in b.get('markets', []):
                                for o in m.get('outcomes', []):
                                    if o['name'] == t_name:
                                        kursy.append(o['price'])
                        
                        if not kursy: continue
                        srednia = sum(kursy) / len(kursy)
                        najlepszy = max(kursy)
                        value = (najlepszy / srednia) - 1
                        
                        # PARAMETRY NISZY: Kurs do 3.50 i Value > 7%
                        if 1.30 <= najlepszy <= 3.50 and value > 0.07:
                            wyniki_meczu.append({'nazwa': t_name, 'kurs': najlepszy, 'val': value})
                    except: continue
                
                if len(wyniki_meczu) == 1:
                    res = wyniki_meczu[0]
                    znaleziono += 1
                    st.success(f"💎 NISZA: {res['nazwa']}")
                    st.write(f"Liga: **{mecz.get('sport_title')}**")
                    st.write(f"Mecz: {mecz['home_team']} vs {mecz['away_team']}")
                    st.write(f"Kurs: **{res['kurs']}** | Przewaga: **+{res['val']*100:.1f}%**")
                    st.divider()
            
            if znaleziono == 0: st.warning("Brak dużych pomyłek w niszach.")
        else: st.error(f"Błąd API: {odpowiedz.status_code}. Sprawdź połączenie.")
    except Exception as e: st.error(f"Błąd techniczny: {e}")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎾 TENIS (Nisze)"): szukaj_value("tennis", "Wszystkie Turnieje")
with c2:
    if st.button("🏀 KOSZ (NCAA)"): szukaj_value("basketball_ncaab", "College Basketball")
with c3:
    if st.button("⚽ PIŁKA (Inne)"): szukaj_value("soccer", "Ligi Światowe")
        
