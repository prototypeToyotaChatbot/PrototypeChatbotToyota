# 🤖 Chatbot Configuration Guide

## 📍 Lokasi Konfigurasi

### 1. **Environment Variables (.env)**
File: `/.env`

```env
# =================================================================
# CHATBOT CONFIGURATION - Anda bisa mengganti konfigurasi di sini
# =================================================================

# N8N Webhook untuk AI Chatbot (ganti dengan URL webhook N8N Anda)
N8N_CHATBOT_WEBHOOK_URL=https://your-n8n-instance.com/webhook/chatbot

# Enable/disable AI processing (true/false)
USE_AI_PROCESSING=false

# Timeout untuk webhook request (detik)
WEBHOOK_TIMEOUT=30

# Pesan-pesan chatbot (bisa diganti sesuai kebutuhan)
WELCOME_MESSAGE=Hello! I'm your car consultant assistant...
FALLBACK_MESSAGE=I'd be happy to help you with car-related questions...
ERROR_MESSAGE=I'm sorry, I'm experiencing some technical difficulties...
```

### 2. **Chat Logic**
File: `/infinity/car_service/main.py`
- Function: `chat_with_assistant()` (line ~640)
- Function: `call_n8n_webhook()` (line ~620)
- Function: `get_welcome_response()` (line ~650)

## 🔧 Cara Menggunakan

### **Step 1: Setup N8N Webhook URL**
1. Buka file `.env`
2. Ganti `N8N_CHATBOT_WEBHOOK_URL` dengan URL webhook N8N Anda:
```env
N8N_CHATBOT_WEBHOOK_URL=https://your-n8n-domain.com/webhook/your-webhook-id
```

### **Step 2: Enable AI Processing**
```env
USE_AI_PROCESSING=true
```

### **Step 3: Customize Messages**
```env
WELCOME_MESSAGE=Halo! Saya asisten konsultasi mobil Anda...
FALLBACK_MESSAGE=Saya siap membantu Anda dengan pertanyaan tentang mobil...
ERROR_MESSAGE=Maaf, saya sedang mengalami gangguan teknis...
```

### **Step 4: Restart Container**
```bash
docker-compose up --build -d car_service
```

## 🔄 Flow Chatbot

```
User Input → Frontend → Gateway → Car Service → N8N Webhook → AI Processing → Response
```

### **Payload yang Dikirim ke N8N:**
```json
{
  "message": "User input message",
  "context": {
    "session_id": "optional"
  },
  "timestamp": "2025-09-27T10:30:00"
}
```

### **Expected Response dari N8N:**
```json
{
  "output": "AI generated response",
  "session_id": "optional"
}
```

## 🧪 Testing

### **Test dengan AI Disabled (Fallback Mode):**
```bash
curl -X POST http://localhost:2323/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### **Test dengan AI Enabled:**
1. Set `USE_AI_PROCESSING=true` di `.env`
2. Set valid `N8N_CHATBOT_WEBHOOK_URL`
3. Restart container
4. Test dengan curl di atas

## 📝 Customization Options

### **1. Ubah Pesan Selamat Datang:**
Edit `WELCOME_MESSAGE` di `.env`

### **2. Ubah Fallback Response:**
Edit function `get_fallback_response()` di `main.py`

### **3. Tambah Custom Logic:**
Edit function `chat_with_assistant()` di `main.py`

### **4. Ubah Webhook Payload:**
Edit function `call_n8n_webhook()` di `main.py`

## 🚨 Troubleshooting

**Webhook tidak dipanggil:**
- Cek `USE_AI_PROCESSING=true`
- Cek `N8N_CHATBOT_WEBHOOK_URL` valid
- Cek network connection

**Timeout errors:**
- Increase `WEBHOOK_TIMEOUT` value
- Check N8N webhook response time

**Fallback responses:**
- Normal behavior ketika AI processing disabled
- Atau ketika webhook gagal

## 🔐 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_CHATBOT_WEBHOOK_URL` | "" | URL webhook N8N untuk AI processing |
| `USE_AI_PROCESSING` | false | Enable/disable AI processing |
| `WEBHOOK_TIMEOUT` | 30 | Timeout webhook request (seconds) |
| `WELCOME_MESSAGE` | Default greeting | Pesan pembuka chatbot |
| `FALLBACK_MESSAGE` | Default fallback | Pesan fallback ketika AI tidak tersedia |
| `ERROR_MESSAGE` | Default error | Pesan error ketika terjadi kesalahan |