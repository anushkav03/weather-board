const search = document.querySelector('.search');

const temp = document.querySelector('.temperature');
temp.addEventListener("click", function() {
    alert('well oo man the way they turn cold');
});

const input = document.querySelector('.input-copy-from')
const paragraph = document.querySelector('.input-copy-to')
const paraContainer = document.querySelector('.search')
input.addEventListener('change', function() {
    paragraph.textContent = input.value;
})