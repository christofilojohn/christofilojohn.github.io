document.addEventListener("DOMContentLoaded", function() {
    // ===== TYPEWRITER EFFECT =====
    class TypeWriter {
        constructor(element, text, speed = 50, onComplete = null) {
            this.element = element;
            this.text = text;
            this.speed = speed;
            this.onComplete = onComplete;
            this.currentIndex = 0;
            this.isTyping = false;
        }
        
        start() {
            if (this.isTyping) return;
            this.isTyping = true;
            this.element.textContent = '';
            this.type();
        }
        
        type() {
            if (this.currentIndex < this.text.length) {
                this.element.textContent += this.text.charAt(this.currentIndex);
                this.currentIndex++;
                setTimeout(() => this.type(), this.speed);
            } else {
                this.isTyping = false;
                if (this.onComplete) this.onComplete();
            }
        }
    }
    
    // Initialize typewriter for hero subtitle
    const subtitle = document.getElementById('heroSubtitle');
    if (subtitle) {
        const originalText = subtitle.textContent;
        subtitle.textContent = '';
        
        // Wait for page load animation, then start typing
        setTimeout(() => {
            const typewriter = new TypeWriter(subtitle, originalText, 40);
            typewriter.start();
        }, 800);
    }

    // ===== MATRIX RAIN BACKGROUND (OPTIONAL ENHANCEMENT) =====
    function createMatrixRain() {
        const canvas = document.createElement('canvas');
        canvas.id = 'matrix-rain';
        canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:-2;opacity:0.03;';
        document.body.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        
        function draw() {
            ctx.fillStyle = 'rgba(10, 14, 20, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00ff88';
            ctx.font = fontSize + 'px JetBrains Mono';
            
            for (let i = 0; i < drops.length; i++) {
                const char = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(char, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        setInterval(draw, 50);
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }
    
    // Uncomment to enable matrix rain effect
    // createMatrixRain();

    // ===== IMAGE GALLERY FUNCTIONALITY =====
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

        showSlide(0);

        imageGallery.addEventListener('click', function(e) {
            if (e.target.classList.contains('dot')) {
                currentSlideIndex = Array.from(e.target.parentNode.children).indexOf(e.target);
                showSlide(currentSlideIndex);
            }
        });

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

    // ===== ART GALLERY FULLSCREEN =====
    const artGallery = document.querySelector('.art-gallery');
    const fullscreenGallery = document.getElementById('fullscreen-gallery');

    if (artGallery && fullscreenGallery) {
        const fullscreenImage = document.getElementById('fullscreen-image');
        const fullscreenTitle = document.getElementById('fullscreen-title');
        const fullscreenDescription = document.getElementById('fullscreen-description');
        const artItems = Array.from(artGallery.querySelectorAll('.art-item'));
        let currentArtIndex = 0;

        function setMaxImageSize() {
            const maxWidth = Math.min(window.innerWidth * 0.9, 1200);
            const maxHeight = window.innerHeight * 0.8;
            fullscreenImage.style.maxWidth = `${maxWidth}px`;
            fullscreenImage.style.maxHeight = `${maxHeight}px`;
        }

        function showFullscreen(index) {
            const item = artItems[index];
            fullscreenImage.src = item.dataset.src;
            fullscreenImage.alt = item.querySelector('h3').textContent;
            fullscreenTitle.textContent = '> ' + item.querySelector('h3').textContent;
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

        document.getElementById('close-button')?.addEventListener('click', hideFullscreen);
        document.getElementById('next-button')?.addEventListener('click', () => showFullscreen((currentArtIndex + 1) % artItems.length));
        document.getElementById('prev-button')?.addEventListener('click', () => showFullscreen((currentArtIndex - 1 + artItems.length) % artItems.length));

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
