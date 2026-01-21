import sys
import os
import traceback

print("=" * 60)
print("🌄 APLIKACJA POGODOWA DLA TATR")
print("=" * 60)

# Dodaj folder src do ścieżki
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')

if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)
    print(f"📁 Używam folderu src: {src_dir}")
else:
    print(f"📁 Używam bieżącego folderu: {current_dir}")

# Dodaj bieżący folder też
sys.path.insert(0, current_dir)

print("\n🔍 Sprawdzam pliki...")

# Sprawdź czy mamy kluczowe pliki
required_files_in_src = [
    'data_fetcher.py',
    'peaks_database.py',
    'weather_processor.py',
    'weather_display.py',
    'mountain_weather_app.py',
    'gui_weather_app.py'
]

all_ok = True
for file in required_files_in_src:
    # Sprawdź w src
    file_path_src = os.path.join(src_dir, file) if os.path.exists(src_dir) else None
    # Sprawdź w bieżącym
    file_path_current = os.path.join(current_dir, file)

    if file_path_src and os.path.exists(file_path_src):
        print(f"✅ {file} (w src/)")
    elif os.path.exists(file_path_current):
        print(f"✅ {file} (w bieżącym)")
        # Jeśli plik jest w bieżącym, dodaj jego folder do ścieżki
        sys.path.insert(0, os.path.dirname(file_path_current))
    else:
        print(f"❌ {file} - NIE ZNALEZIONY")
        all_ok = False

if not all_ok:
    print("\n❌ Brakuje niektórych plików!")
    input("Naciśnij Enter aby zakończyć...")
    sys.exit(1)

print("\n📦 Ładowanie modułów...")

try:
    # Import głównej aplikacji
    from mountain_weather_app import MountainWeatherApp

    print("✅ mountain_weather_app załadowany")

    # Spróbuj załadować GUI
    try:
        from gui_weather_app import WeatherGUI

        has_gui = True
        print("✅ gui_weather_app załadowany")
    except ImportError as e:
        print(f"⚠️  Nie udało się załadować GUI: {e}")
        has_gui = False

except ImportError as e:
    print(f"\n❌ KRYTYCZNY BŁĄD IMPORTU: {e}")
    print("\n🔍 Przyczyna: Problem z importami w plikach")
    print("1. Sprawdź czy w weather_processor.py jest: from peaks_database import szczyty_tatr")
    print("2. Sprawdź czy wszystkie pliki są w folderze src/")
    input("\nNaciśnij Enter aby zakończyć...")
    sys.exit(1)

# Uruchom aplikację
try:
    app = MountainWeatherApp()

    print("\n🔧 Wybierz tryb działania:")
    print("1. Tryb konsolowy (CLI)")
    if has_gui:
        print("2. Tryb graficzny (GUI)")

    choice = input("\nTwój wybór (1-2): ").strip()

    if choice == "1":
        app.run()
    elif choice == "2" and has_gui:
        gui = WeatherGUI(app)
        gui.run()
    else:
        print("⚠️  Nieprawidłowy wybór lub GUI niedostępne, uruchamiam tryb konsolowy...")
        app.run()

except Exception as e:
    print(f"\n❌ BŁĄD URUCHAMIANIA: {e}")
    traceback.print_exc()
    input("\nNaciśnij Enter aby zakończyć...")

print("\n🏔️  Do zobaczenia na szlaku!")
