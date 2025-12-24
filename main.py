import sys
import os

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