from dask.array import around

from src.peaks_database import szczyty_tatr


class WeatherProcessor:
    temp_lapse_rate = 0.6 # Spadek temperatury na 100m
    wind_danger_threshold = 15 # m/s niebezpieczny wiatr
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
        except Exception as e:
            print(f"Brakuje klucza w danych: {e}")
            return None

        peak_name = szczyty_tatr['name']
        height = szczyty_tatr['elevation']
        region = szczyty_tatr['region']
        country = szczyty_tatr['country']

        peak_temperature = WeatherProcessor.adjust_the_temperature_to_the_altitude(
            valley_temperature, height
        )

        pressure_peak = WeatherProcessor.adjust_the_pressure_to_the_altitude(
            pressure, height
        )

        rate = WeatherProcessor.assess_mountain_conditions(
            peak_temperature, wind_speed, weather_description
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


