# Bike Sharing Dashboard

## Deskripsi Proyek
Proyek ini adalah aplikasi dashboard interaktif yang dibuat menggunakan Streamlit untuk menganalisis dan memvisualisasikan data penyewaan sepeda. Dashboard ini memberikan wawasan tentang tren penyewaan sepeda berdasarkan data per hari dan per jam, serta faktor-faktor yang mempengaruhi seperti cuaca dan musim.

### Fitur-fitur:
- Visualisasi tren penyewaan sepeda berdasarkan bulan dan tahun.
- Tren penyewaan sepeda berdasarkan hari dalam seminggu.
- Analisis penyewaan sepeda per jam.
- Pengaruh cuaca dan musim terhadap jumlah penyewaan.
- Statistik umum tentang data penyewaan sepeda.

## Cara Menjalankan Dashboard

1. **Install Dependensi**
   Setelah mengunduh atau meng-clone repositori ini, pastikan untuk menginstal semua dependensi yang diperlukan. Jalankan perintah berikut di terminal:

   ```bash
   pip install -r requirements.txt

2. Menjalankan Streamlit Setelah instalasi selesai, buka terminal dan navigasikan ke folder proyek, lalu jalankan perintah berikut untuk membuka dashboard:
    streamlit run dashboard/dashboard.py

3. Akses Dashboard Setelah menjalankan perintah tersebut, Streamlit akan memberikan URL yang bisa diakses di browser untuk melihat dashboard.

## Penjelasan Dataset
Proyek ini menggunakan dua dataset:
1. day.csv: Data penyewaan sepeda per hari yang berisi informasi tentang jumlah penyewaan sepeda pada setiap hari.
2. hour.csv: Data penyewaan sepeda per jam yang berisi informasi tentang jumlah penyewaan sepeda per jam pada setiap hari.

## Kolom-Kolom dalam day.csv:
- dteday: Tanggal penyewaan.
- season: Musim (1 = Spring, 2 = Summer, 3 = Fall, 4 = Winter).
- weathersit: Kondisi cuaca (1 = Clear, 2 = Mist, 3 = Light Snow/Rain, 4 = Heavy Rain/Snow).
- cnt: Jumlah penyewaan sepeda pada hari tersebut.

## Kolom-Kolom dalam hour.csv:
- hr: Jam penyewaan.
- cnt: Jumlah penyewaan sepeda pada jam tersebut.

## Contoh Output
Dashboard ini menghasilkan berbagai visualisasi, termasuk:
1. Tren penyewaan sepeda per bulan selama tahun tertentu.
2. Boxplot untuk menunjukkan pengaruh cuaca dan musim terhadap jumlah penyewaan.
3. Visualisasi penyewaan sepeda per jam dan hari dalam seminggu.

