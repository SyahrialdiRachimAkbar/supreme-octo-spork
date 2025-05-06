## Rencana Proyek: Prediksi Resistensi Antibiotik dengan Machine Learning dan Streamlit

Berikut adalah langkah-langkah yang akan kita lakukan untuk menyelesaikan proyek ini:

- [x] **Langkah 1: Definisikan Ruang Lingkup dan Kebutuhan Proyek**
  - [x] Tentukan jenis antibiotik yang akan diprediksi resistensinya.
  - [x] Identifikasi fitur-fitur (data pasien, data mikroba, dll.) yang relevan untuk prediksi.
  - [x] Tetapkan metrik evaluasi untuk model machine learning (misalnya, akurasi, presisi, recall, F1-score).
  - [x] Tentukan fungsionalitas inti aplikasi Streamlit (input pengguna, output prediksi).

- [x] **Langkah 2: Cari dan Kumpulkan Dataset Resistensi Antibiotik**
  - [x] Cari dataset publik yang relevan (misalnya, dari NCBI, ECDC, WHO, atau repositori data lainnya).
  - [x] Jika dataset publik tidak memadai, pertimbangkan untuk mencari data dari studi literatur atau sumber lain.
  - [x] Unduh dan simpan dataset yang dipilih.
  - [x] Dokumentasikan sumber dan karakteristik dataset.

- [x] **Langkah 3: Pra-pemrosesan dan Eksplorasi Data**
  - [x] Bersihkan data (tangani nilai yang hilang, outlier, duplikat).
  - [x] Lakukan transformasi data jika diperlukan (misalnya, encoding fitur kategorikal, normalisasi/standarisasi fitur numerik).
  - [x] Lakukan analisis data eksploratif (EDA) untuk memahami distribusi data, hubungan antar fitur, dan pola resistensi.
  - [x] Lakukan seleksi fitur untuk memilih fitur yang paling informatif.

- [x] **Langkah 4: Bangun dan Evaluasi Model Machine Learning**
  - [x] Pilih beberapa algoritma machine learning yang sesuai untuk tugas klasifikasi (misalnya, Logistic Regression, Random Forest, Gradient Boosting, SVM, Neural Networks).
  - [x] Bagi dataset menjadi data latih dan data uji.
  - [x] Latih model menggunakan data latih.
  - [x] Lakukan tuning hyperparameter untuk mengoptimalkan performa model.
  - [x] Evaluasi model menggunakan data uji dan metrik yang telah ditentukan.
  - [x] Pilih model terbaik berdasarkan hasil evaluasi.

- [x] **Langkah 5: Kembangkan Aplikasi Streamlit untuk Prediksi**
  - [x] Buat antarmuka pengguna (UI) yang intuitif di Streamlit.
  - [x] Implementasikan fungsionalitas input data pengguna (fitur-fitur yang dibutuhkan model).
  - [x] Muat model machine learning yang telah dilatih.
  - [x] Implementasikan logika prediksi menggunakan model.
  - [x] Tampilkan hasil prediksi kepada pengguna secara jelas.
  - [x] Tambahkan informasi pendukung (misalnya, penjelasan tentang resistensi antibiotik, cara interpretasi hasil).

- [ ] **Langkah 6: Deploy Aplikasi Streamlit**
  - [x] Siapkan environment untuk deployment (misalnya, file requirements.txt).
  - [ ] Pilih platform deployment untuk Streamlit (misalnya, Streamlit Sharing, Heroku, AWS, GCP).
  - [ ] Deploy aplikasi ke platform yang dipilih.
  - [ ] Pastikan aplikasi dapat diakses secara publik.

- [ ] **Langkah 7: Validasi Deployment dan Performa Model**
  - [ ] Uji fungsionalitas aplikasi Streamlit yang telah di-deploy.
  - [ ] Lakukan pengujian input dengan berbagai skenario.
  - [ ] Verifikasi bahwa prediksi yang dihasilkan konsisten dengan performa model yang dievaluasi sebelumnya.
  - [ ] Kumpulkan feedback jika memungkinkan.

- [ ] **Langkah 8: Laporan dan Kirim Proyek ke Pengguna**
  - [ ] Buat laporan proyek yang merangkum semua langkah, metodologi, hasil, dan tantangan yang dihadapi.
  - [ ] Sertakan kode sumber proyek (notebook analisis data, skrip model, kode aplikasi Streamlit).
  - [ ] Berikan instruksi cara menjalankan dan menggunakan aplikasi.
  - [ ] Kirim semua deliverables kepada pengguna.
