import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Skaner 4.6 - Polish Hunter", page_icon="🇵🇱")
st.title("🇵🇱 AI Skaner 4.6: Łowca na Polskim Rynku")

# Pasek boczny ze strategią BukMichała
st.sidebar.header("🛡️ Strategia 7 Kroków")
st.sidebar.markdown("""
1. **Skanuj AI** (Value > 5%)
2. **Sprawdź Buka** (Kurs >= AI)
3. **Czas meczu** (Sprawdź godzinę!)
4. **Limit 3.0** (Stabilność)
5. **Stawka 2%** (Pamiętaj o podatku 12%!)
6. **Zapisz w Dzienniku**
7. **Zero Emocji**
""")

KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

def szukaj_value(sport_key, sport_name):
    # POPRAWIONY ADRES URL (v4):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&apiKey={KLUCZ}"
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            st.info(f"Skanuję: {sport_name}...")
            
            for mecz in dane:
                bookmakers = mecz.get('bookmakers', [])
                if len(bookmakers) < 3: continue
                
                # KONWERSJA CZASU NA POLSKI
                start_time_utc = datetime.strptime(mecz['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                start_time_pl = start_time_utc + timedelta(hours=2)
                czas_str = start_time_pl.strftime("%d.%m %H:%M")
                
                wyniki_meczu = []
                teams = [mecz['home_team'], mecz['away_team']]
                if 'soccer' in sport_key: teams.append('Draw')

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
                        
                        # FILTR: Kurs do 3.00, Value powyżej 5%
                        if 1.30 <= najlepszy <= 3.00 and value > 0.05:
                            wyniki_meczu.append({'nazwa': t_name, 'kurs': najlepszy, 'val': value})
                    except: continue
                
                if len(wyniki_meczu) == 1:
                    res = wyniki_meczu[0]
                    znaleziono += 1
                    st.success(f"💎 OKAZJA: {res['nazwa']}")
                    st.write(f"🏟️ Liga: **{mecz.get('sport_title')}** | ⏰ Start: **{czas_str}**")
                    st.write(f"📈 Kurs AI: **{res['kurs']}** | Przewaga: **+{res['val']*100:.1f}%**")
                    
                    # LINKI DO POLSKICH BUKMACHERÓW
                    st.write("🔗 **Sprawdź kurs u polskich bukmacherów:**")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1: st.markdown("[STS](https://www.sts.pl)")
                    with col2: st.markdown("[Superbet](https://www.superbet.pl)")
                    with col3: st.markdown("[Fortuna](https://www.efortuna.pl)")
                    with col4: st.markdown("[Totalbet](https://www.totalbet.pl)")
                    st.divider()
            
            if znaleziono == 0: st.warning("Brak okazji spełniających filtry.")
        else: st.error(f"Błąd API: {odpowiedz.status_code}. Sprawdź połączenie.")
    except Exception as e: st.error(f"Błąd techniczny: {e}")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎾 TENIS"): szukaj_value("tennis", "Tenis")
with c2:
    if st.button("🏀 KOSZ"): szukaj_value("basketball", "Koszykówka")
with c3:
    if st.button("⚽ PIŁKA"): szukaj_value("soccer", "Piłka Nożna")
