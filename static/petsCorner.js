// JavaScript to handle slideshow transition
let slideIndex = 0;
const slides = document.querySelectorAll('.slide');

setInterval(() => {
    slides[slideIndex].classList.remove('active');
    slideIndex = (slideIndex + 1) % slides.length;
    slides[slideIndex].classList.add('active');
}, 3000); // Change slide every 3 seconds

