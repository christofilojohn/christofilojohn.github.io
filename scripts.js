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

document.addEventListener('DOMContentLoaded', function() {
    const gallery = document.querySelector('.art-gallery');
    const fullscreenGallery = document.getElementById('fullscreen-gallery');
    const fullscreenImage = document.getElementById('fullscreen-image');
    const fullscreenTitle = document.getElementById('fullscreen-title');
    const fullscreenDescription = document.getElementById('fullscreen-description');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const closeButton = document.getElementById('close-button');

    let currentIndex = 0;
    const artItems = Array.from(document.querySelectorAll('.art-item'));

    function showFullscreen(index) {
        const item = artItems[index];
        const fullSizeImageSrc = item.dataset.src;
        const title = item.querySelector('h3').textContent;
        const description = item.querySelector('p').textContent;

        fullscreenImage.src = fullSizeImageSrc;
        fullscreenImage.alt = title;
        fullscreenTitle.textContent = title;
        fullscreenDescription.textContent = description;
        fullscreenGallery.style.display = 'flex';
        currentIndex = index;

        fullscreenImage.onload = function() {
            console.log("Image loaded successfully");
        };
        fullscreenImage.onerror = function() {
            console.error("Failed to load image:", fullSizeImageSrc);
            fullscreenImage.alt = "Failed to load image";
        };
    }

    function hideFullscreen() {
        fullscreenGallery.style.display = 'none';
    }

    function showNext() {
        currentIndex = (currentIndex + 1) % artItems.length;
        showFullscreen(currentIndex);
    }

    function showPrev() {
        currentIndex = (currentIndex - 1 + artItems.length) % artItems.length;
        showFullscreen(currentIndex);
    }

    gallery.addEventListener('click', function(e) {
        if (e.target.tagName === 'IMG') {
            const artItem = e.target.closest('.art-item');
            if (artItem) {
                const index = artItems.indexOf(artItem);
                showFullscreen(index);
            }
        }
    });

    closeButton.addEventListener('click', hideFullscreen);
    nextButton.addEventListener('click', showNext);
    prevButton.addEventListener('click', showPrev);

    let touchstartX = 0;
    let touchendX = 0;

    fullscreenGallery.addEventListener('touchstart', e => {
        touchstartX = e.changedTouches[0].screenX;
    });

    fullscreenGallery.addEventListener('touchend', e => {
        touchendX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        if (touchendX < touchstartX) showNext();
        if (touchendX > touchstartX) showPrev();
    }

    document.addEventListener('keydown', function(e) {
        if (fullscreenGallery.style.display === 'flex') {
            if (e.key === 'ArrowRight') showNext();
            if (e.key === 'ArrowLeft') showPrev();
            if (e.key === 'Escape') hideFullscreen();
        }
    });
});