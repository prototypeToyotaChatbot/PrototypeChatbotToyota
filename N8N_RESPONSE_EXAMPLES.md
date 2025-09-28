# Contoh Response dari N8N Webhook

## 📢 System Message Template

Gunakan instruksi berikut pada **System Message** di node *AI Agent* agar output selalu sesuai format yang bisa diproses backend.

```text
Kamu adalah asisten AI untuk dealer mobil.
Jawablah setiap permintaan HANYA dengan JSON valid menggunakan struktur berikut:
{
  "response": "<jawaban utama dalam format teks markdown>",
  "suggestions": ["<opsi tindak lanjut 1>", "<opsi tindak lanjut 2>", "<opsi tindak lanjut 3>", "<opsi tindak lanjut 4>"] ,
  "context": {
    "source": "ai",
    "confidence": <angka antara 0 dan 1>,
    "session_id": "{{ $json["session_id"] }}",
    "user_id": "{{ $json["context"]["user_id"] || "" }}"
  }
}

Aturan tambahan:
- Pastikan JSON valid (gunakan tanda kutip ganda dan escape karakter khusus).
- `response` boleh menggunakan markdown ringkas (bullet list, bold) tetapi tetap dalam string tunggal.
- `suggestions` berisi 2-4 string aksi spesifik yang relevan dengan jawaban.
- `context` boleh ditambah field lain, namun **harus** minimal memiliki `source`, `confidence`, dan `session_id`.
- Jika kamu tidak yakin, turunkan `confidence` dan berikan saran untuk menghubungi manusia.
- Jangan kirim teks di luar blok JSON.
```

## 1. Response untuk Pertanyaan Harga
```json
{
  "response": "Toyota Avanza tersedia dalam 3 varian dengan harga sebagai berikut:\n• Avanza E MT: Rp 230.400.000\n• Avanza G MT: Rp 245.650.000\n• Avanza Veloz: Rp 265.550.000\n\nHarga sudah termasuk PPnBM. Apakah Anda tertarik dengan varian tertentu?",
  "suggestions": [
    "Jelaskan perbedaan setiap varian",
    "Hitung simulasi kredit",
    "Lihat promo bulan ini",
    "Jadwalkan test drive"
  ],
  "context": {
    "source": "ai",
    "confidence": 0.95,
    "car_model": "avanza",
    "query_type": "pricing"
  }
}
```

## 2. Response untuk Perbandingan Mobil
```json
{
  "response": "Perbandingan Toyota Avanza vs Honda BR-V:\n\n**Toyota Avanza:**\n✓ Harga lebih terjangkau (mulai 230jt)\n✓ BBM lebih irit (13-15 km/l)\n✓ Service mudah & murah\n\n**Honda BR-V:**\n✓ Kabin lebih luas\n✓ Ground clearance lebih tinggi\n✓ Fitur safety lebih lengkap\n\nKeduanya cocok untuk keluarga, pilihan tergantung prioritas budget atau fitur.",
  "suggestions": [
    "Simulasi kredit Avanza",
    "Simulasi kredit BR-V", 
    "Lihat spesifikasi lengkap",
    "Test drive keduanya"
  ],
  "context": {
    "source": "ai",
    "confidence": 0.88,
    "comparison": ["avanza", "brv"],
    "query_type": "comparison"
  }
}
```

## 3. Response untuk Pertanyaan Umum
```json
{
  "response": "Maaf, saya kurang memahami pertanyaan Anda. Sebagai asisten Toyota, saya dapat membantu dengan:\n• Informasi harga dan spesifikasi mobil\n• Simulasi kredit dan promo\n• Perbandingan model\n• Jadwal test drive\n• Lokasi dealer terdekat\n\nApa yang ingin Anda ketahui tentang Toyota?",
  "suggestions": [
    "Lihat daftar mobil Toyota",
    "Cari dealer terdekat",
    "Info promo terbaru",
    "Hitung cicilan mobil"
  ],
  "context": {
    "source": "ai",
    "confidence": 0.60,
    "query_type": "unclear",
    "fallback_reason": "ambiguous_query"
  }
}
```

## 4. Response dengan Confidence Rendah
```json
{
  "response": "Saya belum yakin dengan informasi yang Anda butuhkan. Untuk mendapatkan informasi akurat tentang spare part Toyota yang Anda sebutkan, saya sarankan menghubungi langsung dealer Toyota terdekat atau customer service di 1500-TOYOTA.",
  "suggestions": [
    "Cari dealer terdekat",
    "Hubungi customer service",
    "Kembali ke menu utama",
    "Tanya hal lain"
  ],
  "context": {
    "source": "ai",
    "confidence": 0.35,
    "query_type": "parts_inquiry",
    "fallback_reason": "low_confidence"
  }
}
```

## Tips Penggunaan Confidence Score:

- **0.9-1.0**: Response sangat akurat, data dari database resmi
- **0.8-0.9**: Response baik, kombinasi data + AI reasoning  
- **0.7-0.8**: Response cukup baik, tapi mungkin perlu verifikasi
- **0.6-0.7**: Response general, tidak terlalu spesifik
- **0.5-0.6**: Response kurang yakin, berikan disclaimer
- **0.0-0.5**: Gunakan fallback response atau redirect ke human

## Suggestions yang Baik:

1. **Actionable**: "Jadwalkan test drive" bukan "Test drive"
2. **Specific**: "Hitung cicilan Avanza" bukan "Info kredit"  
3. **Contextual**: Sesuai dengan response yang diberikan
4. **Varied**: Berikan opsi berbeda (info, action, comparison)