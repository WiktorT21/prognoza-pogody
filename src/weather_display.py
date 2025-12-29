from datetime import datetime

from statsmodels.tsa.vector_ar.var_model import forecast

from weather_processor import WeatherProcessor
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


    def show_forecast(self, raw_data, peak_info):
        if raw_data is None:
            print("❌ Błąd: Brak danych prognozy")
            return None
        if 'list' not in raw_data.keys():
            print("❌ Błąd: Nieprawidłowa struktura danych")
        if len(raw_data['list']) == 0:
            print("❌ Błąd: Lista prognoz jest pusta")
            return None

        all_forecasts = []
        peak_name = peak_info['name']
        peak_height = peak_info['elevation']
        region = peak_info['region']
        country = peak_info['country']

        for single_forecast in raw_data['list']:
            timestamp = single_forecast['dt']
            forecast_datetime = datetime.fromtimestamp(timestamp)
            date_str = forecast_datetime.strftime("%Y-%m-%d")
            time_str = forecast_datetime.strftime("%H-%M")

            if 'main' not in single_forecast:
                continue
            main_data = single_forecast['main']

            if 'temp' in main_data:
                valley_temperature = main_data['temp']
            else:
                valley_temperature = 0

            if 'humidity' in main_data:
                humidity = main_data['humidity']
            else:
                humidity = 0

            if 'pressure' in main_data:
                valley_pressure = main_data['pressure']
            else:
                valley_pressure = 1013

            if 'wind' in single_forecast:
                wind_data = single_forecast['wind']
                if 'speed' in wind_data:
                    wind_speed = wind_data['speed']
                else:
                    wind_speed = 0
            else:
                wind_speed = 0

            if 'weather' in single_forecast and len(single_forecast['weather']) > 0:
                weather_info = single_forecast['weather'][0]
                if 'description' in weather_info:
                    weather_description = weather_info['description']
                else:
                    weather_description = "Brak opisu"
            else:
                weather_description = "Brak opisu"


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

