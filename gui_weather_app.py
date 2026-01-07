import tkinter as tk
from tkinter import ttk

from PIL.ImageOps import expand
from bokeh.colors.named import lightblue
from click import style
from docutils.nodes import footer
from qtconsole.mainwindow import background


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


