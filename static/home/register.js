let button = document.querySelector('button');
let alertDisplay = document.querySelector('.alert');
button.addEventListener('click', () => {
    let timeId = setTimeout(() => alertDisplay.style.display = "flex", 400);
    setTimeout(() => alertDisplay.style.display = "none", 3000);
})