const express = require('express');
const axios = require('axios');
const session = require('express-session');
const flash = require('connect-flash');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Configuration
app.set('views', path.join(__dirname, 'templates'));

// Helper to render HTML files
const renderHTML = (res, filePath, data = {}) => {
  const fullPath = path.join(__dirname, 'templates', filePath);
  fs.readFile(fullPath, 'utf8', (err, html) => {
    if (err) {
      console.error('Error reading HTML file:', err);
      return res.status(500).send('Internal Server Error');
    }
    res.send(html);
  });
};

// Middleware
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Session configuration
app.use(session({
    secret: process.env.SESSION_SECRET || 'artgram-session-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false } // Set to true in production with HTTPS
}));

app.use(flash());

// API Gateway URL
const API_GATEWAY = process.env.API_GATEWAY || 'http://localhost:8000';

// Helper function to make API requests
async function apiRequest(method, url, data = null, headers = {}) {
    try {
        const config = {
            method,
            url: `${API_GATEWAY}${url}`,
            headers: {
                'Content-Type': 'application/json',
                ...headers
            }
        };
        
        if (data) {
            config.data = data;
        }
        
        const response = await axios(config);
        return response.data;
    } catch (error) {
        console.error('API Request Error:', error.response?.data || error.message);
        throw error;
    }
}

// Authentication middleware
function isAuthenticated(req, res, next) {
    if (req.session.token) {
        next();
    } else {
        res.redirect('/login');
    }
}

// Routes - Serving Django Templates Exactly As Is

// Landing Page
app.get('/', async (req, res) => {
    try {
        // Check if user is logged in
        if (req.session.token) {
            res.redirect('/explore');
        } else {
            renderHTML(res, 'landing.html');
        }
    } catch (error) {
        renderHTML(res, 'landing.html');
    }
});

// Authentication Routes
app.get('/login', (req, res) => {
    renderHTML(res, 'users/login.html');
});

app.post('/login', async (req, res) => {
    try {
        const response = await apiRequest('POST', '/api/auth/token/', {
            username: req.body.username,
            password: req.body.password
        });
        
        req.session.token = response.tokens.access;
        req.session.user = response.user;
        req.flash('success', 'Login successful!');
        
        res.redirect('/explore');
    } catch (error) {
        req.flash('error', 'Invalid credentials');
        res.redirect('/login');
    }
});

app.get('/register', (req, res) => {
    renderHTML(res, 'users/register.html');
});

app.post('/register', async (req, res) => {
    try {
        const response = await apiRequest('POST', '/api/auth/register/', req.body);
        
        req.session.token = response.tokens.access;
        req.session.user = response.user;
        req.flash('success', 'Registration successful!');
        
        res.redirect('/complete-profile');
    } catch (error) {
        req.flash('error', 'Registration failed');
        res.redirect('/register');
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/');
});

// Profile Routes
app.get('/complete-profile', isAuthenticated, (req, res) => {
    renderHTML(res, 'users/profile_complete.html');
});

app.post('/complete-profile', async (req, res) => {
    try {
        await apiRequest('PUT', '/api/auth/profile/', req.body, {
            'Authorization': `Bearer ${req.session.token}`
        });
        
        req.flash('success', 'Profile updated!');
        res.redirect('/explore');
    } catch (error) {
        req.flash('error', 'Profile update failed');
        res.redirect('/complete-profile');
    }
});

app.get('/profile/@:username/', async (req, res) => {
    try {
        const userProfile = await apiRequest('GET', `/api/users/profile/${req.params.username}/`);
        renderHTML(res, 'users/profile.html');
    } catch (error) {
        res.status(404);
        renderHTML(res, 'users/profile.html');
    }
});

// Explore Routes
app.get('/explore/', isAuthenticated, async (req, res) => {
    try {
        const artworks = await apiRequest('GET', '/api/explore/');
        renderHTML(res, 'explore/home.html');
    } catch (error) {
        renderHTML(res, 'explore/home.html');
    }
});

// Artwork Routes
app.get('/artworks/', isAuthenticated, async (req, res) => {
    try {
        const artworks = await apiRequest('GET', '/api/artworks/');
        renderHTML(res, 'artworks/home.html');
    } catch (error) {
        renderHTML(res, 'artworks/home.html');
    }
});

app.get('/artworks/create/', isAuthenticated, (req, res) => {
    renderHTML(res, 'artworks/create.html');
});

app.post('/artworks/create/', isAuthenticated, async (req, res) => {
    try {
        await apiRequest('POST', '/api/artworks/create/', req.body, {
            'Authorization': `Bearer ${req.session.token}`
        });
        
        req.flash('success', 'Artwork created!');
        res.redirect('/artworks/');
    } catch (error) {
        req.flash('error', 'Failed to create artwork');
        res.redirect('/artworks/create/');
    }
});

app.get('/artwork/:slug/', isAuthenticated, async (req, res) => {
    try {
        const artwork = await apiRequest('GET', `/api/artworks/${req.params.slug}/`);
        renderHTML(res, 'artworks/detail.html');
    } catch (error) {
        res.status(404);
        renderHTML(res, 'artworks/detail.html');
    }
});

app.get('/artworks/my-artworks/', isAuthenticated, async (req, res) => {
    try {
        const artworks = await apiRequest('GET', '/api/artworks/my-artworks/', null, {
            'Authorization': `Bearer ${req.session.token}`
        });
        renderHTML(res, 'artworks/my_artworks.html');
    } catch (error) {
        renderHTML(res, 'artworks/my_artworks.html');
    }
});

app.get('/profile/add-work/', isAuthenticated, (req, res) => {
    renderHTML(res, 'users/add_work.html');
});

// Notifications
app.get('/notifications/', isAuthenticated, async (req, res) => {
    try {
        const notifications = await apiRequest('GET', '/api/notifications/', null, {
            'Authorization': `Bearer ${req.session.token}`
        });
        renderHTML(res, 'notifications/home.html');
    } catch (error) {
        renderHTML(res, 'notifications/home.html');
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`ArtGram Web UI running on port ${PORT}`);
    console.log(`API Gateway: ${API_GATEWAY}`);
});
