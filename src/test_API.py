import requests
from config import Config

# Test API key
print("🧪 TEST API KEY")
url = Config.get_forecast_url(49.1639, 20.1317)
print(f"URL: {url}")

response = requests.get(url)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ API działa! Liczba prognoz: {len(data.get('list', []))}")
    print(f"Klucze: {list(data.keys())}")
else:
    print(f"❌ Błąd: {response.text[:200]}")