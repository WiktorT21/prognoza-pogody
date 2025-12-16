"""
Configuration management for weather API
SIMPLIFIED VERSION - no .env file reading
"""
import os


class Config:
    """Application configuration"""
    CACHE_TIME = 300
    # HARDCODE your API key here TEMPORARILY
    OPENWEATHER_API_KEY = "87fa0c47733c2e7eb40a68254ebbf1af"  # <-- TWÓJ KLUCZ

    # API URLs
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    # Application settings
    UNITS = "metric"  # metric for °C, imperial for °F
    LANGUAGE = "pl"

    @classmethod
    def validate_api_key(cls):
        """Check if API key is set"""
        if not cls.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY is not set")
        return True

    @classmethod
    def get_weather_url(cls, lat, lon):
        """Generate URL for current weather"""
        return (
            f"{cls.OPENWEATHER_URL}?"
            f"lat={lat}&lon={lon}&"
            f"appid={cls.OPENWEATHER_API_KEY}&"
            f"units={cls.UNITS}&lang={cls.LANGUAGE}"
        )

    @classmethod
    def get_forecast_url(cls, lat, lon):
        """Generate URL for 5-day forecast"""
        return (
            f"{cls.OPENWEATHER_FORECAST_URL}?"
            f"lat={lat}&lon={lon}&"
            f"appid={cls.OPENWEATHER_API_KEY}&"
            f"units={cls.UNITS}&lang={cls.LANGUAGE}"
        )


# Test
if __name__ == "__main__":
    print("Testing Config class...")
    print(f"API Key: {Config.OPENWEATHER_API_KEY[:10]}...")

    # Generate test URL
    url = Config.get_weather_url(49.2992, 19.9492)
    print(f"Test URL: {url[:80]}...")

    # Try to fetch data (optional)
    try:
        import requests

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API działa! Temperatura w Zakopanem: {data['main']['temp']}°C")
        else:
            print(f"❌ Błąd API: {response.status_code}")
    except ImportError:
        print("ℹ️ requests nie zainstalowany, pomijam test API")