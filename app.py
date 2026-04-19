import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Skaner 5.6 - Ultra Refresh", page_icon="🎯")
st.title("🎯 AI Skaner 5.6: Maszyna Czasu")

# --- 1. KONFIGURACJA ---
st.sidebar.header("⚙️ Ustawienia Skanera")
KLUCZ = "8e65c70e422cd12b3be347f106596f7d"

# SUWAK: Musi być przed funkcją
skok_czasu = st.sidebar.slider("Przesuń start skanowania o (godziny):", 0, 72, 0)

# Napis pomocniczy
teraz_pl = datetime.now()
start_punkt_pl = teraz_pl + timedelta(hours=skok_czasu)
st.sidebar.info(f"Skanuję mecze OD: {start_punkt_pl.strftime('%d.%m o %H:%M')}")

# --- 2. FUNKCJA SKANUJĄCA ---
# ttl=1 wymusza odświeżanie danych co sekundę, żeby nie pokazywać starych wyników
@st.cache_data(ttl=1)
def szukaj_value(sport_key, sport_name, przesuniecie):
    # Brutalne czyszczenie starej pamięci
    st.cache_data.clear()
    
    teraz_utc = datetime.utcnow()
    # Obliczamy czas na podstawie przesunięcia z suwaka
    start_skanu = (teraz_utc + timedelta(hours=przesuniecie)).strftime("%Y-%m-%dT%H:%M:%SZ")
    koniec_skanu = (teraz_utc + timedelta(hours=przesuniecie + 4)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # URL z v4, TimeFrom oraz znacznikiem odświeżania timestamp
    ts = teraz_utc.strftime("%H%M%S")
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?regions=eu&markets=h2h&commenceTimeFrom={start_skanu}&commenceTimeTo={koniec_skanu}&apiKey={KLUCZ}&v={ts}&s={przesuniecie}"
    
    try:
        odpowiedz = requests.get(url, timeout=15)
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            znaleziono = 0
            
            st.info(f"Szukam okazji od godziny: {start_skanu} (UTC)")
            
            for mecz in dane:
                bookmakers = mecz.get('bookmakers', [])
                if len(bookmakers) < 3: continue 
                
                start_time_pl = datetime.strptime(mecz['commence_time'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=2)
                czas_str = start_time_pl.strftime("%d.%m o %H:%M")
                
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
                        
                        # FILTR VALUE 5%
                        if 1.30 <= najlepszy <= 3.00 and value > 0.05:
                            wyniki_meczu.append({'nazwa': t_name, 'kurs': najlepszy, 'val': value})
                    except: continue
                
                if len(wyniki_meczu) == 1:
                    res = wyniki_meczu[0]
                    znaleziono += 1
                    st.success(f"💎 OKAZJA: {res['nazwa']}")
                    st.write(f"🏟️ {mecz.get('sport_title')} | ⏰ {czas_str}")
                    st.write(f"⚔️ {mecz['home_team']} vs {mecz['away_team']}")
                    st.write(f"📈 Kurs AI: **{res['kurs']}** | Przewaga: **+{res['val']*100:.1f}%**")
                    
                    l1, l2, l3 = st.columns(3)
                    with l1: st.markdown("[Superbet](https://superbet.pl)")
                    with l2: st.markdown("[STS](https://sts.pl)")
                    with l3: st.markdown("[Fortuna](https://efortuna.pl)")
                    st.divider()
            
            if znaleziono == 0: 
                st.warning("Brak okazji spełniających filtry (Value > 5%, Bukmacherzy min. 3).")
        else: 
            st.error(f"Błąd API: {odpowiedz.status_code}")
    except Exception as e: 
        st.error(f"Błąd: {e}")

# --- 3. PRZYCISKI ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎾 TENIS"): szukaj_value("tennis", "Tenis", skok_czasu)
with c2:
    if st.button("🏀 KOSZ"): szukaj_value("basketball", "Koszykówka", skok_czasu)
with c3:
    if st.button("⚽ PIŁKA"): szukaj_value("soccer", "Piłka Nożna", skok_czasu)
