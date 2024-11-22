import base64
from flask import Flask, redirect, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask import render_template
import urllib

# Get API keys
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

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


## Client Credentials auth flow; get access token > playlist ID > oembed html
@app.route('/playlist')
def getPlaylist():
    currWeather = request.args.get('currWeather', default="sunny")
    # Get weather keyword
    weather = getWeather(currWeather)

    # Get access token
    token = getAccessToken()

    # Use access token to get playlist ID
    playlistID = getPlaylistID(token, weather)

    # Use playlist ID to get OEmbed HTML
    oembed_html = getOEmbed(playlistID)

    #return render_template('playlist.html', oembed_html=oembed_html)
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
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        # Parse the JSON response; also has "Expires In" info
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    else:
        # Handle errors
        error_message = response.json().get("error_description", "Unknown error")
        return jsonify({"error": error_message}), response.status_code
    
def getPlaylistID(access_token, weather):
    WEBAPI_URL = "https://api.spotify.com/v1/search"

    params = {
        "q": weather,
        "type": "playlist",
        "limit": 1,
        "offset": 0
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(WEBAPI_URL, headers=headers, params=params)

    if response.status_code == 200:
        playlist_data = response.json()
        
        if playlist_data["playlists"]["items"]:
            playlistID = playlist_data["playlists"]["items"][0]["external_urls"]["spotify"]
            return playlistID
        else:
            return {"error": "No playlists found for the given query."}
    else:
        # Handle errors
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        return {"error": error_message}
    
def getOEmbed(playlistID):
    #OEMBED_URL = "https://open.spotify.com/oembed"
    response = requests.get(f"https://open.spotify.com/oembed?url={playlistID}")
    if response.status_code == 200:
        oembed_data = response.json() 
        return oembed_data["html"]


## User authentication process
# @app.route('/login', methods=['GET'])
# def login():
#     # Make API call: redirect user to Spotify login
#     params = {
#         'client_id': SPOTIFY_CLIENT_ID,
#         'response_type': 'code',
#         'redirect_uri': "https://weather-board-387v.onrender.com/callback",
#         #'scope': SCOPES,
#         'show_dialog': 'true',  # Optional: Set to 'true' to show the consent dialog each time
#         'state': 'some_random_string'  # Optional: Add a unique state to protect against CSRF
#     }

#     auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
#     return jsonify({'auth_url': auth_url})

# # Spotify redirect URI
# @app.route('/callback')
# def callback():
#     # Get the auth code from user's response
#     code = request.args.get('code')
#     if not code:
#         return jsonify({"error": "Authorization code not provided"}), 400
    
#     # Exchange it for access token by making API call to /api/token with POST
#     token_response = requests.post("https://accounts.spotify.com/api/token", 
#         data={
#             'grant_type': 'authorization_code',
#             'code': code,
#             'redirect_uri': "https://weather-board-387v.onrender.com/callback",
#             'client_id': SPOTIFY_CLIENT_ID,
#             'client_secret': SPOTIFY_CLIENT_SECRET
#         }
#     )
    
#     token_json = token_response.json()

#     # Check if the request was successful
#     if 'access_token' in token_json:
#         access_token = token_json['access_token']
#         refresh_token = token_json['refresh_token']
        
#         # Send the tokens to the frontend or store them as needed
#         return jsonify({
#             'access_token': access_token,
#             #'refresh_token': refresh_token # not doing refresh token right now
#         })
#     else:
#         return jsonify({"error": "Failed to retrieve access token"}), 400


## Development
if __name__ == '__main__':
    app.run(debug=True)


## Production
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
