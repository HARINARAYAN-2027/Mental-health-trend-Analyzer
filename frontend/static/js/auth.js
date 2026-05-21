/**
 * Mental Health Trend Analyzer - Secure Authentication Bridge Pipeline
 * Synchronized with Live Render Cloud Infrastructure
 */

// CLOUD UPDATE: Switched localhost route to the live production server path
const AUTH_API = "https://mental-health-trend-analyzer.onrender.com/api/auth";

document.addEventListener('DOMContentLoaded', () => {
    
    // Switch Tabbing Elements Selection
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');
    const formLogin = document.getElementById('form-login');
    const formRegister = document.getElementById('form-register');

    // ==================== 1. Tabbing View Animation Transitions ====================
    if (tabLogin && tabRegister) {
        tabLogin.addEventListener('click', () => {
            tabLogin.style.color = "var(--accent-blue)";
            tabLogin.style.borderBottom = "2px solid var(--accent-blue)";
            tabLogin.style.fontWeight = "600";
            
            tabRegister.style.color = "var(--text-muted)";
            tabRegister.style.borderBottom = "none";
            tabRegister.style.fontWeight = "500";

            if (formLogin) formLogin.style.display = "flex";
            if (formRegister) formRegister.style.display = "none";
        });

        tabRegister.addEventListener('click', () => {
            tabRegister.style.color = "var(--accent-purple)";
            tabRegister.style.borderBottom = "2px solid var(--accent-purple)";
            tabRegister.style.fontWeight = "600";
            
            tabLogin.style.color = "var(--text-muted)";
            tabLogin.style.borderBottom = "none";
            tabLogin.style.fontWeight = "500";

            if (formRegister) formRegister.style.display = "flex";
            if (formLogin) formLogin.style.display = "none";
        });
    }

    // ==================== 2. Login Submit Event Router ====================
    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const usernamePayload = document.getElementById('login-username').value.trim();
            const passwordPayload = document.getElementById('login-password').value;

            try {
                const response = await fetch(`${AUTH_API}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: usernamePayload, password: passwordPayload })
                });

                const data = await response.json();

                if (response.ok) {
                    // Storing details safely inside localstorage standard parameters
                    localStorage.setItem('mentalflow_token', data.token);
                    localStorage.setItem('mentalflow_user_id', data.user.id);
                    localStorage.setItem('mentalflow_username', data.user.username);
                    
                    alert(`Login successfully! Welcome back, ${data.user.username}. Moving to Analytical Engine.`);
                    window.location.href = "analyzer.html";
                } else {
                    alert(`Authentication Fault: ${data.error}`);
                }
            } catch (err) {
                console.error("Auth server unreachable:", err);
                alert("Backend processing servers look offline!");
            }
        });
    }

    // ==================== 3. Registration Submit Event Router ====================
    if (formRegister) {
        formRegister.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('reg-username').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const password = document.getElementById('reg-password').value;
            const confirmPassword = document.getElementById('reg-confirm').value;

            if (password.length < 6) {
                alert("Security constraint error: Password length must be 6+ units!");
                return;
            }

            if (password !== confirmPassword) {
                alert("Mismatched data fields: Passwords matching checks failed!");
                return;
            }

            try {
                const response = await fetch(`${AUTH_API}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password, confirmPassword })
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Account provisioned successfully in local system databases! Switching to credentials confirmation panel.");
                    if (tabLogin) tabLogin.click(); // Programmatically shift form back to Sign In
                } else {
                    alert(`Database Rejection: ${data.error}`);
                }
            } catch (err) {
                console.error("Database schema network exception:", err);
                alert("Pipeline connection drop error!");
            }
        });
    }
});
