Weather Forecast CLI App
A simple Python command-line tool to fetch and display the current weather and a 3-day forecast for any city using the OpenWeatherMap API. The app supports temperature unit selection (Celsius/Fahrenheit), clear tabular output, ASCII art for weather conditions, and robust error handling.

Features
🌤️ Fetches current weather data (temperature, humidity, wind, condition)

📅 Displays a 3-day weather forecast in a clean table

🏙️ Supports any global city

🌡️ Choose between Celsius and Fahrenheit

🎨 Shows ASCII art for weather conditions (e.g., sun, rain, clouds)

🛡️ Handles errors & invalid user input gracefully

🛠️ Modular code, easy to extend

Demo
![CLI Demo Animation with your own image or GIF*</sup>

Usage Example
shell
python weather_cli.py

Enter city name: Hyderabad
Temperature unit options:
 [1] Celsius
 [2] Fahrenheit
Choose (1 or 2) [default 1]: 1
Output includes a current weather summary, ASCII art, and a neat table with the 3-day forecast.

Installation
Clone the Repository

text
git clone https://github.com/yourusername/WeatherApp.git
cd WeatherApp
Install Required Packages

bash
pip install requests tabulate
Get Your API Key

Sign up at OpenWeatherMap

Copy your API key

Configuration
Important: For best security, do not hard-code your API key!

Set your API key as an environment variable:

Linux/Mac

bash
export OPENWEATHER_API_KEY=your_api_key_here
Windows

text
set OPENWEATHER_API_KEY=your_api_key_here
The script will read this variable at runtime.

Alternatively, you can update the script to read your key from a config file (ensure .gitignore excludes it).

How to Run
bash
python weather_cli.py
Follow the prompts to enter a city and select the temperature unit.

Dependencies
Library	Purpose
requests	HTTP requests to OpenWeatherMap API
tabulate	Tabular display of forecast (optional)
datetime	Date/time formatting
json	Parsing API responses
Error Handling
Invalid city names prompt for correct input.

Handles network/API errors gracefully.

Missing API key produces a prompt and exits cleanly.

Customization Ideas
Add colored output using colorama

Extend to weekly forecast

Accept city name and units as command line arguments

Internationalization via OpenWeatherMap lang parameter

License
MIT License

API Reference
Powered by OpenWeatherMap

Contributing
Pull requests and suggestions are welcome! Please open an issue to discuss before major changes.

Disclaimer
Do not commit your API keys to the repository. If you accidentally do, revoke them immediately and follow security best practices.

Enjoy your weather, right from the terminal! 😊
