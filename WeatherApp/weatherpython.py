import requests
from datetime import datetime, timedelta
import sys

try:
    from tabulate import tabulate
    USE_TABULATE = True
except ImportError:
    USE_TABULATE = False

# Map simple weather text to ASCII art
ASCII_ART = {
    "clear": "   \\   /   \n    .-.    \n ― (   ) ― \n    `-’    \n   /   \\   ",
    "clouds": "     .--.   \n  .-(    ).\n (___.__)__)",
    "rain": "     .--.   \n  .-(    ).\n (___.__)__) \n  ʻ ʻ ʻ ʻ ",
    "drizzle": "     .--.   \n  .-(    ).\n (___.__)__) \n  ʻ ʻ ʻ ʻ ",
    "thunderstorm": "     .--.   \n  .-(    ).\n (___.__)__) \n  ⚡⚡⚡⚡",
    "snow": "     .--.   \n  .-(    ).\n (___.__)__) \n   * * * *",
    "mist": " _ - _ - _ - ",
    "fog": " _ - _ - _ - ",
    "haze": " _ - _ - _ - ",
    "smoke": "     (    )\n    (____)",
}

API_KEY = "877f43ec18d0ef4537db87aeaabb1f42"

def get_user_input():
    """Get city name and temperature unit from user."""
    city = input("Enter city name: ").strip()
    while not city:
        print("City name cannot be empty.")
        city = input("Enter city name: ").strip()

    print("Temperature unit options:")
    print(" [1] Celsius")
    print(" [2] Fahrenheit")
    unit_choice = input("Choose (1 or 2) [default 1]: ").strip()
    if unit_choice == "2":
        units = "imperial"
        degree_sym = "°F"
    else:
        units = "metric"
        degree_sym = "°C"

    return city, units, degree_sym

def fetch_weather(api_url, params):
    """Generic function to fetch data from OpenWeather API."""
    try:
        response = requests.get(api_url, params=params, timeout=10)
    except requests.RequestException as e:
        print(f"Error: Could not connect to the weather service ({e})")
        sys.exit(1)
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.json().get('message', '')}")
        sys.exit(1)
    return response.json()

def ascii_art_for(condition):
    """Return appropriate ASCII art for weather condition."""
    for key in ASCII_ART:
        if key in condition.lower():
            return ASCII_ART[key]
    return ""

def display_current_weather(data, degree_sym):
    """Print current weather nicely formatted."""
    condition = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    city_name = data.get('name', 'Unknown location')
    ascii_img = ascii_art_for(data["weather"][0]["main"])

    print("\n=== Current Weather ===")
    print(f"Location: {city_name}")
    if ascii_img:
        print(ascii_img)
    print(f"Condition: {condition}")
    print(f"Temperature: {temp} {degree_sym}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind} m/s\n")

def pick_daily_forecast(forecast_list, timezone_shift_s):
    """Get 3 upcoming day forecasts (pref. at 12:00 local time), else nearest."""
    today = datetime.utcfromtimestamp(forecast_list[0]['dt']) + timedelta(seconds=timezone_shift_s)
    forecasts = {}
    for entry in forecast_list:
        time = datetime.utcfromtimestamp(entry['dt']) + timedelta(seconds=timezone_shift_s)
        date_str = time.strftime("%Y-%m-%d")
        hour = time.hour
        # Pick times closest to midday (12:00)
        if date_str not in forecasts:
            forecasts[date_str] = (abs(hour - 12), entry)
        else:
            prev_diff, _ = forecasts[date_str]
            if abs(hour - 12) < prev_diff:
                forecasts[date_str] = (abs(hour - 12), entry)
    # Skip today, pick next 3 days
    sorted_dates = sorted(set(forecasts.keys()))
    today_str = today.strftime("%Y-%m-%d")
    next_days = [d for d in sorted_dates if d > today_str][:3]
    return [forecasts[date][1] for date in next_days]

def display_forecast(forecast_entries, degree_sym):
    """Show 3 day forecast in table."""
    table = []
    for entry in forecast_entries:
        dt = datetime.utcfromtimestamp(entry['dt'])
        date = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M")
        temp = entry["main"]["temp"]
        condition = entry["weather"][0]["description"].title()
        table.append([date, temp, condition])
    headers = ["Date", f"Temp {degree_sym}", "Condition"]
    print("=== 3-Day Forecast ===")
    if USE_TABULATE:
        print(tabulate(table, headers, tablefmt="github"))
    else:
        print("{:12} {:10} {}".format(*headers))
        for row in table:
            print("{:12} {:10} {}".format(*row))
    print()

def main():
    print("\n=== Weather Forecast CLI ===")
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Please obtain your OpenWeatherMap API key and set it in the script.")
        sys.exit(1)

    city, units, degree_sym = get_user_input()

    # Fetch current weather
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": units}
    weather_data = fetch_weather(weather_url, params)

    # Fetch 5-day/3-hour forecast
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    forecast_data = fetch_weather(forecast_url, params)

    # Display
    display_current_weather(weather_data, degree_sym)
    timezone_shift = weather_data.get("timezone", 0)  # seconds
    forecast_entries = pick_daily_forecast(forecast_data["list"], timezone_shift)
    display_forecast(forecast_entries, degree_sym)

    print("✨ Done! Have a great day.\n")

if __name__ == "__main__":
    main()
