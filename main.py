import sys
import os

from lief import exception


def add_path():
    current_file_path = os.path.abspath(__file__)
    main_folder = os.path.dirname(current_file_path)
    folder_src = os.path.join(main_folder, 'src')

    if not os.path.exists(folder_src):
        print(f"Błąd: Nieodnaleziono folderu 'src/' w {main_folder}")
        print("Stwórz folder 'src' i umieść w nim wsyztskie pliki .py")
        return False
    if folder_src not in sys.path:
        sys.path.insert(0, folder_src)
        print(f"📁 Dodano ścieżkę: {folder_src}")
    return True

def main():
    print("\n" + "="*60)
    print("🌄  URUCHAMIANIE APLIKACJI POGODOWEJ DLA TATR")
    print("="*60)

    print("\n🔧 Konfiguracja środowiska...")
    if not add_path():
        input("\nNaciśnij Enter aby zakończyć...")
        return
    print("📦 Ładowanie modułów...")

    try:
        from src.mountain_weather_app import MountainWeatherApp
        print("✅ Wszystkie moduły zaimportowane pomyślnie!")
    except ImportError as e:
        print(f"\n❌ KRYTYCZNY BŁĄD IMPORTU: {e}")
        print("\n🔍 PRZYCZYNA: Brakuje któregoś z wymaganych plików.")
        print("\n📁 SPRAWDŹ STRUKTURĘ PROJEKTU:")
        print("Twój folder powinien wyglądać tak:")
        print("")
        print("prognoza-pogody/")
        print("├── src/")
        print("│   ├── data_fetcher.py")
        print("│   ├── weather_processor.py")
        print("│   ├── weather_display.py")
        print("│   ├── peaks_database.py")
        print("│   └── mountain_weather_app.py")
        print("├── config.py")
        print("└── main.py  <-- TEN PLIK")
        print("")

        input("naciśnij Enter aby zakończyć...")
        return

    print("\n🚀 Uruchamiam główną aplikację...")
    print("-"*40)

    try:
        app = MountainWeatherApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Aplikacja przerwana przez użytkownika (Ctrl+C).")
    except Exception as e:
        print(f"\n❌ NIESPODZIEWANY BŁĄD: {type(e).__name__}")
        print(f"Szczegóły: {e}")

        input("\nNaciśnij Enter aby zakończyć...")

    print("\n" + "="*60)
    print("🏁 PROGRAM ZAKOŃCZONY")
    print("="*60)

if __name__ == "__main__":
    main()
    print('\n💡 Wskazówka: Aby uruchomić ponownie, wpisz: python main.py')
