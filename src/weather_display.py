from datetime import datetime

class WeatherDisplay:
    @staticmethod
    def show_mountain_weather(result):
        if not result:
            print("Brak danych do wyświetlenia")
            return

        nazwa = result['nazwa szczytu']
        wyskosc = result['wysokosc']
        Temp_dolina = result['Temperatura dolina']
        Temp_szczyt = result['Temperatura szczyt']
        wiatr = result['wiatr']
        wilgotnosc = result['wilgotność']
        cisnienie = result['cisnienie']
        opis = result['opis']
        bezpieczenstwo = result['bezpieczenstwo']

        if isinstance(bezpieczenstwo, dict):
            poziom = bezpieczenstwo.get('poziom', 'bezpiecznie')
            porada = bezpieczenstwo.get('porada', '')
        else:
            poziom = bezpieczenstwo  # String

        print("")
        print("⛰️"*10)
        print(f"{nazwa.upper()} - {wyskosc} m n.p.m")
        print("⛰️"*10)
        print("")

        print("🌡️ Temperatury:")
        print(f"W dolinie: {Temp_dolina} °C")
        print(f"Na szczycie: {Temp_szczyt} °C")
        print("")

        print("📊 Warunki pogodowe:")
        if wiatr < 5:
            opis_wiatru = "łagodny"
        elif wiatr < 10:
            opis_wiatru = "umiarkowany"
        elif wiatr < 15:
            opis_wiatru = "silny"
        else:
            opis_wiatru = "bardzo silny"

        print(f"💨 Wiatr: {wiatr:.1f} m/s {opis_wiatru}")
        print(f"💧 Wilgotność: {wilgotnosc}%")
        print(f"📈 Ciśnienie: {cisnienie} hPA")
        print("")

        poziom = result['bezpieczenstwo']

        print("🛡️ Ocena bezpieczeństwa: ")
        if poziom == 'bezpiecznie':
            print("✅ Warunki Bezpieczne")
            print("🟢 Możesz bezpiecznie planować wyjście w góry")
        elif poziom == 'ostroznie':
            print("⚠️ Wymaga ostrożności")
            print(f"🟡 Zachowaj ostrożność, warunki mogą być trudne")
        elif poziom == 'niebezpiecznie':
            print(f"🚨 Warunki niebezpieczne")
            print(f"🔴 Odradzamy wyjsście w góry")
        print("")

    @staticmethod
    def show_quick_view(result):
        nazwa = result['nazwa szczytu']
        Temp_szczyt = result['Temperatura szczyt']
        wiatr = result['wiatr']
        bezpieczenstwo = result['bezpieczenstwo']
        poziom = result['bezpieczenstwo']

        if isinstance(bezpieczenstwo, dict):
            poziom = bezpieczenstwo.get('poziom', 'bezpiecznie')
        else:
            poziom = bezpieczenstwo  # String

        if poziom == 'bezpiecznie':
            kropka = "✅"
        elif poziom == 'ostroznie':
            kropka = "⚠️"
        else:
            kropka = "🚨"

        print(f"{nazwa} | {Temp_szczyt} | {wiatr} | {kropka}")


    def show_forecast(self, peak_info, processed_data):
        if processed_data is None:
            print("❌ Brak danych do wyświetlenia")
            return

        if 'forecasts' not in processed_data:
            print("❌ Brak prognoz w danych")
            return

        peak_name = processed_data['peak_name']
        elevation = processed_data['elevation']
        forecast_count = processed_data['forecast_count']
        date_range = processed_data['date_range']

        # Nagłówek NAJPIERW
        print("\n" + "⛰️" * 20)
        print(f"📅 PROGNOZA POGODY DLA: {peak_name.upper()}")
        print(f"📍 Wysokość: {elevation} m n.p.m.")
        print(f"📊 Liczba prognoz: {forecast_count}")
        print(f"⏰ Zakres: {date_range}")
        print("⛰️" * 20)

        # Grupowanie prognoz według dni
        forecasts_by_day = {}
        for forecast in processed_data['forecasts']:
            date = forecast['date']
            if date not in forecasts_by_day:
                forecasts_by_day[date] = []
            forecasts_by_day[date].append(forecast)

        print("\n📅 PODSUMOWANIE DZIENNE:")
        print("-" * 50)

        # Wyświetlanie podsumowania dla każdego dnia
        for date in sorted(forecasts_by_day.keys()):
            day_forecasts = forecasts_by_day[date]

            # Zbierz dane z tego dnia
            temps = []
            winds = []
            safeties = []
            descriptions = []

            for f in day_forecasts:
                # Temperatura
                temp = f.get('temperature_peak') or f.get('temperature peak') or 0
                temps.append(float(temp))

                # Wiatr
                wind = f.get('wind') or 0
                winds.append(float(wind))

                # Bezpieczeństwo
                safety = f.get('safety', {})
                if isinstance(safety, dict):
                    level = safety.get('poziom', 'bezpiecznie')
                else:
                    level = str(safety)
                safeties.append(level)

                # Opis
                desc = f.get('description', '')
                descriptions.append(desc)

            # Oblicz statystyki
            temp_min = min(temps) if temps else 0
            temp_max = max(temps) if temps else 0
            wind_max = max(winds) if winds else 0

            # Znajdź najgorszy poziom bezpieczeństwa
            if 'niebezpiecznie' in safeties:
                worst_safety = 'niebezpiecznie'
                emoji = "🔴"
            elif 'ostroznie' in safeties:
                worst_safety = 'ostroznie'
                emoji = "🟡"
            else:
                worst_safety = 'bezpiecznie'
                emoji = "🟢"

            # Najczęstszy opis pogody
            most_common = ""
            if descriptions:
                most_common = max(set(descriptions), key=descriptions.count)

            # Wyświetl podsumowanie dnia
            print(f"\n{emoji} 📅 {date}:")
            print(f"   🌡️  Temperatura: {temp_min:.1f}°C → {temp_max:.1f}°C")
            print(f"   💨 Maks. wiatr: {wind_max:.1f} m/s")
            print(f"   🛡️  Bezpieczeństwo: {worst_safety.upper()}")

            if most_common:
                print(f"   ⛅ Główne warunki: {most_common}")
            print(f"   📊 Prognoz w dniu: {len(day_forecasts)}")

        print("\n" + "-" * 50)
        print(f"✅ Wyświetlono prognozę na {len(forecasts_by_day)} dni")


if __name__ == "__main__":
    # Przykładowe dane do testu
    test_data = {
        'nazwa szczytu': 'Rysy',
        'wysokosc': 2501,
        'Temperatura dolina': 20.5,
        'Temperatura szczyt': 5.2,
        'wiatr': 12.3,
        'wilgotnosc': 78,
        'cisnienie': 845,
        'opis': 'light rain with wind',
        'bezpieczenstwo': {
            'poziom': 'ostroznie',  # LUB 'rate': 'ostroznie' - zależy od twojego kodu
            'porada': 'Uważaj na silny wiatr i deszcz. Załóż kurtkę przeciwdeszczową.'
        }
    }

    print("🧪 TEST WeatherDisplay")
    print("=" * 50)
    print("")

        # Test pełnego wyświetlania
    WeatherDisplay.show_mountain_weather(test_data)

    print("")
    print("🧪 Test krótkiego podglądu:")
    WeatherDisplay.show_quick_view(test_data)

