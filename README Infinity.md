
# Prototype Chatbot Toyota Microservices

Prototype Chatbot Toyota adalah rangkaian layanan mikro (microservices) demo yang menampilkan integrasi chatbot RAG, layanan data kendaraan, dan alur agent menggunakan Python + FastAPI + PgVector17 + FastAPI-MCP.

## 📦 Struktur Folder (contoh layanan)

```
infinity/      # folder kode demo (nama folder dipertahankan untuk kompatibilitas seed/db)
├── requirements.txt
├── car_service/
│   ├── Dockerfile
│   └── main.py
│   ├── Dockerfile
│   └── main.py
```

## 🚀 Cara Menjalankan (singkat)

1. **Persiapan:**
   - Install Docker dan Docker Compose

2. **Jalankan layanan:**
   ```bash
   docker compose up --build
   ```

3. **Akses:**
   - Car Service → [http://localhost:8001](http://localhost:8001)
   - QwenAgent / Model API → [http://localhost:9000](http://localhost:9000)

## 📝 Endpoint
- **QwenAgent Service:**
   - POST `http://localhost:9000/api/chat` untuk chat dengan agent/model. Contoh body (sesuaikan dengan service):
      ```json
      {
         "messages": "Tambahkan data kendaraan baru dengan model 'Avanza' dan varian 'G'.",
      }



## 🔗 Koneksi Antar Layanan

- `order_service` akan otomatis meneruskan order ke `kitchen_service` jika order valid.
- Semua service menggunakan database bersama: `infinitycafe_db`.

## 🔍 Testing

Gunakan Postman collection `InfinityCafe_PostmanCollection.json` untuk menguji seluruh endpoint layanan.

## 🙌 Kontribusi & Lisensi

Proyek ini dibuat untuk pembelajaran dan simulasi produksi ringan.  
Silakan kembangkan lebih lanjut sesuai kebutuhan.


How to install
0. ubah file .env 

1. running docker desktop
2. docker compose --profile gpu-amd up
3. add Database n8n
4. docker compose --profile gpu-amd up lagi
