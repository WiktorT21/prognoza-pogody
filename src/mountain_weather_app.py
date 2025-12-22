from random import choice

from data_fetcher import WeatherFetcher
from weather_processor import WeatherProcessor
from weather_display import WeatherDisplay
from peaks_database import get_peak_info, get_all_peaks, szczyty_tatr

class MountainWeatherApp:
    def __init__(self):
        self.fetcher = WeatherFetcher
        self.processor = WeatherProcessor
        self.display = WeatherDisplay
        self.peaks_db = szczyty_tatr

    def run(self):
        self._display_welcome()

        while True :
            self._display_menu()
            choice = input("Twój wybór (1-4): ")
            choice = choice.strip()

            if choice == "1":
                self._check_one_peak()
            elif choice == "2":
                self._check_all_peaks()
            elif choice == "3":
                self._check_forecast()
            elif choice == "4":
                print("\n🏔️  Do zobaczenia na szlaku! 🏔️")
                break
            else:
                print(" ❌ Nieprawdiłowy wybór sprubuj ponownie")

    def _display_welcome(self):
        print("\n" + "=" * 50)
        print("🌄  APLIKACJA POGODOWA DLA TATR  🌄")
        print("="*50)
        print("\nSprawdź warunki pogodowe na szczytach Tatrzańskich!")
        print(f"Dostępnych szczytów: {len(self.peaks_db)}")

    def _display_menu(self):
        print("\n" + "-" * 30)
        print(" 📋  MENU GŁÓWNE")
        print("-" * 30)
        print("1. 🔍 Sprawdź pogodę dla wybranego szczytu")
        print("2. 📊 Sprawdź pogodę dla wszystkich szczytów")
        print("3. 📅 Sprawdź prognozę na kilka dni")
        print("4. 🚪 Wyjdź z aplikacji")

    def _check_one_peak(self):
        print("\n" + "=" * 50)
        print("🏔️  WYBIERZ SZCZYT")
        print("\n" + "=" * 50)

        list_of_peaks = list(self.peaks_db.keys())
        list_of_peaks.sort()

        for i, peak_name in enumerate(list_of_peaks, start=1):
            print(f"{i:2}. {peak_name}")

        try:
            choice = int(input(f"\nWybierz numer szczytu (1-{len(list_of_peaks)}): "))

            if 1 <= choice <= len(list_of_peaks):
                chosen_peak = list_of_peaks[choice - 1]
                self._get_and_show_peak(chosen_peak)
            else:
                print("❌ Nieprawidłowy numer")
        except ValueError:
            print("❌ To nie jest liczba!")

    def _get_and_show_peak(self, peak_name):
        print(f"\n⌛ Pobieram dane dla {peak_name}...")

        peak_info = get_peak_info(peak_name)
        if not peak_info:
            print(f"❌ Nie znaleziono szczytu: {peak_name}")
            return

        raw_data = self.fetcher.fetch_current_weather(
            peak_info["lat"],
            peak_info["lon"]
        )

        if not raw_data:
            print("❌ Nie udało się pobrać danych pogodowych")
            print("(Sprawdź połączenie internetowe i klucz API)")
            return

        processed_data = self.processor.process_mountain_weather(
            raw_data, peak_info
        )

        if not processed_data:
            print("❌ Nie udało się przetworzyć danych")
            return

        print("\n" + "="*50)
        self.display.show_mountain_weather(processed_data)

        save = input("\n💾 Czy zapisać te dane do pliku? (t/n): ".lower())
        if save == 't':
            self._save_to_file(peak_name, processed_data)