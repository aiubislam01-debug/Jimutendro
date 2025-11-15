from tkinter import *
from datetime import datetime
import requests
import pytz

    


def get_hourly_data(lat, lon):

    forecast = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weathercode&timezone=auto")
    
    data = requests.get(forecast).json()
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    codes = data["hourly"]["weathercode"]
    timezone_name = data["timezone"]

    tz = pytz.timezone(timezone_name)
    current_time = datetime.now(tz)

    min_diff = float("inf")
    index = 0
    for i, t in enumerate(times):
        dt = datetime.fromisoformat(t)

        dt = tz.localize(dt) if dt.tzinfo is None else dt
        diff = abs((dt - current_time).total_seconds())
        if diff < min_diff:
            min_diff = diff
            index = i

    hourly = []
    for i in range(index, index + 24):

        temp = round(temps[i], 1)
        dt = datetime.fromisoformat(times[i])
        time_str = dt.strftime("%I %p")
        condition = weather_code_to_text(codes[i])
        hourly.append((time_str, temp, condition, codes[i]))

    return hourly


def weather_code_to_text(code):
    
    mapping = {
        0: "Clear",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime Fog",
        51: "Light Drizzle",
        53: "Drizzle",
        55: "Heavy Drizzle",
        61: "Light Rain",
        63: "Rain",
        65: "Heavy Rain",
        71: "Light Snow",
        73: "Snow",
        75: "Heavy Snow",
        80: "Showers",
        81: "Rain Showers",
        82: "Heavy Showers",
        95: "Thunderstorm",
        96: "Thunder + Light Hail",
        99: "Thunder + Heavy Hail"
    }
    return mapping.get(code, "Unknown")




def show_hourly_forecast(root, hourly_data, x=0, y=0, width=900, height=150):


    a = Frame(root, bg=root.cget("bg"))
    a.place(x=x, y=y, width=width, height=height)
    

    c = Canvas(a, bg=root.cget("bg"))
    x = Scrollbar(a, orient=HORIZONTAL, command=c.xview)
    c.configure(xscrollcommand=x.set)
    x.pack(side=BOTTOM, fill=X)
    c.pack(fill="both", expand=True)

    b = Frame(c, bg=root.cget("bg"))
    c.create_window((0,0),window=b,anchor = 'nw')

    def update_scroll(event):
        c.configure(scrollregion=c.bbox("all"))
    b.bind("<Configure>", update_scroll)

    for time_str, temp, des, code in hourly_data:
        blck1 = Frame(b, bg="#f8f8f8", width=100, height=120)
        blck1.pack(side=LEFT, padx=5, pady=10)

        lbl1 = Label(blck1, text=time_str, fg="#333", bg="#f8f8f8",
              font=("Segoe UI", 9, "bold"))
        lbl1.pack(pady=(5, 0))

        lbl2 =Label(blck1, text=f"{temp}°C", fg="#0078d7", bg="#f8f8f8",
              font=("Segoe UI", 11, "bold"))
        lbl2.pack()

        lbl3 = Label(blck1, text=des, fg="#555", bg="#f8f8f8",
              font=("Segoe UI", 9))
        lbl3.pack(pady=(0, 5))




lat = 23
lon = 90
hourly_data = get_hourly_data(lat,lon)

