import base64
from random import random
from flask import Flask, request, jsonify
import requests
from flask import render_template

import os
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

app = Flask(__name__)

## ROUTES

# Get weather data
@app.route('/weather', methods=['GET'])
def get_weather(city=None):
    if city is None:
        city = request.args.get('city')
    if not city:
        return jsonify({"error": "Try entering a valid city name."}), 400

    # Make API call to weatherapi
    weather_api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(weather_api_url)

    if response.status_code == 200:
        weather_data = response.json()
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code

# Home page renders index.html template   
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# Spotify's Client Credentials auth flow; get access token > playlist ID > oembed html
@app.route('/playlist')
def get_playlist_route():
    currWeather = request.args.get('currWeather', default="sunny")
    weather = getWeather(currWeather) # simplifying weather terms & mapping to a smaller set of terms
    token = getAccessToken()
    
    # returns either Spotify URL string or an error dict
    result = getPlaylistID(token, weather)

    # if dict then error
    if isinstance(result, dict):
        return result.get("error", "Error"), 400

    # else pass into oembed 
    oembed_html = getOEmbed(result)
    
    # and return resulting raw html
    return oembed_html

def getWeather(currWeather):
    description = currWeather.lower()
    if "rain" in description or "drizzle" in description or "shower" in description:
        return "rainy"
    elif "snow" in description or "sleet" in description or "ice pellets" in description:
        return "snow"
    elif "cloud" in description or "overcast" in description or "mist" in description or "fog" in description:
        return "cloudy"
    elif "sunny" in description or "clear" in description:
        return "sunny"
    else:
        # Default
        return "sunny"

def getAccessToken():
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    client_creds = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_creds_b64}",
        "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    else:
        # Handle errors
        error_message = response.json().get("error_description", "Unknown error")
        return jsonify({"error": error_message}), response.status_code
    
def getPlaylistID(access_token, weather):
    # type=track for individual tracks; change back to type=playlist for playlist
    params = {"q": weather, "type": "track"} 
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # api call to spotify search endpoint - to search by weather term
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("tracks", {}).get("items", [])
        
        if items:
            # pick a random track from the items returned
            import random
            track = random.choice(items) 
            return track["external_urls"]["spotify"]
            
    return {"error": "No tracks found"}
    
def getOEmbed(playlistID):
    #OEMBED_URL = "https://open.spotify.com/oembed"
    response = requests.get(f"https://open.spotify.com/oembed?url={playlistID}")
    if response.status_code == 200:
        oembed_data = response.json() 
        return oembed_data["html"]

## Development
if __name__ == '__main__':
    app.run(debug=True)


## Production
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
