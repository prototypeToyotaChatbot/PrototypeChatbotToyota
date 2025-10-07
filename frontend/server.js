/**
 * Toyota Chatbot Frontend Server
 * Express.js server yang bertindak sebagai proxy untuk backend services
 * Menghindari masalah CORS dan localhost saat deployment
 */

import express from "express";
import { handler } from "./build/handler.js";
import fetch from "node-fetch";

const app = express();
const PORT = process.env.PORT || 3000;

// Service URLs - menggunakan Docker service names untuk internal network
const CAR_SERVICE_URL = process.env.CAR_SERVICE_URL || "http://car_service:8007";
const GATEWAY_URL = process.env.GATEWAY_URL || "http://toyota-gateway:2323";

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// ========== HEALTH CHECK ==========
app.get("/health", (req, res) => {
  res.json({ 
    status: "ok", 
    service: "toyota-frontend",
    timestamp: new Date().toISOString()
  });
});

// ========== API PROXY ROUTES ==========

/**
 * Chat endpoint - Main chatbot conversation
 */
app.post("/api/chat", async (req, res) => {
  try {
    const body = req.body;
    console.log("Chat request:", { message: body.message?.substring(0, 50) });

    const response = await fetch(`${GATEWAY_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to process chat:", err);
    res.status(500).json({ 
      "session-id": null,
      output: "Maaf, terjadi kesalahan. Silakan coba lagi."
    });
  }
});

/**
 * Car recommendations endpoint
 */
app.get("/api/recommendations", async (req, res) => {
  try {
    const queryParams = new URLSearchParams(req.query);
    const url = `${GATEWAY_URL}/recommendations${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    console.log("Fetching recommendations:", url);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch recommendations:", err);
    res.status(500).json({ 
      error: "Failed to fetch recommendations",
      data: [],
      total: 0
    });
  }
});

/**
 * Car comparison endpoint
 */
app.get("/api/compare", async (req, res) => {
  try {
    const queryParams = new URLSearchParams();
    
    // Handle multiple variant_ids
    if (Array.isArray(req.query.variant_ids)) {
      req.query.variant_ids.forEach(id => queryParams.append('variant_ids', id));
    } else if (req.query.variant_ids) {
      queryParams.append('variant_ids', req.query.variant_ids);
    }

    const url = `${GATEWAY_URL}/compare?${queryParams.toString()}`;
    console.log("Comparing variants:", url);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to compare variants:", err);
    res.status(500).json({ 
      error: "Failed to compare variants",
      data: [],
      comparison_summary: {}
    });
  }
});

/**
 * Car variant details endpoint
 */
app.get("/api/variants/:variant_id", async (req, res) => {
  try {
    const { variant_id } = req.params;
    const url = `${GATEWAY_URL}/variants/${variant_id}`;
    
    console.log("Fetching variant details:", variant_id);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch variant details:", err);
    res.status(500).json({ 
      error: "Failed to fetch variant details"
    });
  }
});

/**
 * Promotions endpoint
 */
app.get("/api/promotions", async (req, res) => {
  try {
    const queryParams = new URLSearchParams(req.query);
    const url = `${GATEWAY_URL}/promotions${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    console.log("Fetching promotions:", url);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch promotions:", err);
    res.status(500).json({ 
      error: "Failed to fetch promotions",
      data: [],
      total: 0
    });
  }
});

/**
 * Stock availability endpoint
 */
app.get("/api/stock", async (req, res) => {
  try {
    const queryParams = new URLSearchParams(req.query);
    const url = `${GATEWAY_URL}/stock${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    console.log("Checking stock:", url);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to check stock:", err);
    res.status(500).json({ 
      error: "Failed to check stock",
      data: []
    });
  }
});

/**
 * Cars list endpoint
 */
app.get("/api/cars", async (req, res) => {
  try {
    const queryParams = new URLSearchParams(req.query);
    const url = `${GATEWAY_URL}/cars${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    console.log("Fetching cars:", url);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch cars:", err);
    res.status(500).json({ 
      error: "Failed to fetch cars",
      data: [],
      total: 0
    });
  }
});

/**
 * Car variants by car ID endpoint
 */
app.get("/api/cars/:car_id/variants", async (req, res) => {
  try {
    const { car_id } = req.params;
    const url = `${GATEWAY_URL}/cars/${car_id}/variants`;
    
    console.log("Fetching car variants:", car_id);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch car variants:", err);
    res.status(500).json({ 
      error: "Failed to fetch car variants",
      data: []
    });
  }
});

/**
 * Accessories endpoint
 */
app.get("/api/accessories", async (req, res) => {
  try {
    const url = `${GATEWAY_URL}/accessories`;
    
    console.log("Fetching accessories");

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch accessories:", err);
    res.status(500).json({ 
      error: "Failed to fetch accessories",
      data: []
    });
  }
});

/**
 * Variant accessories endpoint
 */
app.get("/api/variants/:variant_id/accessories", async (req, res) => {
  try {
    const { variant_id } = req.params;
    const url = `${GATEWAY_URL}/variants/${variant_id}/accessories`;
    
    console.log("Fetching variant accessories:", variant_id);

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch variant accessories:", err);
    res.status(500).json({ 
      error: "Failed to fetch variant accessories",
      data: []
    });
  }
});

/**
 * Workshops endpoint
 */
app.get("/api/workshops", async (req, res) => {
  try {
    const queryParams = new URLSearchParams(req.query);
    const url = `${GATEWAY_URL}/workshops${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    console.log("Fetching workshops");

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch workshops:", err);
    res.status(500).json({ 
      error: "Failed to fetch workshops",
      data: []
    });
  }
});

/**
 * Communities endpoint
 */
app.get("/api/communities", async (req, res) => {
  try {
    const queryParams = new URLSearchParams(req.query);
    const url = `${GATEWAY_URL}/communities${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    console.log("Fetching communities");

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch communities:", err);
    res.status(500).json({ 
      error: "Failed to fetch communities",
      data: []
    });
  }
});

/**
 * Dress codes endpoint
 */
app.get("/api/dress-codes", async (req, res) => {
  try {
    const url = `${GATEWAY_URL}/dress-codes`;
    
    console.log("Fetching dress codes");

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Failed to fetch dress codes:", err);
    res.status(500).json({ 
      error: "Failed to fetch dress codes",
      data: []
    });
  }
});

// ========== SVELTEKIT HANDLER ==========
// Let SvelteKit handle all other routes
app.use(handler);

// ========== ERROR HANDLING ==========
app.use((err, req, res, next) => {
  console.error("Server error:", err);
  res.status(500).json({ 
    error: "Internal server error",
    message: err.message 
  });
});

// ========== START SERVER ==========
app.listen(PORT, () => {
  console.log(`✅ Toyota Chatbot Frontend running at http://localhost:${PORT}`);
  console.log(`🔗 Gateway URL: ${GATEWAY_URL}`);
  console.log(`🚗 Car Service URL: ${CAR_SERVICE_URL}`);
  console.log(`📱 Ready for deployment!`);
});
