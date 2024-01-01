// Function to load the navbar
document.addEventListener("DOMContentLoaded", function() {
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

// Function to toggle the menu in mobile view
function toggleMenu() {
    var navItems = document.getElementById('navItems');
    if (navItems.style.display === 'block') {
        navItems.style.display = 'none';
    } else {
        navItems.style.display = 'block';
    }
}

// Reset navbar when window is resized
window.onresize = function() {
    var navItems = document.getElementById('navItems');
    if (window.innerWidth > 768) { // Adjust this value based on your media query breakpoint
        navItems.style.display = 'flex'; // Or 'block', depending on your original design
    } else {
        navItems.style.display = 'none';
    }
};
