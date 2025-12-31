import requests
import time
from config import Config

class WeatherFetcher:
    def __init__(self):
        self.cache = {} # Dane pogodowe
        self.cache_time = {} # Dane czasu

    def _is_cache_valid(self, cache_key):
        if cache_key not in self.cache_time:
            return False # Cache nie pobrane

        saved_time = self.cache_time[cache_key]
        current_time = time.time()
        time_passed = current_time - saved_time

        if time_passed < Config.CACHE_TIME:
            return True # Cache aktualne
        else:
            return False # Cache przedawnione

    def fetch_current_weather(self, lat, lon):
        cache_key = "current_" + str(lat) + "_" + str(lon)

        if self._is_cache_valid(cache_key):
            print("Używam cache dla: ", lat, lon)
            return self.cache[cache_key]

        try:
            url = Config.get_forecast_url(lat, lon)
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                weather_data = response.json()
                self.cache[cache_key] = weather_data
                self.cache_time[cache_key] = time.time()
                print("Pobrano nowe dane dla: ", lat, lon)
                return weather_data
            else:
                print("Błąd API: ", response.status_code)
                return None
        except Exception as e:
            print("Błąd połączenia: ", e)
            return None

    def fetch_forecast(self, lat, lon, days=5):
        cache_key = "Prognoza_" + str(days) + "_" + str(lat) + "_" + str(lon)

        if self._is_cache_valid(cache_key):
            print("Używam cache dla prognozy: ", days, " dni dla: ", lat, lon)
            return self.cache[cache_key]

        try:
            url = Config.get_forecast_url(lat, lon)
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                forecast_data = response.json()

                self.cache[cache_key] = forecast_data
                self.cache_time[cache_key] = time.time()

                print("Pobrano nową prognozę: ", days, "dni dla: ", lat, lon)
                return forecast_data
            else:
                print("Błąd API: ", response.status_code)
                return None
        except Exception as e:
            print("Błąd połączenia: ", e)
            return None

"""
if __name__ == "__main__":
    print("🧪 BARDZO PROSTY TEST")

    try:
        # 1. Utwórz obiekt
        fetcher = WeatherFetcher()
        print("✅ 1. Obiekt utworzony")

        # 2. Sprawdź metodę cache
        fetcher.cache["test"] = {"data": "test"}
        fetcher.cache_time["test"] = time.time()

        if fetcher._is_cache_valid("test"):
            print("✅ 2. Metoda is_cache_valid działa")
        else:
            print("❌ 2. is_cache_valid nie działa")

        # 3. Wywołaj główną metodę
        print("\n🔍 3. Test fetch_current_weather...")
        result = fetcher.fetch_current_weather(52.23, 21.01)

        if result is not None:
            print(f"✅ 3. fetch_current_weather zwrócił dane")
            print(f"   Typ danych: {type(result)}")
            print(f"   Klucze: {list(result.keys()) if isinstance(result, dict) else 'nie dict'}")
        else:
            print("⚠️  3. fetch_current_weather zwrócił None")
            print("   (Może brak API key lub błąd połączenia)")

        print("\n🎉 Test zakończony!")

    except AttributeError as e:
        print(f"\n❌ BŁĄD: {e}")
        print("Sprawdź nazwy metod w klasie WeatherFetcher!")
        print("Powinno być: fetch_current_weather()")

    except Exception as e:
        print(f"\n❌ Niespodziewany błąd: {type(e).__name__}: {e}")

    input("\nNaciśnij Enter...")
"""







