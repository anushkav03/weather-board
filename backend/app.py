from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Get API keys
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

# Make API call to weather & set up endpoint
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Make API call
    weather_api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=${city}&aqi=no"
    response = requests.get(weather_api_url)

    if response.status_code == 200:
        weather_data = response.json()
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code
    
    
if __name__ == '__main__':
    app.run(debug=True)
