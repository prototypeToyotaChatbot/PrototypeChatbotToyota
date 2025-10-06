# Contoh Response dari N8N Webhook

## System Message Template

Gunakan instruksi berikut pada **System Message** di node *AI Agent* agar output selalu sesuai format yang bisa diproses backend.

```text
Kamu adalah asisten AI untuk dealer mobil.
Jawablah setiap permintaan HANYA dengan JSON valid menggunakan struktur berikut:
{
  "output": "<jawaban utama dalam format teks>",
  "session_id": "{{ $json["session_id"] || '' }}"
}

Aturan tambahan:
- Pastikan JSON valid (gunakan tanda kutip ganda dan escape karakter khusus).
- `output` boleh menggunakan markdown ringkas (bullet list, bold) tetapi tetap dalam satu string.
- `session_id` opsional; kirim hanya jika Anda ingin mempertahankan sesi khusus.
- Jangan kirim teks di luar blok JSON.
```

## 1. Response untuk Pertanyaan Harga
```json
{
  "output": "Toyota Avanza tersedia dalam 3 varian dengan harga sebagai berikut:
- Avanza E MT: Rp 230.400.000
- Avanza G MT: Rp 245.650.000
- Avanza Veloz: Rp 265.550.000

Harga sudah termasuk PPnBM. Apakah Anda tertarik dengan varian tertentu?",
  "session_id": "session-123"
}
```

## 2. Response untuk Perbandingan Mobil
```json
{
  "output": "Perbandingan Toyota Avanza vs Honda BR-V:

**Toyota Avanza**
- Harga lebih terjangkau (mulai 230 jt)
- BBM lebih irit (13-15 km/l)
- Service mudah & murah

**Honda BR-V**
- Kabin lebih luas
- Ground clearance lebih tinggi
- Fitur safety lebih lengkap

Keduanya cocok untuk keluarga; pilih sesuai prioritas budget atau fitur.",
  "session_id": "session-123"
}
```

## 3. Response untuk Pertanyaan Umum
```json
{
  "output": "Maaf, saya belum memahami pertanyaan Anda. Saya dapat membantu dengan informasi harga, promo, perbandingan model, simulasi kredit, atau jadwal test drive. Apa yang ingin Anda ketahui tentang Toyota?"
}
```

## 4. Response dengan Confidence Rendah
```json
{
  "output": "Saya belum yakin dengan informasi yang Anda butuhkan. Untuk detail mengenai spare part yang Anda sebutkan, silakan hubungi dealer Toyota terdekat atau customer service di 1500-TOYOTA."
}
```

## Tips Penyusunan Output

- Gunakan **bold** untuk menekankan nama model, varian, atau harga.
- Gunakan daftar peluru untuk spesifikasi atau perbandingan agar mudah dibaca.
- Tambahkan pertanyaan lanjutan agar percakapan berlanjut.
- Sertakan mata uang saat menyebut harga.
```
