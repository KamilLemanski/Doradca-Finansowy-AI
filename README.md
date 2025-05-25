🧠Doradca Finansowy AI

Live App ➤ https://doradca-finansowy-ai-kamil-lemanski.streamlit.app

Doradca Finansowy AI to aplikacja, która łączy prosty, responsywny interfejs użytkownika zbudowany w oparciu o Streamlit z potężnym backendem AI opartym o OpenAI GPT-3.5-turbo. Dzięki zastosowaniu wzorców prompt engineering i bibliotek do przetwarzania danych (Pandas, Matplotlib) użytkownik otrzymuje dynamiczną, interaktywną rekomendację portfela inwestycyjnego wraz z wizualizacją i krótkim uzasadnieniem. Aplikacja używa specjalnie na tę potrzebę stworzonego klucza API OpenAI, który nie jest przechowywany w repozytorium kodu.

------------
✨ Właściwości:

✅ Generowanie portfolio inwestycyjnego dla użytkownika

🎯 Dostosowanie do wieku, celu inwestycji, kwoty oszczędności oraz poziomu ryzyka

🎨 Tworzenie wykresu portfela oraz jego argumentacji

🔐 Bezpieczne użycie klucza API

-------------
🧪 Zastosowane technologie:

Python 3.7+

Streamlit

OpenAI GPT-3.5-turbo

Pandas

Matplotlib

------------
👉 Uruchomienie aplikacji online:

https://doradca-finansowy-ai-kamil-lemanski.streamlit.app

------------
📂 Folder structure:

ai-financial-advisor/

├── app.py              # Główna logika aplikacji

├── requirements.txt     # Biblioteki Pythona

├── .gitignore          # Ochrona danych poufnych (API)

└── README.md            # Ten plik


------------
⚙️ Instalacja i uruchomienie aplikacji lokalnie:

1. Sklonuj repozytorium: https://github.com/KamilLemanski/ai-financial-advisor.git

2. Zainstaluj wymagane biblioteki: pip install -r requirements.txt

3. Skonfiguruj swój klucz OpenAI: cp .env.example .env

4. Uruchom aplikację: python app.py

------------
🔐 Zmienne środowiskowe:

Ustaw zmienną środowiskową OPENAI_API_KEY w pliku .env:

OPENAI_API_KEY=sk-...twój-klucz...

------------
☁️ Deployment na platformie streamlit.io:

1. Połącz repozytorium GitHub z streamlit.io
   
2. Upewnij się, że w repo są pliki: app.py, requirements.txt
   
3. Na platformie Streamlit dodaj swój wygenerowany klucz API
   
3. Aplikacja zostanie automatycznie uruchomiona pod adresem .streamlit.app

------------
📌 Przykład użycia:

1. Wprowadź wiek, cel inwestycji, kwotę oszczędności oraz poziom ryzyka

2. Kliknij „Generuj portfolio”

3. Otrzymujesz rekomendowane portfolio, jego wykres kołowy oraz wyjaśnienie wyboru aplikacji


------------
📝 Licencja:

Przedstawione narzędzenie oraz jego rekomendacje nie są poradą inwestycyjną w rozumieniu Rozporządzenia Ministra Finansów z dnia 19.10.2005 r. w sprawie informacji stanowiących rekomendacje dotyczące instrumentów finansowych lub ich emitentów (Dz. U. z 2005 r. Nr 206, poz. 1715). Treść rekomendacji ma jedynie charakter edukacyjny, a sama aplikacja została stworzona na potrzeby naukowe.

Kamil Lemański 2025 ©️

------------
🙏 Credits:

OpenAI (GPT-3.5-turbo), Streamlit.

