const express = require("express");
const path = require("path");
const swaggerUi = require("swagger-ui-express");
const swaggerJsdoc = require("swagger-jsdoc");
const fetch = require("node-fetch");
const { error } = require("console");

const app = express();
const PORT = 8080;

// Middleware
app.use(express.json());
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Swagger configuration
const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: "3.0.0",
    info: {
      title: "Infinity Cafe Frontend API",
      version: "1.0.0",
      description: "Dokumentasi untuk frontend Infinity Cafe",
    },
    servers: [{ url: "http://frontend:8080" }],
  },
  apis: ["./server.js"],
});

app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ========== API ROUTES ==========

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});



// User endpoints
app.post('/login', async (req, res) => {
  try {
    const response = await fetch('http://user_service:8005/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/register', async (req, res) => {
  try {
    const response = await fetch('http://user_service:8005/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Car endpoints
app.get('/cars', async (req, res) => {
  try {
    const response = await fetch('http://car_service:8007/cars');
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/cars/:car_id/variants', async (req, res) => {
  try {
    const { car_id } = req.params;
    const response = await fetch(`http://car_service:8007/cars/${car_id}/variants`);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/variants/:variant_id', async (req, res) => {
  try {
    const { variant_id } = req.params;
    const response = await fetch(`http://car_service:8007/variants/${variant_id}`);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/recommendations', async (req, res) => {
  try {
    const params = new URLSearchParams(req.query);
    const response = await fetch(`http://car_service:8007/recommendations?${params}`);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/compare', async (req, res) => {
  try {
    const params = new URLSearchParams(req.query);
    const response = await fetch(`http://car_service:8007/compare?${params}`);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/promotions', async (req, res) => {
  try {
    const response = await fetch('http://car_service:8007/promotions');
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/stock', async (req, res) => {
  try {
    const params = new URLSearchParams(req.query);
    const response = await fetch(`http://car_service:8007/stock?${params}`);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// JWT validation function
function validateJWT(token) {
  try {
    if (!token) return false;
    
    // Split JWT into parts
    const parts = token.split('.');
    if (parts.length !== 3) return false;
    
    // Decode payload (middle part)
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
    
    // Check if token is expired
    const currentTime = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < currentTime) {
      console.log('Token expired');
      return false;
    }
    
    // Check if token has required fields
    if (!payload.sub) {
      console.log('Token missing subject');
      return false;
    }
    
    return true;
  } catch (error) {
    console.log('JWT validation error:', error.message);
    return false;
  }
}

// Authentication middleware
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '') || req.query.token;
  const tempToken = req.query.temp;
  
  // If we have a temporary token, allow access (client-side will handle validation)
  if (tempToken) {
    console.log('Temporary token provided, allowing access');
    return next();
  }
  
  // If we have a regular token, validate it
  if (token) {
    if (!validateJWT(token)) {
      console.log('Invalid or expired token');
      return res.redirect('/login');
    }
    console.log('Token validated successfully');
    return next();
  }
  
  // No token provided - let client-side handle authentication
  // This allows page refreshes to work properly
  console.log('No token provided, allowing access for client-side auth check');
  return next();
}

// ========== PAGE ROUTES ==========
app.get("/", (req, res) => {
  res.redirect("/login");
});

app.get("/dashboard", requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "login.html"));
});

// ========== STATIC FILES (MUST COME LAST) ==========
app.use(express.static(path.join(__dirname, "public")));

// Start server
app.listen(PORT, () => {
  console.log(`✅ Frontend running at http://localhost:${PORT}`);
  console.log(`📘 Swagger docs available at http://localhost:${PORT}/docs`);
});