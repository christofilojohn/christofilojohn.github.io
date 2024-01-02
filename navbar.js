// Function to load the navbar
document.addEventListener("DOMContentLoaded", function() {
    currentSlide(1);
    var navbarPlaceholder = document.getElementById('navbar-placeholder');
    if (navbarPlaceholder) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'navbar.html', true);
        xhr.onreadystatechange = function() {
            if (this.readyState !== 4) return;
            if (this.status !== 200) return; // Handle error
            navbarPlaceholder.innerHTML = this.responseText;
        };
        xhr.send();
    }
});


function currentSlide(n) {
    var i;
    var slides = document.getElementsByClassName("image-container");
    var dots = document.getElementsByClassName("dot");

    if (n > slides.length) { n = 1; }
    if (n < 1) { n = slides.length; }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    slides[n - 1].style.display = "block"; // Changed from flex to block
    dots[n - 1].className += " active";
}

