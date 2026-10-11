import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Czyste niebo",
    1: "Przeważnie pogoda słoneczna",
    2: "Częściowo pochmurno",
    3: "Pochmurno",
    45: "Mgła",
    48: "Mgła z osadem",
    51: "Lekkie mżawka",
    53: "Umiarkowana mżawka",
    55: "Gęsta mżawka",
    56: "Lodowata mżawka",
    57: "Gęsta lodowata mżawka",
    61: "Lekkie opady deszczu",
    63: "Umiarkowane opady deszczu",
    65: "Intensywne opady deszczu",
    66: "Lekkie marznące opady",
    67: "Silne marznące opady",
    71: "Lekkie opady śniegu",
    73: "Umiarkowane opady śniegu",
    75: "Intensywne opady śniegu",
    77: "Śnieg ziarnisty",
    80: "Lekkie przelotne opady",
    81: "Umiarkowane opady",
    82: "Silne opady",
    85: "Lekkie opady śniegu",
    86: "Silne opady śniegu",
    95: "Burza",
    96: "Burza z gradem",
    99: "Silna burza z gradem",
}

WEATHER_ICONS = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    53: "🌦️",
    55: "🌧️",
    56: "🌧️",
    57: "🌧️",
    61: "🌧️",
    63: "🌧️",
    65: "🌧️",
    66: "🌧️",
    67: "🌧️",
    71: "🌨️",
    73: "🌨️",
    75: "🌨️",
    77: "🌨️",
    80: "🌦️",
    81: "🌧️",
    82: "🌧️",
    85: "🌨️",
    86: "🌨️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️",
}


