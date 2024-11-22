// ======== VARIABLES & DOM ELEMENTS ======== //
let weatherData = null

const rawInput = document.querySelector('.input')
const paraContainer = document.querySelector('.search-box')

const weatherText = document.querySelector('.weather-text')
const weatherImg = document.querySelector('.weather-img')

const timezoneText = document.querySelector('.timezone-text')
const cityText = document.querySelector('.city-text')

const tempBox = document.querySelector('.temperature');
const tempText = document.querySelector('.temperature-text')
const tempIcon = document.querySelector('.thermometer-icon');

const playlistButton = document.querySelector('.playlistButton')
const playlistEmbed = document.getElementById('spotify-embed');

const search = document.querySelector('.search');


// ======== API CALL TO BACKEND ======== //
function updateWeatherData(city) {
    const apiWeatherURL = `/weather?city=${city}`

    fetch(apiWeatherURL)
        .then(response => {
            if (!response.ok) {
                alert('Try entering a valid city name.')
            }
            return response.json();
        })
        .then(data => {
            weatherData = data;

            // Update all divs
            updateWeather();
            updateTimezone();
            updateTemperature();            
        })
}


// ======== UI UPDATE FUNCTIONS ======== //

// Update weather div
function updateWeather() {
    weatherText.textContent = weatherData.current.condition.text;
    weatherImg.src = `https:${weatherData.current.condition.icon}`;
}

// Update timezone and city div
function updateTimezone() {
    cityText.textContent = weatherData.location.localtime
    timezoneText.textContent = weatherData.location.name + ", " + weatherData.location.region + ", " + weatherData.location.country;

}

// Update temperature div & temperature icon (cold, normal, hot)
function updateTemperature() {
    if (weatherData.location.country == "United States of America") {
        tempText.textContent = weatherData.current.temp_f.toString() + "°F"
    } else {
        tempText.textContent = weatherData.current.temp_c.toString() + "°C"
    }
    updateTemperatureIcon();
}

function updateTemperatureIcon() {
    tempIcon.classList.remove('bi-thermometer', 'bi-thermometer-low', 'bi-thermometer-half', 'bi-thermometer-high');
    let temp = weatherData.current.temp_c;

    if (temp < 15) {
        tempIcon.classList.add('bi-thermometer-low');
        tempIcon.style.color = "blue";
    }
    else if (temp >= 15 && temp < 25) {
        tempIcon.classList.add('bi-thermometer-half');
        tempIcon.style.color = "green";
    }
    else if (temp >= 25 && temp < 35) {
        tempIcon.classList.add('bi-thermometer-high');
        tempIcon.style.color = "orange";
    }
    else {
        tempIcon.classList.add('bi-thermometer-high');
        tempIcon.style.color = "red";
    }
}

function updateTemperatureUnit() {
    if (tempText.textContent[tempText.textContent.length - 1] == "C") {
        tempText.textContent = weatherData.current.temp_f + "°F"
    } else {
        tempText.textContent = weatherData.current.temp_c + "°C"
    }
}

// // User auth
// function userAuth(){
//     fetch('login')
//         .then(response => response.json())
//         .then(data => {
//             // Redirect user to returned Spotify authorization URL
//             window.location.href = data.auth_url;
//         })
//         .catch(error => console.error('Error:', error));
// }

// Show Spotify playlist embed
function getPlaylist() {
    currWeather = "sunny"
    fetch(`playlist?weather=${currWeather}`)
        .then(response => response.text()
        .then(oembed_html => {
            playlistEmbed.innerHTML = oembed_html;
        }))

    // let playlistURL = "https://open.spotify.com/embed/playlist/37i9dQZF1EIeBPeLAL3kZc?utm_source=oembed";
    // playlistEmbed.innerHTML = `<iframe style="border-radius: 12px" width="100%" height="352" title="Spotify Embed: Rainy Day Morning Mix"
    //         frameborder="0" allowfullscreen allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
    //         loading="lazy" src=${playlistURL}>
    // </iframe>`;
}


// ======== EVENT LISTENERS ======== //

// User entering city
rawInput.addEventListener('keydown', function(event) {
    if ((event.key ) == 'Enter')  {
        const input = rawInput.value.trim();
        if (input != "") {
            // call weather function
            updateWeatherData(input);
        }
    }
})

// User changing temperature units
tempBox.addEventListener("click", function() {
    updateTemperatureUnit(); 
});

// Default page when window loads; for now, Berkeley CA
window.onload = updateWeatherData("Berkeley")

// User clicking "get playlist" button
playlistButton.addEventListener("click", function() {
    getPlaylist(); 
});

// ======== other stuff ======== //