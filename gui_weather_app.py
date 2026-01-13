import tkinter as tk
from itertools import count
from tkinter import ttk, Toplevel, messagebox

from astropy.units.quantity_helper.function_helpers import insert
from pyflakes.checker import counter


class WeatherGUI:
    def __init__(self, weather_app):
        self.weather_app = weather_app
        self.root = tk.Tk()

        self.root.title("🌄 Aplikacja Pogodowa dla Tatr")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f8ff")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            'Title.TLabel',
            font = ('Arial', 24, 'bold'),
            background= '#f0f8ff',
            foreground='#2c3e50'
        )

        style.configure(
            'Header.TLabel',
            font=('Arial', 14, 'bold'),
            background='#f0f8ff',
            foreground='#2c3e50'
        )

        style.configure(
            'Normal.TLabel',
            font=('Arial', 11),
            background='#f0f8ff',
            foreground='#2c3e50'
        )

        style.configure(
            'Green.TButton',
            font=('Arial', 11, 'bold'),
            background='green',
            foreground='white',
            padding= 10
        )

        style.configure(
            'Blue.TButton',
            font=('Arial', 11, 'bold'),
            background='blue',
            foreground='white',
            padding=10
        )

        style.configure(
            'Red.TButton',
            font=('Arial', 11, 'bold'),
            background='green',
            foreground='white',
            padding=10
        )

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#f0f8ff')
        header_frame.pack(fill="x", pady=10)

        title_label = ttk.Label(
            header_frame,
            text="🌄 APLIKACJA POGODOWA DLA TATR 🌄",
            style='title.TLabel'
        )
        title_label.pack()

        subtitle_label = ttk.Label(
              header_frame,
            text="Sprawdź warunki pogodowe na szczytach Tatrzańskich!",
            style="Normal.TLabel"
        )
        subtitle_label.pack()

        main_frame = tk.Frame(
            self.root,
            bg="#f0f8ff"
        )
        main_frame.pack(
            pady=20,
            padx=20,
            fill="both",
            expand=True
        )

        left_frame = tk.Frame(
            main_frame,
            bg='#ecf0f1',
            relief='ridge',
            borderwidth=2
        )
        left_frame.pack(
            side='left',
            fill='y',
            padx= (0, 10)
        )

        menu_label = ttk.Label(
            left_frame,
            text="📋 MENU GŁÓWNE",
            style="Header.TLabel"
        )
        menu_label.pack(
            pady=20
        )

        buttons = [
            ("🔍 Sprawdź pogodę dla wybranego szczytu", self.show_single_peak),
            ("📊 Sprawdź pogodę dla wszystkich szczytów", self.show_all_peaks),
            ("📅 Sprawdź prognozę na 5 dni", self.show_forecast),
            ("🚪 Wyjdź z aplikacji", self.exit_app)
        ]

        for text, command in buttons:
            btn = ttk.Button(
                left_frame,
                text=text,
                command=command,
                style='Green.TButton',
                width=35
            )
            btn.pack(pady=10, padx=20)

        right_frame = tk.Frame(
            main_frame,
            bg='white',
            relief='sunken',
            borderwidth=2
        )
        right_frame.pack(
            side='right',
            fill='both',
            expand=True
        )

        text_frame = tk.Frame(right_frame, bg='white')
        text_frame.pack(pady=10, padx=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient='vertical',
        )

        self.result_text = tk.Text(
            right_frame,
            wrap='word',
            font=('Courier New', 10),
            bg='white',
            fg='black',
            height=30,
            width=70,
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(command=self.result_text.yview)

        self.result_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        footer_frame = tk.Frame(
            self.root,
            bg='#f0f8ff'
        )
        footer_frame.pack(side='bottom', pady=10)

        peaks_count = len(self.weather_app.peaks_db)
        footer_label = ttk.Label(
            footer_frame,
            text=f"Dostępnych szcytów: {peaks_count}",
            style='Normal.TLabel'
        )
        footer_label.pack()

    def show_single_peak(self):
        dialog = Toplevel(self.root)
        dialog.title("🏔️ Wybierz szczyt")
        dialog.geometry("400x500")
        dialog.configure(bg="#a7d8ff")

        label = ttk.Label(
            dialog,
            text="Wybierz szczyt do sprawdzenia: ",
            style='Header.TLabel'
        )
        label.pack(pady=20)

        listbox_frame = ttk.Frame(dialog, bg="#f0f8ff")
        listbox_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 11),
            bg='white',
            selectbackground='#3498db',
            height=12
        )
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        list_of_peaks = list(self.weather_app.peaks_db.keys())
        list_of_peaks.sort()

        for i, peak_name in list_of_peaks:
            listbox.insert(tk.END, f"{i:2}. {peak_name}")

    def display_single_peak(self, peak_name):
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f"\n⌛ Pobieram dane dla {peak_name}...\n")
        self.root.update()

        peak_info = self.weather_app.peaks_db.get(peak_name)

        if peak_info is None:
            messagebox.showerror("Błąd", f"Nie znaleziono szczytu: {peak_name}")
            return

        raw_data = self.weather_app.fetcher.fetch_current_weather(
            lat = peak_info['lat'],
            long = peak_info['lon']
        )

        if raw_data is None:
            messagebox.showerror("Błąd", "Nie udało się pobrać danych pogodowych")
            return

        processed_data = self.weather_app.processor.process_mountain_weather(
            raw_data = raw_data,
            peak_info = peak_info
        )

        if processed_data is None:
            messagebox.showerror("Błąd", "Nie udało się przetworzyć danych")
            return

        self.result_text.delete("1.0", "end")
        self.display_weather_data(processed_data)

    def display_weather_data(self, data):
        header_line = "⛰️" * 20 + "\n"

        self.result_text.insert(tk.END, header_line)
        self.result_text.insert(tk.END, f"{data['peak_name'].upper()} - {data['height']} m n.p.m\n")
        self.result_text.insert(tk.END, header_line + "\n")

        self.result_text.insert(tk.END, "🌡️ Temperatury:\n")
        self.result_text.insert(tk.END, f"W dolinie {data['Temperatura dolina']} °C\n")
        self.result_text.insert(tk.END, f"Na szczycie: {data['Temperatura szczyt']} °C\n")

        self.result_text.insert(tk.END, "📊 Warunki pogodowe:\n" )

        wind = data['wind']

        if wind < 5:
            wind_description = "łagodny"
        elif wind < 10:
            wind_description = "umiarkowany"
        elif wind < 15:
            wind_description = "silny"
        else:
            wind_description = "bardzo silny"

        self.result_text.insert(tk.END, f"💨 Wiatr:   {round(wind, 1)} m/s {wind_description}\n")
        self.result_text.insert(tk.END, f"💧 Wilgotność: {str(data['humidity'])} &\n")
        self.result_text.insert(tk.END, f"📈 Ciśnienie: {str(data['pressure'])} hPa\n")
        self.result_text.insert(tk.END, f"⛅ Opis: {str(data['description'])}\n\n")

        self.result_text.insert(tk.END, "🛡️ Ocena bezpieczeństwa:\n")

        safety_level = data['safety_level']

        if safety_level == 'bezpiecznie':
            self.result_text.insert(tk.END, "✅ Warunki Bezpieczne\n")
            self.result_text.insert(tk.END, "🟢 Możesz bezpiecznie planować wyjście w góry\n")
        elif safety_level == 'ostrożnie':
            self.result_text.insert(tk.END, "⚠️ Wymaga ostrożności\n")
            self.result_text.insert(tk.END, "🟡 Zachowaj ostrożność, warunki mogą być trudne\n")
        elif safety_level == 'niebezpiecznie':
            self.result_text.insert(tk.END, "🚨 Warunki niebezpieczne\n")
            self.result_text.insert(tk.END, "🔴 Odradzamy wyjście w góry\n")

    def show_all_peaks(self):
        self.result_text.delete("1.0", "end")
        self.result_text.insert(tk.END, "\n⌛ Pobieranie danych... (może chwilę potrwać)\n")
        self.root.update_idletasks()
        self.root.update()

        def fetch_all_peaks():
            try:
                results = []
                all_peaks = self.weather_app.peaks_db.keys()
                all_peaks.sort()

                for i, peak_name in enumerate(all_peaks, 1):
                    self.result_text.insert(tk.END, f"[{i}/{len(all_peaks)}] {peak_name}...\n")
                    self.root.update()

                    peak_info = self.weather_app.peaks_db.get(peak_name)

                    if peak_info is not None:
                        raw_data = self.weather_app.fetcher.fetch_current_weather(
                            self.weather_app.fetcher,
                            peak_info['lat'],
                            peak_info['lon']
                        )
                        if raw_data is not None:
                            processed = self.weather_app.processor.process_mountain_weather(
                                raw_data,
                                peak_info
                            )
                            if processed is not None:
                                results.append(processed)
                self.root.after(0, lambda: self.display_all_peaks_summary(results))
            except Exception as e:
                self.root.after(0, lambda: self.result_text.insert(tk.END, f"❌ Błąd: {e}\n"))

        import threading
        thread = threading.Thread(target=fetch_all_peaks, daemon=True)
        thread.start()

    def display_all_peaks_summary(self, results):
        self.clear_screen()

        if not results:
            self.result_text.insert(tk.END, "❌ Nie udało się pobrać żadnych danych!\n")
            self.result_text.insert(tk.END, "   Sprawdź połączenie internetowe i klucz API.\n")
            return

        self.result_text.insert(tk.END, "=" * 50 + "\n")
        self.result_text.insert(tk.END, "📊 POGODA WE WSZYSTKICH SZCZYTACH\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")

        counter_safe = 0
        counter_caution = 0
        counter_dangerous = 0

        for result in results:
            safety_level = result['bezpieczenstwo']

            if isinstance(safety_level, dict):
                safety_level = safety_level.get('poziom', 'bezpiecznie')
            else:
                safety_level = safety_level

            if safety_level == 'bezpiecznie':
                counter_safe += 1
            elif safety_level == 'ostroznie':
                counter_caution += 1
            elif safety_level == 'niebezpiecznie':
                counter_dangerous += 1

        self.result_text.insert(tk.END, "📋 PODSUMOWANIE:\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        self.result_text.insert(tk.END, f"🟢 Bezpiecznie: " + str(counter_safe) + " szczytów\n\n")
        self.result_text.insert(tk.END, f"🟡 Ostrożnie: " + str(counter_caution) + " szczytów\n\n")
        self.result_text.insert(tk.END, f"🔴 Niebezpiecznie: " + str(counter_dangerous) + " szczytów\n\n")

        self.result_text.insert(tk.END, "🏔️ SZCZYTY:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")

        for result in results:
            name = result['name']
            temperature = result['tempreature']
            wind = result['wind']
            level = result['bezpieczenstwo']

            bezpieczenstwo = result['bezpieczenstwo']
            if isinstance(bezpieczenstwo, dict):
                level = bezpieczenstwo.get('poziom', 'bezpiecznie')
            else:
                level = bezpieczenstwo

            if level == 'bezpiecznie':
                icon = "✅"
            elif level == 'ostroznie':
                icon = "⚠️"
            else:
                icon = "🚨"

            temp_float = float(temperature)
            wind_float = float(wind)

            line = f"{icon} {name:25} | {temperature:5.1f}°C | {wind:5.1f} m/s | {level}"
            self.result_text.insert(tk.END, line + "\n")

        all_numbers_off_peaks = len(self.weather_app.peaks_db)
        self.result_text.insert(tk.END, "\n\n")
        self.result_text.insert(tk.END, f"✅ Pobrano dane dla {len(results)} z {all_numbers_off_peaks} szczytów\n")




