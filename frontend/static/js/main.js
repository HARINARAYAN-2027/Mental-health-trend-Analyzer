/**
 * Mental Health Trend Analyzer - Main Shared Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Highlight Active Nav Link based on Current Page URL
    const currentPath = window.location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (currentPath === "" && linkPath === "index.html")) {
            link.classList.add('active');
        }
    });

    // 2. Dynamic Scroll Effect on Navbar
    window.addEventListener('scroll', () => {
        const nav = document.querySelector('nav');
        if (window.scrollY > 40) {
            nav.style.background = 'rgba(15, 23, 42, 0.92)';
            nav.style.padding = '0.9rem 5%';
        } else {
            nav.style.background = 'rgba(15, 23, 42, 0.7)';
            nav.style.padding = '1.2rem 5%';
        }
    });
});

/**
 * Utility helper to get stored Auth token or details safely
 */
function getAuthHeaders() {
    const token = localStorage.getItem('mentalflow_token');
    return token ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };
}