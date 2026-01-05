import tkinter as tk
from tkinter import ttk

from PIL.ImageOps import expand
from bokeh.colors.named import lightblue
from click import style
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
        header_frame = tk.Frame(self.root, bg=lightblue)
        header_frame.pack(fill="x", pady=10)

        title_label = tk.Label(
            header_frame,
            text="🌄 APLIKACJA POGODOWA DLA TATR 🌄",
            font=("Arial", 20, "bold"),
            bg="#e6f2ff"
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
            bg="#add8e6"
        )
        main_frame.pack(
            pady=20,
            padx=20,
            fill="both",
            expand=True
        )




