import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Skaner 4.9.2 - Gold Machine", page_icon="🎯")
st.title("🎯 AI Skaner 4.9.2: Złota Maszyna Czasu")

# --- KONFIGURACJA W PASKU BOCZNYM ---
st.sidebar.header("⚙️ Ustawienia Skanera")
KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

# SUWAK: Pozwala przesunąć start skanowania (od 0 do 72 godzin do przodu)
skok_czasu = st.sidebar.slider("Przesuń start skanowania o (godziny):", 0, 72, 0)

# Obliczamy czas dla użytkownika (dla orientacji)
teraz_pl = datetime.now()
start_punkt_pl = teraz_pl + timedelta(hours=skok_czasu)
st.sidebar.info(f"Skanuję mecze zaczynające się OD: {start_punkt_pl.strftime('%d.%m o %H:%M')}")




st.sidebar.markdown("---")
st.sidebar.markdown("""
**🛡️ Strategia 7 Kroków:**
1. Ustaw suwak (np. 24h dla jutra).
2. Kliknij przycisk sportu.
3. Szukaj Value > 5%.
4. Sprawdź u polskiego buka.
5. Kurs musi być >= Kurs AI.
6. Stawka max 2% budżetu.
7. Zapisz typ w dzienniku.
""")

def szukaj_value(sport_key, sport_name):
    teraz_utc = datetime.utcnow()
    
    # 1. Wyliczamy czas startu i końca (TWOJE POPRAWNE LINIE)
    start_skanu = (teraz_utc + timedelta(hours=skok_czasu)).strftime("%Y-%m-%dT%H:%M:%SZ")
    koniec_skanu = (teraz_utc + timedelta(hours=skok_czasu + 24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    
    
    
    # POPRAWIONY URL:
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&commenceTimeFrom={start_skanu}&commenceTimeTo={koniec_skanu}&apiKey={KLUCZ}"
    
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            st.info(f"Analizuję {len(dane)} meczów dla: {sport_name}")
            
            for mecz in dane:
                bookmakers = mecz.get('bookmakers', [])
                if len(bookmakers) < 1: continue
                
                # Konwersja czasu na polski
                start_time_pl = datetime.strptime(mecz['commence_time'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=2)
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
                        
                        if 1.30 <= najlepszy <= 3.00 and value > 0.01:
                            wyniki_meczu.append({'nazwa': t_name, 'kurs': najlepszy, 'val': value})
                    except: continue
                
                if len(wyniki_meczu) == 1:
                    res = wyniki_meczu[0]
            
                    znaleziono += 1
                    st.success(f"💎 OKAZJA: {res['nazwa']}")
                    st.write(f"🏟️ {mecz.get('sport_title')} | ⏰ {czas_str}")
                    st.write(f"⚔️ {mecz['home_team']} vs {mecz['away_team']}")
                    st.write(f"📈 Kurs AI: **{res['kurs']}** | Przewaga: **+{res['val']*100:.1f}%**")
                    
                    st.write("🔗 **Porównaj u polskich buków:**")
                    
                    link1, link2, link3 = st.columns(3)
                    with link1: st.markdown("[Superbet](https://www.superbet.pl)")
                    with link2: st.markdown("[STS](https://www.sts.pl)")
                    with link3: st.markdown("[Fortuna](https://www.efortuna.pl)")
                    
                
                    st.divider()
            
            if znaleziono == 0: 
                st.warning("Brak okazji. Przesuń suwak dalej na pasku bocznym (np. na 24h dla jutra).")
        else: 
            st.error(f"Błąd API: {odpowiedz.status_code}. Sprawdź limity na koncie.")
    except Exception as e: 
        st.error(f"Błąd techniczny: {e}")

# --- PRZYCISKI GŁÓWNE ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎾 TENIS"): szukaj_value("tennis", "Tenis")
with col2:
    if st.button("🏀 KOSZ"): szukaj_value("basketball", "Koszykówka")
with col3:
    if st.button("⚽ PIŁKA"): szukaj_value("soccer", "Piłka Nożna")
