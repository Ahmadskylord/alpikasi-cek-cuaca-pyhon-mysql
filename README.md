# Aplikasi Cek Cuaca Sederhana

Aplikasi web sederhana untuk mengecek cuaca suatu kota menggunakan Flask, OpenWeatherMap API, dan MySQL. Hasil pencarian cuaca akan disimpan ke database dan ditampilkan sebagai riwayat.

## Fitur

- Cek cuaca berdasarkan nama kota (menggunakan OpenWeatherMap API)
- Menyimpan hasil pencarian ke database MySQL
- Menampilkan riwayat pencarian cuaca
- Tampilan responsif dan modern

## Instalasi

1. **Clone repository ini**  
   ```bash
   git clone https://github.com/username/cuaca.git
   cd cuaca
   ```

2. **Install dependensi Python**  
   ```bash
   pip install flask requests mysql-connector-python
   ```

3. **Buat database MySQL**  
   Masuk ke MySQL dan jalankan:
   ```sql
   CREATE DATABASE cuaca_app;
   USE cuaca_app;
   CREATE TABLE cuaca (
     id INT AUTO_INCREMENT PRIMARY KEY,
     kota VARCHAR(100),
     suhu FLOAT,
     deskripsi VARCHAR(100),
     waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

4. **Masukkan API Key OpenWeatherMap**  
   Ganti `'YOUR_API_KEY'` pada file `cuaca.py` dengan API key milik Anda dari [OpenWeatherMap](https://openweathermap.org/api).

5. **Jalankan aplikasi**  
   ```bash
   python cuaca.py
   ```

6. **Akses aplikasi di browser**  
   Buka [http://localhost:5000](http://localhost:5000)

## Struktur File

- `cuaca.py` — Source code utama aplikasi
- `README.md` — Dokumentasi aplikasi

## Lisensi

Proyek ini bebas digunakan untuk pembelajaran.
