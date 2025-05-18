import os
import json
from dotenv import load_dotenv
import openai
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z zmiennej środowiskowej
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Nie ustawiono klucza API OpenAI. Ustaw OPENAI_API_KEY w pliku .env")

# Konfiguracja strony
st.set_page_config(page_title="🧠Doradca Finansowy AI", layout="wide")

# Stylowanie tabeli: niełamliwe nagłówki i lewostronne wyrównanie
st.markdown(
    """
    <style>
    th { white-space: nowrap; }
    th, td { text-align: left !important; }
    h3 a[href^="#"] {
        display: none !important;
    }
    h1 {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Rozkład kolumn: wąska lewa na opis, odstęp, prawa szeroka na funkcjonalność
col_desc, col_spacer, col_main = st.columns([1.2, 0.3, 4])

# Lewa kolumna: opis aplikacji i disclaimer
with col_desc:
    st.markdown(
        """
Aplikacja Doradca Finansowy AI łączy prosty, responsywny interfejs użytkownika zbudowany w oparciu o Streamlit z potężnym backendem AI opartym o OpenAI GPT-3.5-turbo. Dzięki zastosowaniu wzorców prompt engineering i bibliotek do przetwarzania danych (Pandas, Matplotlib) użytkownik otrzymuje dynamiczną, interaktywną rekomendację portfela inwestycyjnego wraz z wizualizacją i krótkim uzasadnieniem. Aplikacja używa specjalnie na tę potrzebę stworzonego klucza API OpenAI, który nie jest przechowywany w repozytorium kodu.

---

Przedstawione narzędzenie oraz jego rekomendacje nie są poradą inwestycyjną w rozumieniu Rozporządzenia Ministra Finansów z dnia 19.10.2005 r. w sprawie informacji stanowiących rekomendacje dotyczące instrumentów finansowych lub ich emitentów (Dz. U. z 2005 r. Nr 206, poz. 1715). Treść rekomendacji ma jedynie charakter edukacyjny, a sama aplikacja została stworzona na potrzeby naukowe.

Kamil Lemański 2025 ©️
        """,
        unsafe_allow_html=True
    )

# Prawa kolumna: główna część aplikacji
with col_main:
    st.title("🧠Doradca Finansowy AI")
    st.markdown("Wprowadź poniższe dane w celu wygenerowania rekomendacji dla twojego portfela inwestycyjnego.")

    # Formularz danych użytkownika
    with st.form("user_input"):
        # 1) Wiek jako text_input zamiast number_input, bez domyślnej wartości
        age_str = st.text_input(
            "Wiek",
            value="",
            placeholder="Wpisz swój wiek"
        )

        # 2) Cel inwestycji z pustą opcją na start
        goal = st.selectbox(
            "Cel inwestycji",
            [
                "Wybierz cel inwestycji",
                "Emerytura",
                "Ochrona przed inflacją",
                "Budowa kapitału",
                "Finansowanie edukacji",
                "Zakup mieszkania/domu",
                "Spekulacja i krótkoterminowy zysk",
            ],
        )

        # Kwota oszczędności
        amount_str = st.text_input(
            "Kwota oszczędności (PLN)",
            "",
            placeholder="np. 10000"
        )

        # 3) Poziom ryzyka z pustą opcją na start
        risk = st.selectbox(
            "Poziom ryzyka",
            [
                "Wybierz poziom ryzyka",
                "niskie",
                "średnie",
                "wysokie",
            ],
        )

        submitted = st.form_submit_button("Generuj portfolio")

    if submitted:
        # --- walidacja wieku ---
        if not age_str:
            st.error("Podaj swój wiek.")
            st.stop()
        try:
            age = int(age_str)
            if age < 18:
                raise ValueError
        except ValueError:
            st.error("Jesteś osobą niepełnoletnią.")
            st.stop()

        # --- walidacja celu inwestycji ---
        if goal.startswith("Wybierz cel inwestycji"):
            st.error("Wybierz cel inwestycji")
            st.stop()

        # --- walidacja kwoty ---
        if not amount_str:
            st.error("Podaj kwotę oszczędności w PLN.")
            st.stop()
        try:
            amount = float(amount_str.replace(",", "."))
            if amount <= 0:
                raise ValueError
        except ValueError:
            st.error("Kwota musi być liczbą większą od 0 (np. 10000).")
            st.stop()

        # --- walidacja poziomu ryzyka ---
        if risk.startswith("Wybierz poziom ryzyka"):
            st.error("Wybierz poziom ryzyka")
            st.stop()

        # Lista aktywów w zależności od ryzyka
        assets = []
        if risk in ["średnie", "wysokie"]:
            assets.append("BTC")
        if risk == "wysokie":
            assets.append("ETH")
        # Dodane obligacje i fundusze obligacji
        assets.extend([
            "Złoto",
            "Srebro",
            "Akcje",
            "ETF-y",
            "Obligacje skarbowe",
            "Lokaty bankowe",
            "Obligacje korporacyjne",
            "Fundusze obligacji"
        ])

        # Generowanie propozycji portfela
        prompt_portfolio = (
            f"Jesteś profesjonalnym ekspertem i doradcą finansowym. "
            f"Użytkownik: wiek {age}, cel {goal}, kwota {amount} PLN, ryzyko {risk}. "
            f"Zaproponuj maksymalnie 8 aktywów z procentami (wielokrotności 5%) dla: {', '.join(assets)}. "
            f"MUSISZ zaproponować m.in 2 aktywa do stworzenia portfolio. Nie uciekaj od odpowiedzi."
            "Odpowiedz wyłącznie JSON-em w strukturze: "
            "{ BTC, ETH, Złoto, Srebro, Akcje: {percent, examples}, ETF-y: {percent, examples}, "
            "Obligacje skarbowe: {percent, examples}, Obligacje korporacyjne: {percent, examples}, Fundusze obligacji: {percent, examples} }."
        )
        with st.spinner("Generuję rekomendacje..."):
            resp_pf = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jesteś doradcą finansowym AI, odpowiadaj tylko JSON-em."},
                    {"role": "user", "content": prompt_portfolio}
                ],
                temperature=0.7
            )
        try:
            data = json.loads(resp_pf.choices[0].message.content)
        except json.JSONDecodeError:
            st.error("Nie udało się sparsować JSON z API.")
            st.stop()

        # Zaokrąglenie i ograniczenie grup procentowych
        for k, v in list(data.items()):
            if isinstance(v, dict):
                raw = v.get("percent", 0)
                try:
                    pct = float(raw)
                except (ValueError, TypeError):
                    pct = 0
                rounded_pct = round(pct / 5) * 5
                data[k]["percent"] = rounded_pct
            else:
                try:
                    pct = float(v)
                except (ValueError, TypeError):
                    pct = 0
                rounded_pct = round(pct / 5) * 5
                data[k] = rounded_pct

        # Sortowanie grup i ograniczenie do 8
        groups = sorted(
            data.items(),
            key=lambda x: x[1]["percent"] if isinstance(x[1], dict) else x[1],
            reverse=True
        )[:8]

        # Budowa wierszy tabeli
        rows = []
        for asset, entry in groups:
            if isinstance(entry, dict):
                pct = entry.get("percent", 0)
                examples = entry.get("examples", [])
                if pct > 0 and examples:
                    share = round(pct / len(examples) / 5) * 5
                    for name in examples:
                        rows.append({"Aktywo": name, "Procent": share, "Kwota (PLN)": share/100*amount})
            else:
                if entry > 0:
                    rows.append({"Aktywo": asset, "Procent": entry, "Kwota (PLN)": entry/100*amount})

        # Filtracja zerowych i ograniczenie do 8
        rows = [r for r in rows if r["Procent"] > 0][:8]

        # Korekta sumy do 100%
        total_pct = sum(r["Procent"] for r in rows)
        diff = 100 - total_pct
        if rows and diff:
            rows[-1]["Procent"] += diff
            rows[-1]["Kwota (PLN)"] = rows[-1]["Procent"]/100*amount

        # Formatowanie wartości
        for r in rows:
            r["Kwota (PLN)"] = f"{r['Kwota (PLN)']:.2f}"
            r["Procent"] = f"{r['Procent']}%"

        col1, col2 = st.columns([1.2, 1.2])
        with col1:
            st.markdown(
                """
                <div style='font-size:1.25em; font-weight:bold; margin-bottom:0; padding-bottom:0;'>💸Rekomendowane portfolio:</div>
                """,
                unsafe_allow_html=True
            )
            filtered_rows = [r for r in rows if int(r['Procent'].rstrip('%')) > 0]
            sorted_rows = sorted(filtered_rows, key=lambda r: int(r['Procent'].rstrip('%')), reverse=True)
            df = pd.DataFrame(sorted_rows)
            st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)
            st.markdown(
                """
                <div style='font-size:1.25em; font-weight:bold; margin-bottom:0; padding-bottom:0;'>📊Wykres kołowy portfela:</div>
                """,
                unsafe_allow_html=True
            )
            fig, ax = plt.subplots()
            ax.pie([int(r['Procent'][:-1]) for r in sorted_rows], labels=[r['Aktywo'] for r in sorted_rows], autopct='%1.0f%%')
            st.pyplot(fig)
        with col2:
            tickers = ", ".join([r['Aktywo'] for r in rows])
            prompt_explain = (
                f"Dlaczego wybrałeś następujące aktywa: {tickers} "
                f"dla użytkownika w wieku {age}, cel {goal}, kwota {amount} PLN, ryzyko {risk}? "
                "Uzasadnij swoją rekomendację w max 200-260 słowach."
            )
            resp_ex = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":"system","content":"Jesteś doradcą finansowym AI."},
                    {"role":"user","content":prompt_explain}
                ],
                temperature=0.7
            )
            explanation = resp_ex.choices[0].message.content.strip()
            st.markdown(
                f"""
                <div style='margin-bottom:0; padding-bottom:0;'>
                  <div style='font-size:1.25em; font-weight:bold; margin-bottom:0; padding-bottom:0;'>📝Argumentacja:</div>
                  <div style='margin-top:0; padding-top:0;'>{explanation}</div>
                </div>
                """,
                unsafe_allow_html=True
            )