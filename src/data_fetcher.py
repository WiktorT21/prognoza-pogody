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

    # Na końcu data_fetcher.py dodaj:
if __name__ == "__main__":
    print("=== Test _is_cache_valid ===")

    fetcher = WeatherFetcher()

    # Test 1: Klucz który nie istnieje
    test1 = fetcher._is_cache_valid("test_key")
    print(f"Test 1 (nieistniejący klucz): {test1} - powinno być: False")

    # Test 2: Dodaj klucz i sprawdź od razu
    fetcher.cache_time["test_key"] = time.time()
    test2 = fetcher._is_cache_valid("test_key")
    print(f"Test 2 (świeży klucz): {test2} - powinno być: True")

    # Test 3: Stary klucz (symulacja)
    fetcher.cache_time["old_key"] = time.time() - 400  # 400 sekund temu
    test3 = fetcher._is_cache_valid("old_key")
    print(f"Test 3 (stary klucz, 400s): {test3} - powinno być: False")

    print("\n✅ Testy zakończone!")




