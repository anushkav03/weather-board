from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask import render_template

# Get API keys
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

# Routes
@app.route('/weather', methods=['GET'])
def get_weather(city=None):
    if city is None:
        city = request.args.get('city')
    if not city:
        return jsonify({"error": "Try entering a valid city name."}), 400

    # Make API call
    weather_api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(weather_api_url)

    if response.status_code == 200:
        weather_data = response.json()
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