def geocode_city(city_name: str):
    params = {
        "name": city_name,
        "count": 1,
        "language": "pl",
        "format": "json",
    }
    response = requests.get(GEOCODE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        raise ValueError("Nie znaleziono miejscowości.")

    place = results[0]
    return {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "name": place.get("name", city_name),
        "country": place.get("country", ""),
        "admin1": place.get("admin1", ""),
    }


def fetch_weather(city_name: str):
    place = geocode_city(city_name)
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 7,
    }

    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})
    current_code = current.get("weather_code")

    result = {
        "city": place["name"],
        "country": place["country"],
        "admin1": place["admin1"],
        "weather_code": current_code,
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind": current.get("wind_speed_10m"),
        "weather": WEATHER_CODES.get(current_code, "Nieznany stan pogody"),
        "max_temp": daily.get("temperature_2m_max", [None] * 7)[0],
        "min_temp": daily.get("temperature_2m_min", [None] * 7)[0],
    }

    if daily.get("weather_code"):
        result["next_days"] = []
        date_values = daily.get("time", [])
        for index, (code, max_temp, min_temp) in enumerate(
            zip(
                daily.get("weather_code", []),
                daily.get("temperature_2m_max", []),
                daily.get("temperature_2m_min", []),
            )
        ):
            date_str = date_values[index] if index < len(date_values) else None
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_names = {
                    "Mon": "Pon",
                    "Tue": "Wto",
                    "Wed": "Śro",
                    "Thu": "Czw",
                    "Fri": "Pią",
                    "Sat": "Sob",
                    "Sun": "Ndz",
                }
                day_name = day_names.get(date_obj.strftime("%a"), date_obj.strftime("%a"))
            except (TypeError, ValueError):
                day_name = f"Dzień {index + 1}"

            result["next_days"].append(
                {
                    "day": index,
                    "date": day_name,
                    "code": code,
                    "condition": WEATHER_CODES.get(code, "Nieznany stan pogody"),
                    "max": max_temp,
                    "min": min_temp,
                }
            )
    else:
        result["next_days"] = []

    return result


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pogoda")
        self.geometry("520x560")
        self.minsize(480, 520)
        self.configure(bg="#f2f7ff")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f2f7ff")
        self.style.configure("TLabel", background="#f2f7ff", foreground="#1d2a39", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#103a66")
        self.style.configure("Value.TLabel", font=("Segoe UI", 12, "bold"), foreground="#0d3b66")
        self.style.configure("TEntry", padding=8)
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"))

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(main_frame, text="Sprawdź pogodę", style="Header.TLabel")
        title.pack(anchor="w", pady=(0, 12))

        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        self.city_entry = ttk.Entry(search_frame)
        self.city_entry.pack(side="left", fill="x", expand=True)
        self.city_entry.bind("<Return>", lambda event: self.search_weather())
        self.city_entry.insert(0, "Warszawa")

        search_btn = ttk.Button(search_frame, text="Szukaj", command=self.search_weather)
        search_btn.pack(side="left", padx=(10, 0))

        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill="both", expand=True)

        self.city_label = ttk.Label(self.result_frame, text="", style="Header.TLabel")
        self.city_label.pack(anchor="w", pady=(10, 5))

        self.temp_label = ttk.Label(self.result_frame, text="", style="Value.TLabel")
        self.temp_label.pack(anchor="w")

        current_weather_frame = ttk.Frame(self.result_frame)
        current_weather_frame.pack(anchor="w", pady=(8, 4))

        self.weather_icon = ttk.Label(current_weather_frame, text="", font=("Segoe UI", 28))
        self.weather_icon.pack(side="left")

        self.weather_label = ttk.Label(current_weather_frame, text="")
        self.weather_label.pack(side="left", padx=(10, 0))

        self.details_label = ttk.Label(self.result_frame, text="", justify="left")
        self.details_label.pack(anchor="w", pady=(0, 10))

        self.forecast_label = ttk.Label(self.result_frame, text="Prognoza na kolejne 7 dni:", font=("Segoe UI", 12, "bold"))
        self.forecast_label.pack(anchor="w", pady=(8, 6))

        self.forecast_text = tk.Text(self.result_frame, height=10, wrap="word", font=("Segoe UI", 10), bg="#ffffff")
        self.forecast_text.pack(fill="both", expand=True)
        self.forecast_text.config(state="disabled")

        self.search_weather()

    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Brak danych", "Wpisz nazwę miejscowości.")
            return

        try:
            data = fetch_weather(city)
            display_name = data["city"]
            if data["admin1"]:
                display_name += f", {data['admin1']}"
            if data["country"]:
                display_name += f", {data['country']}"

            current_code = data.get("weather_code")
            weather_name = data["weather"]
            weather_icon = WEATHER_ICONS.get(current_code, "❔")

            self.city_label.config(text=display_name)
            self.temp_label.config(text=f"{data['temperature']}°C")
            self.weather_icon.config(text=weather_icon)
            self.weather_label.config(text=f"Pogoda: {weather_name}")
            self.details_label.config(
                text=(
                    f"Wilgotność: {data['humidity']}%\n"
                    f"Wiatr: {data['wind']} km/h\n"
                    f"Max: {data['max_temp']}°C | Min: {data['min_temp']}°C"
                )
            )

            self.forecast_text.config(state="normal")
            self.forecast_text.delete("1.0", tk.END)
            if data["next_days"]:
                lines = []
                for item in data["next_days"]:
                    icon = WEATHER_ICONS.get(item.get("code"), "❔")
                    lines.append(
                        f"{icon} {item['date']} {item['day'] + 1}: {item['condition']} | Max {item['max']}°C | Min {item['min']}°C"
                    )
                self.forecast_text.insert(tk.END, "\n".join(lines))
            else:
                self.forecast_text.insert(tk.END, "Brak danych pogody na kolejne 7 dni.")
            self.forecast_text.config(state="disabled")

        except requests.RequestException as exc:
            messagebox.showerror("Błąd połączenia", f"Nie udało się pobrać pogody.\n{exc}")
        except ValueError as exc:
            messagebox.showerror("Brak danych", str(exc))


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
