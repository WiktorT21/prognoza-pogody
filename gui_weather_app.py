import tkinter as tk
from tkinter import ttk, Toplevel, messagebox

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
            lon = peak_info['lon']
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

    def show_forecast(self):
        dialog = Toplevel(self.root)
        dialog.title("📅 Prognoza na 5 dni")
        dialog.geometry("400x500")
        dialog.configure(bg="#f0f8ff")

        label = ttk.Label(
            dialog,
            text = "Wybierz szczyt do prognozy: ",
            style = 'Header.TLabel'
        )
        label.pack(pady=20)

        listbox_frame = tk.Frame(dialog, bg="#f0f8ff")
        listbox_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(listbox_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 11),
            bg="white",
            fg="black",
            selectbackground="#3498db",
            selectforeground="white",
            height=12
        )
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)

        list_of_peaks = list(self.weather_app.peaks_db.keys())
        list_of_peaks.sort()

        for i, peak_name in enumerate(list_of_peaks, 1):
            listbox.insert(tk.END, f"{i:2}. {peak_name}")

        def on_select():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Uwaga", "Wybierz szczyt z listy")
                return

            index = selection[0]
            selected_peak = list_of_peaks[index]
            dialog.destroy()
            self.display_forecast(selected_peak)

        button_frame = tk.Frame(dialog, bg="#f0f8ff")
        button_frame.pack(pady=20)

        select_btn = ttk.Button(
            button_frame,
            text="✅ Pokaż prognozę",
            command=on_select,
            style='Green.TButton'
        )
        select_btn.pack(side='left', padx=10)

        cancel_btn = ttk.Button(
            button_frame,
            text="❌ Anuluj",
            command=dialog.destroy,
            style='Red.TButton'
        )
        cancel_btn.pack(side='left', padx=10)

    def display_forecast(self, peak_name):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"\n⌛ Pobieram dane dla {peak_name}...\n")
        self.root.update()

        peak_info = self.weather_app.peaks_db.get(peak_name)

        if not peak_info:
            messagebox.showerror("Błąd", f" ❌ Nie znaleziono szczytu: {peak_name}")
            return

        raw_forecast_data = self.weather_app.fetcher.fetch_forecast(
            lat=peak_info['lat'],
            lon=peak_info['lon']
        )

        if not raw_forecast_data:
            messagebox.showerror("Błąd", " ❌ Nie udało się pobrać prognozy pogody")
            return

        processed_forecast_data = self.weather_app.processor.process_forecast_data(raw_forecast_data, peak_info)

        if not processed_forecast_data:
            messagebox.showerror("Błąd", " ❌ Nie udało się przetworzyć prognozy")
            return

        self.result_text.delete("1.0", tk.END)
        self.display_forecast_data(processed_forecast_data)

    def display_forecast_data(self, data):
        self.clear_screen()

        self.result_text.insert(tk.END, "⛰️" * 20 + "\n")
        self.result_text.insert(tk.END, f"📅 PROGNOZA POGODY DLA: {data['peak_name'].upper()}\n")
        self.result_text.insert(tk.END, f"📍 Wysokość: {data['elevation']} m n.p.m.\n")
        self.result_text.insert(tk.END, f"📊 Liczba prognoz: {data['forecast_count']}\n")
        self.result_text.insert(tk.END, f"⏰ Zakres: {data['date_range']}\n")
        self.result_text.insert(tk.END, "⛰️" * 20 + "\n\n")

        forecast_by_day = {}

        for forecast in data['forecasts']:
            forecast_date = forecast['date']

            if forecast_date not in forecast_by_day:
                forecast_by_day[forecast_date] = []

            forecast_by_day[forecast_date].append(forecast)

        self.result_text.insert(tk.END,"📅 PODSUMOWANIE DZIENNE:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")

        for date in sorted(forecast_by_day.keys()):
            day_forecast = forecast_by_day[date]

            temperature_list = []
            wind_list = []
            safety_list = []
            description_list = []

            for forecast in day_forecast:
                temperature = forecast.get('temperature_peak') or forecast.get('temperature peak') or 0
                temperature_list.append(float(temperature))

                wind = forecast.get('wind', 0)
                wind_list.append(float(wind))

                safety = forecast.get('safety', {})
                if isinstance(safety, dict):
                    safety_level = safety.get('poziom', 'bezpiecznie')
                else:
                    safety_level = str(safety)
                safety_list.append(safety_level)

                description = forecast.get('description', '')
                description_list.append(description)

            if temperature_list:
                min_temp = min(temperature_list)
                max_temp = max(temperature_list)
            else:
                min_temp = 0
                max_temp = 0

            if wind_list:
                max_wind = max(wind_list)
            else:
                max_wind = 0

            if 'niebezpiecznie' in safety_list:
                worst_level = 'niebezpiecznie'
                emoji = "🔴"
            elif 'ostroznie' in safety_list:
                worst_level = 'ostroznie'
                emoji = "🟡"
            else:
                worst_level = 'bezpiecznie'
                emoji = "🟢"

            most_common = ""
            if description_list:
                non_empty = [d for d in description_list if d]
                if non_empty:
                    most_common = max(set(non_empty), key=non_empty.count)

            self.result_text.insert(tk.END, f"\n{emoji} 📅 {date}:\n")
            self.result_text.insert(tk.END, f"   🌡️  Temperatura: {min_temp:.1f}°C → {max_temp:.1f}°C\n")
            self.result_text.insert(tk.END, f"   💨 Maks. wiatr: {max_wind:.1f} m/s\n")
            self.result_text.insert(tk.END, f"   🛡️  Bezpieczeństwo: {worst_level.upper()}\n")


            if most_common:
                self.result_text.insert(tk.END, f"   ⛅ Główne warunki: {most_common}\n")

            self.result_text.insert(tk.END, f"   📊 Prognoz w dniu: {len(day_forecast)}\n")
            self.result_text.insert(tk.END, "   " + "-" * 40 + "\n")

            days_count = len(forecast_by_day)
            self.result_text.insert(tk.END, "\n" + "-" * 50 + "\n")
            self.result_text.insert(tk.END, f"✅ Wyświetlono prognozę na {days_count} dni\n")

    def clear_display(self):
        self.result_text.delete("1.0", tk.END)

    def exit_app(self):
        response = messagebox.askyesno(
            "Potwierdzenie wyjścia",
            "Czy na pewno chcesz zamknąć aplikację pogodową?",
            icon='question'
        )

        if response:
            self.root.destroy()
            print("Aplikacja zamknięta. Do zobaczenia! 🏔️")
















