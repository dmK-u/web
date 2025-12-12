const API_URL = 'http://localhost:5000';

// Helper to switch views
function showSection(id) {
    document.querySelectorAll('.section').forEach(div => div.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

// 1. REGISTER (AJAX)
async function register() {
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const msg = document.getElementById('reg-msg');

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            msg.className = 'success';
            msg.innerText = 'Registration successful! Please login.';
            setTimeout(() => showSection('login-section'), 1500);
        } else {
            msg.className = 'error';
            msg.innerText = data.msg || data.errors?.[0]?.msg || 'Error registering';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 2. LOGIN (AJAX)
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const msg = document.getElementById('login-msg');

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // SAVE THE TOKEN
            localStorage.setItem('token', data.token);
            msg.innerText = '';
            loadDashboard();
        } else {
            msg.className = 'error';
            msg.innerText = data.msg || 'Invalid credentials';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 3. ACCESS PROTECTED ROUTE (Dashboard)
async function loadDashboard() {
    const token = localStorage.getItem('token');
    
    // If no token, force login
    if (!token) {
        showSection('login-section');
        return;
    }

    // Update UI
    document.getElementById('logout-btn').style.display = 'inline-block';
    showSection('dashboard-section');

    // Fetch protected data
    try {
        // We'll use the /dashboard endpoint if you added it, 
        // or we can test with a generic check.
        // Let's assume you added the example protected route from my first response.
        // If not, we can add it in Step 4.
        const response = await fetch(`${API_URL}/dashboard`, {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${token}` 
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('dashboard-content').innerText = 
                `Server says: "${data.msg}" (User ID: ${data.userId})`;
        } else {
            // Token might be expired
            logout();
        }
    } catch (err) {
        console.error(err);
    }
}

function logout() {
    localStorage.removeItem('token');
    document.getElementById('logout-btn').style.display = 'none';
    showSection('login-section');
}
