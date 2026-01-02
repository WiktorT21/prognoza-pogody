import requests
import sys


def test_api_key():
    """Testuje czy API key OpenWeatherMap działa"""

    # TWÓJ API KEY - ten sam co w config.py
    API_KEY = "87fa0c47733c2e7eb40a68254ebbf1af"

    # Współrzędne Kasprowy Wierch
    lat, lon = 49.2511, 19.9350

    print("🧪 TEST API KEY OPENWEATHERMAP")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-10:]}")
    print(f"Współrzędne: lat={lat}, lon={lon}")
    print("=" * 60)

    # URL dla aktualnej pogody
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pl"

    print(f"\n🔗 URL (skrócony): {url[:100]}...")

    try:
        print("\n⏳ Wysyłam zapytanie do API...")
        response = requests.get(url, timeout=10)

        print(f"📡 Status odpowiedzi: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n✅ ✅ ✅ API KEY DZIAŁA POPRAWNIE! ✅ ✅ ✅")
            print("-" * 50)
            print(f"🌍 Lokalizacja: {data.get('name', 'brak nazwy')}")
            print(f"🌡️  Temperatura: {data['main']['temp']}°C")
            print(f"💨 Wiatr: {data['wind']['speed']} m/s")
            print(f"💧 Wilgotność: {data['main']['humidity']}%")
            print(f"⛅ Opis: {data['weather'][0]['description']}")
            print("-" * 50)
            print("\n🎉 Twój API key jest poprawny! Problem jest gdzie indziej.")
            return True

        elif response.status_code == 401:
            print("\n❌ ❌ ❌ BŁĄD 401: NIEPRAWIDŁOWY API KEY! ❌ ❌ ❌")
            print("-" * 50)
            print("PRZYCZYNA: API key jest nieważny, wygasł lub nie został aktywowany.")
            print("\n🔧 ROZWIĄZANIE:")
            print("1. Zarejestruj się na: https://openweathermap.org/api")
            print("2. Potwierdź email (ważne!)")
            print("3. Wygeneruj nowy API key")
            print("4. Poczekaj 10-15 minut (nowe klucze potrzebują czasu)")
            print("5. Wklej nowy klucz do pliku config.py")
            print("-" * 50)
            print(f"\n📄 Pełna odpowiedź: {response.text}")
            return False

        elif response.status_code == 429:
            print("\n⚠️  BŁĄD 429: PRZEKROCZONY LIMIT WYWOŁAŃ!")
            print("Darmowy plan ma limit 60 zapytań na minutę / 1,000,000 na miesiąc")
            print("Poczekaj chwilę i spróbuj ponownie.")
            return False

        else:
            print(f"\n⚠️  INNY BŁĄD: {response.status_code}")
            print(f"Treść: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT: Serwer nie odpowiada w ciągu 10 sekund")
        print("Sprawdź połączenie internetowe")
        return False

    except requests.exceptions.ConnectionError:
        print("\n❌ BŁĄD POŁĄCZENIA: Nie można połączyć się z serwerem")
        print("Sprawdź połączenie internetowe")
        return False

    except Exception as e:
        print(f"\n❌ NIESPODZIEWANY BŁĄD: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_forecast_api():
    """Testuje API prognozy (dodatkowo)"""

    API_KEY = "87fa0c47733c2e7eb40a68254ebbf1af"
    lat, lon = 49.2511, 19.9350

    print("\n" + "=" * 60)
    print("🧪 TEST API PROGNOZY (forecast)")
    print("=" * 60)

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pl"

    try:
        response = requests.get(url, timeout=10)
        print(f"Status prognozy: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prognoza działa! Liczba punktów: {len(data.get('list', []))}")
            return True
        else:
            print(f"❌ Błąd prognozy: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "🚀 URUCHAMIANIE TESTOW API")
    print("=" * 60)

    # Test 1: Aktualna pogoda
    weather_ok = test_api_key()

    # Test 2: Prognoza (opcjonalnie)
    if weather_ok:
        forecast_ok = test_forecast_api()

    print("\n" + "=" * 60)
    print("🏁 KONIEC TESTOW")
    print("=" * 60)

    input("\nNaciśnij Enter aby zakończyć...")