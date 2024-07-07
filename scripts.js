document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll('.image-container');
    let touchstartX = 0;
    let touchendX = 0;
    let currentSlideIndex = 0;
    
    const gallery = document.querySelector('.image-gallery');
    gallery.addEventListener('touchstart', e => {
        touchstartX = e.changedTouches[0].screenX;
    });
    
    gallery.addEventListener('touchend', e => {
        touchendX = e.changedTouches[0].screenX;
        handleGesture();
    });
    
    function handleGesture() {
        const totalSlides = slides.length;
        if (touchendX + 100 < touchstartX) {
            currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
        } else if (touchendX - 100 > touchstartX) {
            currentSlideIndex = (currentSlideIndex - 1 + totalSlides) % totalSlides;
        }
        showSlide(currentSlideIndex);
    }
    
    // Function to show a specific slide
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.display = i === index ? 'block' : 'none';
        });
    }

    // Initially show the first slide
    showSlide(0);
});
