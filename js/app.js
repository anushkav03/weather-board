// VARIABLES & DOM ELEMENTS
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

const search = document.querySelector('.search');



// FUNCTIONS
function getWeatherData(city) {
    const apiKey = "47c2a0b267bb49e6949222002240510"
    const apiURL = `http://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${city}&aqi=no`

    fetch(apiURL)
        .then(response => {
            if (!response.ok) {
                alert('Try entering a valid city name.')
            }
            return response.json();
        })
        .then(data => {
            weatherData = data;
            // Update Weather div
            weatherText.textContent = weatherData.current.condition.text;
            weatherImg.src = `https:${weatherData.current.condition.icon}`;

            // Update Timezone and City div
            cityText.textContent = weatherData.location.localtime
            timezoneText.textContent = weatherData.location.name + ", " + weatherData.location.region + ", " + weatherData.location.country;

            // Update Temperature div
            if (weatherData.location.country == "United States of America") {
                tempText.textContent = weatherData.current.temp_f.toString() + "°F"
            } else {
                tempText.textContent = weatherData.current.temp_c.toString() + "°C"
            }
            changeTemperatureIcon();
        })
}

// !! Separate API call & getting data from updating the UI

// Change temperature icon (cold, normal, hot)
function changeTemperatureIcon() {
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
        tempIcon.style.color = "yellow";
    }
    else {
        tempIcon.classList.add('bi-thermometer-high');
        tempIcon.style.color = "red";
    }
}

function changeTemperature() {
    if (tempText.textContent[tempText.textContent.length - 1] == "C") {
        tempText.textContent = weatherData.current.temp_f + "°F"
    } else {
        tempText.textContent = weatherData.current.temp_c + "°C"
    }
}





// EVENT LISTENERS

// User entering city
rawInput.addEventListener('keydown', function(event) {
    if ((event.key ) == 'Enter')  {
        const input = rawInput.value.trim();
        if (input != "") {
            // call weather function
            getWeatherData(input);
        }
    }
})

// User changing temperature units
tempBox.addEventListener("click", function() {
    changeTemperature(); 
});