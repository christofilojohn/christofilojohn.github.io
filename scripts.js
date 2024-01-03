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

document.addEventListener("DOMContentLoaded", function() {
    currentSlide(1);
    let touchstartX = 0;
    let touchendX = 0;

    let currentSlideIndex = 1; // Start with the first slide
    const totalSlides = document.querySelectorAll('.image-container').length;

    function currentSlide(n) {
        // Existing logic to show the slide based on index n
        // Update the currentSlideIndex after showing the slide
        currentSlideIndex = n;
        // ... rest of your currentSlide function ...
    }

    function handleGesture() {
        if (touchendX + 100 < touchstartX) {
            nextSlide();
        }
        
        if (touchendX - 100 > touchstartX) {
            previousSlide();
        }
    }

    function nextSlide() {
        let nextIndex = currentSlideIndex + 1;
        if (nextIndex > totalSlides) nextIndex = 1; // Loop back to the first slide
        currentSlide(nextIndex);
    }

    function previousSlide() {
        let prevIndex = currentSlideIndex - 1;
        if (prevIndex < 1) prevIndex = totalSlides; // Loop back to the last slide
        currentSlide(prevIndex);
    }

    const gallery = document.querySelector('.image-gallery');
    gallery.addEventListener('touchstart', e => {
        touchstartX = e.changedTouches[0].screenX;
    });

    gallery.addEventListener('touchend', e => {
        touchendX = e.changedTouches[0].screenX;
        handleGesture();
    });

    currentSlide(currentSlideIndex); // Initialize the first slide
});
