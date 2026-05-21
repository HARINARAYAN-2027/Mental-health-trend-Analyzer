/**
 * Mental Health Trend Analyzer - Main Shared Frontend Logic
 * Optimized for Production Navigation Security & Distributed Sessions
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // ==================== 1. Highlight Active Nav Link ====================
    const currentPath = window.location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (currentPath === "" && linkPath === "index.html")) {
            link.classList.add('active');
        }
    });

    // ==================== 2. Dynamic Scroll Effect on Navbar ====================
    window.addEventListener('scroll', () => {
        const nav = document.querySelector('nav');
        if (nav) {
            if (window.scrollY > 40) {
                nav.style.background = 'rgba(15, 23, 42, 0.95)';
                nav.style.padding = '0.9rem 5%';
                nav.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
            } else {
                nav.style.background = 'rgba(15, 23, 42, 0.7)';
                nav.style.padding = '1.2rem 5%';
                nav.style.boxShadow = 'none';
            }
        }
    });

    // ==================== 3. SECURITY GATE: Route Protection Layer ====================
    const securePages = ['analyzer.html', 'dashboard.html', 'trends.html'];
    const sessionToken = localStorage.getItem('mentalflow_token');

    if (securePages.includes(currentPath) && !sessionToken) {
        console.warn("Unauthorized attempt bypassed. Diverting user back to authorization portal.");
        alert("Bhai, is page ko access karne ke liye pehle Login karna compulsory hai!");
        window.location.href = "index.html";
        return;
    }

    // ==================== 4. AUTOMATIC LOGOUT IMPLEMENTATION ====================
    // Agar aapne navbar me koi Logout button lagaya hai ya lagayenge jiski class/id 'btn-logout' ho
    const logoutBtn = document.getElementById('btn-logout') || document.querySelector('.logout-link');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Clear all structural token headers from memory
            localStorage.removeItem('mentalflow_token');
            localStorage.removeItem('mentalflow_user_id');
            localStorage.removeItem('mentalflow_username');
            localStorage.removeItem('recent_analysis_result');

            alert("Logged out successfully! See you soon bhai.");
            window.location.href = "index.html";
        });
    }
});

/**
 * Utility helper to get stored Auth token or details safely
 * Can be reused across analytics and chart mapping scripts
 */
function getAuthHeaders() {
    const token = localStorage.getItem('mentalflow_token');
    return token ? { 
        'Authorization': `Bearer ${token}`, 
        'Content-Type': 'application/json' 
    } : { 
        'Content-Type': 'application/json' 
    };
}
