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
            // update
            const weather = document.querySelector('.weather-text')
            const timezone = document.querySelector('.timezone-text')

            weather.textContent = data.location.name + ", " + data.location.region + ", " + data.location.country
            timezone.textContent = data.current.condition.text
        })
}

// DOM ELEMENTS



const search = document.querySelector('.search');

const temp = document.querySelector('.temperature');
temp.addEventListener("click", function() {
    alert('well oo man the way they turn cold');
});

const rawInput = document.querySelector('.input')
const paraContainer = document.querySelector('.search-box')
rawInput.addEventListener('keydown', function(event) {
    if ((event.key ) == 'Enter')  {
        const input = rawInput.value.trim();
        if (input != "") {
            // call weather function
            getWeatherData(input)
        }
    }
})