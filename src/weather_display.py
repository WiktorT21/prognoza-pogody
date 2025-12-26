from weather_processor import WeatherProcessor

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

        if poziom == 'bezpiecznie':
            kropka = "✅"
        elif poziom == 'ostroznie':
            kropka = "⚠️"
        else:
            kropka = "🚨"

        print(f"{nazwa} | {Temp_szczyt} | {wiatr} | {kropka}")


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

