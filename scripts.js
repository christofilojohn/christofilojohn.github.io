document.addEventListener("DOMContentLoaded", function() {
    // Image gallery functionality (for main page)
    const imageGallery = document.querySelector('.image-gallery');
    if (imageGallery) {
        const slides = imageGallery.querySelectorAll('.image-container');
        let currentSlideIndex = 0;

        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.style.display = i === index ? 'block' : 'none';
            });
        }

        function nextSlide() {
            currentSlideIndex = (currentSlideIndex + 1) % slides.length;
            showSlide(currentSlideIndex);
        }

        function prevSlide() {
            currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
            showSlide(currentSlideIndex);
        }

        // Initialize the gallery
        showSlide(0);

        // Add event listeners for gallery navigation
        imageGallery.addEventListener('click', function(e) {
            if (e.target.classList.contains('dot')) {
                currentSlideIndex = Array.from(e.target.parentNode.children).indexOf(e.target);
                showSlide(currentSlideIndex);
            }
        });

        // Touch events for swiping
        let touchstartX = 0;
        imageGallery.addEventListener('touchstart', e => {
            touchstartX = e.changedTouches[0].screenX;
        });

        imageGallery.addEventListener('touchend', e => {
            const touchendX = e.changedTouches[0].screenX;
            if (touchendX < touchstartX) nextSlide();
            if (touchendX > touchstartX) prevSlide();
        });
    }

    // Art gallery fullscreen functionality
    const artGallery = document.querySelector('.art-gallery');
    const fullscreenGallery = document.getElementById('fullscreen-gallery');

    if (artGallery && fullscreenGallery) {
        const fullscreenImage = document.getElementById('fullscreen-image');
        const fullscreenTitle = document.getElementById('fullscreen-title');
        const fullscreenDescription = document.getElementById('fullscreen-description');
        const artItems = Array.from(artGallery.querySelectorAll('.art-item'));
        let currentArtIndex = 0;

        function setMaxImageSize() {
            const maxWidth = Math.min(window.innerWidth * 0.9, 1200); // Max width of 1200px or 90% of viewport width
            const maxHeight = window.innerHeight * 0.8; // 80% of viewport height
            fullscreenImage.style.maxWidth = `${maxWidth}px`;
            fullscreenImage.style.maxHeight = `${maxHeight}px`;
        }

        function showFullscreen(index) {
            const item = artItems[index];
            fullscreenImage.src = item.dataset.src;
            fullscreenImage.alt = item.querySelector('h3').textContent;
            fullscreenTitle.textContent = item.querySelector('h3').textContent;
            fullscreenDescription.textContent = item.querySelector('p').textContent;
            fullscreenGallery.style.display = 'flex';
            currentArtIndex = index;
            setMaxImageSize();
        }

        function hideFullscreen() {
            fullscreenGallery.style.display = 'none';
        }

        artGallery.addEventListener('click', function(e) {
            if (e.target.tagName === 'IMG') {
                const artItem = e.target.closest('.art-item');
                if (artItem) showFullscreen(artItems.indexOf(artItem));
            }
        });

        document.getElementById('close-button').addEventListener('click', hideFullscreen);
        document.getElementById('next-button').addEventListener('click', () => showFullscreen((currentArtIndex + 1) % artItems.length));
        document.getElementById('prev-button').addEventListener('click', () => showFullscreen((currentArtIndex - 1 + artItems.length) % artItems.length));

        let touchstartX = 0;
        fullscreenGallery.addEventListener('touchstart', e => touchstartX = e.changedTouches[0].screenX);
        fullscreenGallery.addEventListener('touchend', e => {
            const touchendX = e.changedTouches[0].screenX;
            if (touchendX < touchstartX) showFullscreen((currentArtIndex + 1) % artItems.length);
            if (touchendX > touchstartX) showFullscreen((currentArtIndex - 1 + artItems.length) % artItems.length);
        });

        document.addEventListener('keydown', function(e) {
            if (fullscreenGallery.style.display === 'flex') {
                if (e.key === 'ArrowRight') showFullscreen((currentArtIndex + 1) % artItems.length);
                if (e.key === 'ArrowLeft') showFullscreen((currentArtIndex - 1 + artItems.length) % artItems.length);
                if (e.key === 'Escape') hideFullscreen();
            }
        });
        window.addEventListener('resize', setMaxImageSize);

    }
});