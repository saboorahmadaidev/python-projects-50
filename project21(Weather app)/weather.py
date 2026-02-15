from tkinter import *
from tkinter import ttk, messagebox
import requests

# 🔐 PUT YOUR NEW API KEY HERE
API_KEY = "YOUR_API_KEY_HERE"


def get_weather():
    city = city_combo.get().strip()

    if not city:
        messagebox.showerror("Error", "Please select a city!")
        return

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            messagebox.showerror("API Error", f"Error Code: {response.status_code}")
            return

        data = response.json()

        if str(data.get("cod")) != "200":
            messagebox.showerror("API Error", data.get("message", "Unknown error"))
            return

        
        weather_main = data["weather"][0]["main"]
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

      
        climate_value.config(text=weather_main)
        description_value.config(text=weather_desc.capitalize())
        temp_value.config(text=f"{temp} °C")
        pressure_value.config(text=f"{pressure} hPa")
        humidity_value.config(text=f"{humidity} %")
        wind_value.config(text=f"{wind_speed} m/s")

    except requests.exceptions.Timeout:
        messagebox.showerror("Error", "Request timed out. Try again.")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "No internet connection.")

    except Exception as e:
        messagebox.showerror("Error", "Something went wrong.")


# ---------------- GUI ---------------- #

win = Tk()
win.title("Weather App")
win.geometry("450x400")
win.configure(bg="#e3f2fd")
win.resizable(False, False)

title = Label(
    win,
    text="Weather Application",
    font=("Segoe UI", 20, "bold"),
    bg="#e3f2fd",
)
title.pack(pady=15)


top_frame = Frame(win, bg="#e3f2fd")
top_frame.pack(pady=10)

Label(
    top_frame,
    text="Select City:",
    font=("Segoe UI", 12),
    bg="#e3f2fd"
).grid(row=0, column=0, padx=5)

cities = [
    "Lahore", "Islamabad", "Karachi", "Peshawar", "Quetta",
    "Multan", "Sialkot", "Faisalabad", "Hyderabad",
    "Rawalpindi", "Sargodha", "Bahawalpur", "Sukkur",
    "Abbottabad", "Skardu", "Gilgit", "Chitral",
    "Swat", "Naran", "Murree"
]

city_combo = ttk.Combobox(
    top_frame,
    values=cities,
    font=("Segoe UI", 11),
    state="readonly",
    width=20
)
city_combo.grid(row=0, column=1, padx=5)

get_btn = Button(
    win,
    text="Get Weather",
    command=get_weather,
    bg="#1976D2",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=20
)
get_btn.pack(pady=15)

# Result Frame
result_frame = Frame(win, bg="white", bd=2, relief=RIDGE)
result_frame.pack(pady=10, padx=20, fill="both", expand=True)


def create_row(text, row):
    Label(
        result_frame,
        text=text,
        font=("Segoe UI", 11, "bold"),
        bg="white"
    ).grid(row=row, column=0, sticky="w", padx=15, pady=8)

    value = Label(
        result_frame,
        text="--",
        font=("Segoe UI", 11),
        bg="white"
    )
    value.grid(row=row, column=1, sticky="e", padx=15, pady=8)

    return value


climate_value = create_row("Climate:", 0)
description_value = create_row("Description:", 1)
temp_value = create_row("Temperature:", 2)
pressure_value = create_row("Pressure:", 3)
humidity_value = create_row("Humidity:", 4)
wind_value = create_row("Wind Speed:", 5)

win.mainloop()
