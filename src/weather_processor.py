from src.peaks_database import szczyty_tatr
from datetime import datetime


class WeatherProcessor:
    temp_lapse_rate = 0.6 # Spadek temperatury na 100m
    pressure_lapse_rate = 12
    wind_danger_threshold = 15 # m/s niebezpieczny wiatr
    wind_caution_threshold = 10
    visibility_threshold = 1000 # metrów słaba widoczność

    @staticmethod
    def process_mountain_weather(raw_data, peak_info):
        if not raw_data:
            print("Brak danych do przetworzenia!")
            return  None

        try:
            valley_temperature = raw_data['main']['temp']
            wind_speed = raw_data['wind']['speed']
            humidity = raw_data['main']['humidity']
            weather_description = raw_data['weather'][0]['description']
            pressure = raw_data['main']['pressure']
            visibility = raw_data.get('visibility', 10000)
        except Exception as e:
            print(f"Brakuje klucza w danych: {e}")
            return None

        peak_name = peak_info['name']
        height = peak_info['elevation']
        region = peak_info['region']
        country = peak_info['country']

        peak_temperature = WeatherProcessor.adjust_the_temperature_to_the_altitude(
            valley_temperature, height
        )

        pressure_peak = WeatherProcessor.adjust_the_pressure_to_the_altitude(
            pressure, height
        )

        rate = WeatherProcessor.assess_mountain_conditions(
            peak_temperature, wind_speed, weather_description, visibility
        )

        result = {
            'nazwa szczytu' : peak_name,
            'wysokosc' : height,
            'region' : region,
            'kraj' : country,

            'Temperatura dolina' : round(valley_temperature, 1),
            'Temperatura szczyt' : round(peak_temperature, 1),

            'wiatr' : round(wind_speed, 1),
            'wilgotność' : humidity,
            'cisnienie' : round(pressure_peak, 0),
            'opis' : weather_description,
            'bezpieczenstwo' : rate

        }
        return result

    @staticmethod
    def adjust_the_temperature_to_the_altitude(valley_temperature, height):
        if height <= 0:
            return valley_temperature # Źle pobrane dane

        hundrets_of_metres_T = height / 100
        temperature_drop = hundrets_of_metres_T  * WeatherProcessor.temp_lapse_rate
        temperature_peak = valley_temperature - temperature_drop

        if temperature_peak < -40:
            temperature_peak = -40

        return temperature_peak

    @staticmethod
    def adjust_the_pressure_to_the_altitude(pressure, height):
        if height <= 0:
            return pressure

        hundrets_of_metres_P = height / 100
        pressure_drop = hundrets_of_metres_P * WeatherProcessor.pressure_lapse_rate
        pressure_peak = pressure - pressure_drop

        if pressure_peak < 500:
            pressure_peak = 500

        return pressure_peak

    @staticmethod
    def assess_mountain_conditions(peak_temperature, wind_speed, weather_description, visibility_threshold):
        weather_lower = weather_description.lower()
        problems = []
        rate_level = "bezpiecznie"

        if wind_speed >= 15:
            problems.append("Wiatr bardzo silny!")
            rate_level = "Niebezpiecznie"
        elif wind_speed >= 10:
            problems.append("Wiatr silny!")
            rate_level = "Ostrożnie"
        elif wind_speed >= 5:
            problems.append("Wiatr umiarkowany")
            rate_level = "Bezpiecznie"
        else:
            problems.append("Wiatr łagodny")

        if 'thunderstorm' in weather_lower or 'storm' in weather_lower:
            problems.append("Burza")
            rate_level = 'Niebezpiecznie'
        elif 'heavy rain' in weather_lower or 'heavy snow' in weather_lower:
            problems.append("Silne opady")
            rate_level = "Niebezpiecznie"
        elif 'rain' in weather_lower or 'drizzle' in weather_lower or 'snow' in weather_lower:
            if rate_level != "Niebezpiecznie":
                problems.append("Opadu deszczu/śniegu")
                if rate_level == "Bezpiecznie":
                    rate_level = "Ostrożnie"

        if visibility_threshold < 1000:
            problems.append("Bardzo słaba widoczność")
            rate_level = "Niebezpiecznie"
        elif visibility_threshold < 3000:
            if rate_level != "Niebezpiecznie":
                problems.append("Ograniczona widoczność")
                if rate_level == "Bezpiecznie":
                    rate_level == "Ostrożnie"

        if peak_temperature < -10:
            problems.append("Bardzo niska temperatura")
            rate_level = "Niebezpiecznie"
        elif peak_temperature < 0:
            if rate_level != "Niebezpiecznie":
                problems.append("Temperatura poniżej zera")
                if rate_level == "Bezpiecznie":
                    rate_level == "Ostrożnie"

        porada = WeatherProcessor._generate_advice(rate_level, problems, peak_temperature)
        finally_rate = {
            'poziom' : rate_level,
            'porada' : porada,
            'problemy' : problems
        }
        return finally_rate

    @staticmethod
    def _generate_advice(rate_level, problems, peak_temperature):
        if rate_level == "Bezpiecznie":
            if peak_temperature > 15:
                return "Doskonałe warunki do wędrówki."
            elif peak_temperature > 5:
                return "Dobre warunki. Weź lekką kurtke na wypadek zmiany pogody"
            else:
                return "Zimno ale bezpiecznie. Ubierz się ciepło na warunki górskie"

        elif rate_level == "Ostrożnie":
            parts_of_advice = ["Warunki wymagają ostrożności"]

            for problem in problems:
                if "Wiatr" in problems:
                    parts_of_advice.append("Uważaj na wiatr")
                elif "Opady" in problems:
                    parts_of_advice.append("Weź odzież przeciw deszczową")
                elif "Widoczność" in problem.lower():
                    parts_of_advice.append("Słaba widoczność")
                elif "Temperatura" in problems:
                    parts_of_advice.append("Ubierz się ciepło")

                if peak_temperature < 0 :
                    parts_of_advice.append("Możliwe oblodzenie szlaków")

            porada = " ".join(parts_of_advice)
            return porada

        else:
            parts_of_advice = ["Warunki są niebezpieczne"]

            if "Burza" in problems:
                parts_of_advice.append("Nie wychodź w góry podczas burzy")
            elif "Wiatr" in problems:
                parts_of_advice.append("Bardzo silny wiatr")
            elif "widoczność" in problems:
                parts_of_advice.append("Bardzo słaba widoczność")
            elif "Temperatura" in problems:
                parts_of_advice.append("Bardzo niska temperatura")

            parts_of_advice.append("Odłóż wyjście na inny dzień!")
            porada = " ".join(parts_of_advice)
            return porada

    def process_forecast_data(self, raw_data, peak_info):
        if not raw_data or 'list' not in raw_data:
            print("Błędne dane pogody")
            return None

        list_of_all_forecast = []
        peak_height = peak_info['elevation']
        peak_name = peak_info['name']

        for forecast in raw_data['list']:
            timestamp = forecast['dt']
            date_time = datetime.fromtimestamp(timestamp)
            date_day = date_time.strftime("%Y-%m-%d")
            hour = date_time.strftime("%H:5M")

            main_data = forecast['main']
            valley_temp = main_data['temp']
            humidity = main_data['humidity']
            pressure = main_data['pressure']
            wind_data = forecast['wind']
            wind_speed = wind_data['speed']

            weather_data = forecast['weather'][0]
            description = weather_data['description']

            peak_temp = self.adjust_the_temperature_to_the_altitude(
                valley_temp, peak_height
            )
            peak_pressure = self.adjust_the_pressure_to_the_altitude(
                pressure, peak_height
            )
            safety_assessment = self.assess_mountain_conditions(
                peak_temp, wind_speed, description, 10000
            )

            forecast_dict = {
                'date_time' : str(date_time),
                'date' : date_day,
                'hour' : hour,
                'temperature valley' : round(valley_temp, 1),
                'temperature peak' : round(peak_temp, 1),
                'pressure' : round(peak_pressure, 0),
                'wind' : round(wind_speed, 1),
                'humidity' : humidity,
                'description' : description,
                'safety' : safety_assessment
            }
            list_of_all_forecast.append(forecast_dict)
            sorted_forecast = sorted(list_of_all_forecast, key=lambda x: x['date_time'])

        if len(sorted_forecast) > 0:
            result = {
                'peak_name' : peak_name,
                'elevation' : peak_height,
                'forecast_count' : len(sorted_forecast),
                'date_range' : f"{sorted_forecast[0]['date']} -> {sorted_forecast[-1]['date']}",
                'forecasts' : sorted_forecast
                }
            return result
        else:
            return None
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
            time_str = forecast_datetime.strftime("%H:%M")

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

            peak_temperature = self.adjust_the_temperature_to_the_altitude(
                valley_temperature, peak_height
            )
            peak_pressure = self.adjust_the_pressure_to_the_altitude(
                valley_pressure, peak_height
            )
            safety_data = self.assess_mountain_conditions(
                peak_temperature, wind_speed, weather_description, 1000
            )

            forecast_dict = {
                'datetime' : str(forecast_datetime),
                'date' : date_str,
                'time' : time_str,
                'temperature_valley' : round(valley_temperature, 1),
                'temperature_peak' : round(peak_temperature, 1),
                'pressure' : round(peak_pressure, 0),
                'wind' : round(wind_speed, 1),
                'humidity' : humidity,
                'description' : weather_description,
                'safety_level' : safety_data['poziom'] if safety_data else 'bezpeicznie',
                'safety_advice' : safety_data['porada'] if safety_data else 'Brak oceny'
            }
            all_forecasts.append(forecast_dict)

            if len(all_forecasts) == 0:
                print("⚠️  Nie udało się przetworzyć żadnej prognozy")
                return None
            sorted_forecasts = sorted(all_forecasts, key=lambda x: x['datetime'])

            result = {
                'peak_name': peak_name,
                'elevation': peak_height,
                'forecast_count': len(sorted_forecasts),
                'date_range': f"{sorted_forecasts[0]['date']} do {sorted_forecasts[-1]['date']}",
                'forecasts': sorted_forecasts
            }
            print(f"✅ Przetworzono {len(sorted_forecasts)} prognoz dla {peak_name}")
            return result



if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTUJEMY WeatherProcessor")
    print("=" * 60)

    # ----------------------------------------------------
    # TEST 1: Metody pomocnicze
    # ----------------------------------------------------
    print("\n1. 📊 TEST METOD POMOCNICZYCH:")
    print("-" * 40)

    # Test adjust_the_temperature_to_the_altitude
    print("\n🌡️  Test adjust_the_temperature_to_the_altitude:")
    test_cases_temp = [
        (20.0, 2500, 5.0),  # 20°C na 2500m = 5°C
        (15.0, 1500, 6.0),  # 15°C na 1500m = 6°C
        (10.0, 0, 10.0),  # 0m = taka sama temperatura
        (25.0, 100, 24.4),  # 25°C na 100m = 24.4°C
    ]

    for valley_temp, height, expected in test_cases_temp:
        result = WeatherProcessor.adjust_the_temperature_to_the_altitude(valley_temp, height)
        passed = abs(result - expected) < 0.5  # Tolerancja 0.5°C
        status = "✅" if passed else "❌"
        print(f"   {status} Dolina: {valley_temp}°C, {height}m → Szczyt: {result:.1f}°C (oczekiwane: {expected}°C)")

    # Test adjust_the_pressure_to_the_altitude
    print("\n📈 Test adjust_the_pressure_to_the_altitude:")
    test_cases_pressure = [
        (1013, 2500, 713),  # 1013 hPa na 2500m = 713 hPa
        (1000, 1500, 820),  # 1000 hPa na 1500m = 820 hPa
        (980, 0, 980),  # 0m = takie samo ciśnienie
    ]

    for pressure, height, expected in test_cases_pressure:
        result = WeatherProcessor.adjust_the_pressure_to_the_altitude(pressure, height)
        passed = abs(result - expected) < 10  # Tolerancja 10 hPa
        status = "✅" if passed else "❌"
        print(f"   {status} Dolina: {pressure}hPa, {height}m → Szczyt: {result:.0f}hPa (oczekiwane: {expected}hPa)")

    # ----------------------------------------------------
    # TEST 2: Ocena warunków
    # ----------------------------------------------------
    print("\n2. 🛡️  TEST OCENY WARUNKÓW (assess_mountain_conditions):")
    print("-" * 40)

    test_cases_assess = [
        # (temp, wiatr, opis, widoczność, oczekiwany poziom)
        (10.0, 8.0, "clear sky", 5000, "bezpiecznie"),
        (5.0, 12.0, "light rain", 2000, "ostroznie"),
        (-5.0, 18.0, "heavy snow", 800, "niebezpiecznie"),
        (20.0, 5.0, "sunny", 10000, "bezpiecznie"),
        (2.0, 9.0, "fog", 500, "niebezpiecznie"),
        (-15.0, 3.0, "clear", 8000, "niebezpiecznie"),
    ]

    for i, (temp, wind, desc, vis, expected) in enumerate(test_cases_assess, 1):
        result = WeatherProcessor.assess_mountain_conditions(temp, wind, desc, vis)
        passed = result['poziom'] == expected
        status = "✅" if passed else "❌"
        print(f"\n   {status} Przypadek {i}:")
        print(f"      Temp: {temp}°C, Wiatr: {wind}m/s, Opis: '{desc}', Widoczność: {vis}m")
        print(f"      Otrzymano: {result['poziom']} (oczekiwane: {expected})")
        if not passed:
            print(f"      Problemy: {result['problemy']}")


    # ----------------------------------------------------
    # TEST 3: Pełne przetwarzanie danych
    # ----------------------------------------------------
    print("\n3. 🏔️  TEST PEŁNEGO PRZETWARZANIA (process_mountain_weather):")
    print("-" * 40)

    # Przykładowe dane API
    sample_raw_data = {
        'main': {
            'temp': 18.5,
            'humidity': 65,
            'pressure': 1013
        },
        'wind': {
            'speed': 12.5,
            'gust': 15.0
        },
        'weather': [
            {'description': 'moderate rain'}
        ],
        'visibility': 2500
    }

    # Przykładowy szczyt
    sample_peak = {
        'name': 'Rysy',
        'elevation': 2501,
        'region': 'Tatry Wysokie',
        'country': 'both'
    }

    print("\n   Dane testowe:")
    print(f"      Temperatura w dolinie: {sample_raw_data['main']['temp']}°C")
    print(f"      Wiatr: {sample_raw_data['wind']['speed']} m/s")
    print(f"      Opis: {sample_raw_data['weather'][0]['description']}")
    print(f"      Szczyt: {sample_peak['name']} ({sample_peak['elevation']} m)")

    result = WeatherProcessor.process_mountain_weather(sample_raw_data, sample_peak)

    if result:
        print("\n   ✅ Wynik przetwarzania:")
        print(f"      Nazwa szczytu: {result['nazwa szczytu']}")
        print(f"      Temperatura dolina/szczyt: {result['Temperatura dolina']}°C / {result['Temperatura szczyt']}°C")
        print(f"      Ciśnienie na szczycie: {result['cisnienie']} hPa")
        print(f"      Wiatr: {result['wiatr']} m/s")
        print(f"      Ocena bezpieczeństwa: {result['bezpieczenstwo']['poziom']}")
        print(f"      Porada: {result['bezpieczenstwo']['porada']}")

        # Sprawdź czy wszystkie wymagane klucze istnieją
        required_keys = ['nazwa szczytu', 'Temperatura dolina', 'Temperatura szczyt',
                         'wiatr', 'cisnienie', 'bezpieczenstwo']
        all_keys_present = all(key in result for key in required_keys)

        if all_keys_present:
            print("\n   ✅ Wszystkie wymagane klucze są obecne w wyniku")
        else:
            missing = [key for key in required_keys if key not in result]
            print(f"\n   ❌ Brakujące klucze: {missing}")
    else:
        print("\n   ❌ Nie udało się przetworzyć danych")

    # ----------------------------------------------------
    # TEST 4: Błędne dane
    # ----------------------------------------------------
    print("\n4. 🚨 TEST OBSŁUGI BŁĘDÓW:")
    print("-" * 40)

    # Test z brakującymi danymi
    bad_data = {'main': {'temp': 20.0}}  # Brakuje innych kluczy
    result_bad = WeatherProcessor.process_mountain_weather(bad_data, sample_peak)

    if result_bad is None:
        print("   ✅ Poprawnie obsłużono błędne dane (zwrócono None)")
    else:
        print("   ❌ Powinno zwrócić None dla błędnych danych")

    # Test z pustymi danymi
    result_empty = WeatherProcessor.process_mountain_weather(None, sample_peak)
    if result_empty is None:
        print("   ✅ Poprawnie obsłużono puste dane")
    else:
        print("   ❌ Powinno zwrócić None dla pustych danych")

    # ----------------------------------------------------
    # TEST 5: Generowanie porad
    # ----------------------------------------------------
    print("\n5. 💡 TEST GENEROWANIA PORAD:")
    print("-" * 40)

    test_advice_cases = [
        ("bezpiecznie", ["Wiatr łagodny"], 20.0),
        ("ostroznie", ["Wiatr silny", "Opady deszczu/śniegu"], 3.0),
        ("niebezpiecznie", ["Burza", "Wiatr bardzo silny"], -5.0),
    ]

    for level, problems, temp in test_advice_cases:
        advice = WeatherProcessor._generate_advice(level, problems, temp)
        print(f"\n   Dla poziomu '{level}' (temp: {temp}°C):")
        print(f"      Porada: {advice[:80]}...")

    # ----------------------------------------------------
    # PODSUMOWANIE
    # ----------------------------------------------------
    print("\n" + "=" * 60)
    print("📋 PODSUMOWANIE TESTÓW")
    print("=" * 60)
    print("\nWeatherProcessor powinien:")
    print("✅ Dostosowywać temperaturę do wysokości")
    print("✅ Dostosowywać ciśnienie do wysokości")
    print("✅ Oceniać warunki górskie (bezpieczeństwo)")
    print("✅ Generować porady dla turystów")
    print("✅ Obsługiwać błędne dane (zwracać None)")
    print("✅ Zwracać pełne dane w słowniku")
    print("\n" + "=" * 60)
    print("🏁 KONIEC TESTOWANIA")
    print("=" * 60)




