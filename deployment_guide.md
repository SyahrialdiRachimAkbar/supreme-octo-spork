# Panduan Deployment Aplikasi Streamlit ke Streamlit Community Cloud via GitHub

Berikut adalah langkah-langkah untuk mendeploy aplikasi prediksi resistensi antibiotik MRSA ini ke Streamlit Community Cloud menggunakan repositori GitHub Anda:

## Prasyarat

1.  **Akun GitHub:** Anda memerlukan akun GitHub.
2.  **Akun Streamlit Community Cloud:** Anda memerlukan akun di [Streamlit Community Cloud](https://share.streamlit.io/). Anda dapat mendaftar menggunakan akun GitHub Anda.
3.  **Git:** Pastikan Git terinstal di komputer lokal Anda jika Anda ingin mengelola repositori dari terminal.

## File Proyek yang Diperlukan

Pastikan Anda memiliki file-file berikut dalam satu folder di komputer Anda. File-file ini akan diunggah ke repositori GitHub Anda:

1.  `streamlit_mrsa_app.py`: Kode utama aplikasi Streamlit.
2.  `best_mrsa_prediction_model.joblib`: Model machine learning yang telah dilatih.
3.  `requirements.txt`: File yang berisi daftar dependensi Python yang dibutuhkan oleh aplikasi.
4.  `categorical_unique_values.txt`: File yang berisi nilai unik untuk input kategorikal (digunakan oleh aplikasi).
    *Catatan: Jika Anda melatih ulang model atau menggunakan dataset yang berbeda, file ini mungkin perlu diperbarui.*

## Langkah-langkah Deployment

### 1. Buat Repositori Baru di GitHub

   a.  Buka [GitHub](https://github.com/) dan login ke akun Anda.
   b.  Buat repositori baru (misalnya, dengan nama `mrsa-prediction-streamlit-app`).
   c.  Anda dapat memilih untuk membuat repositori publik atau privat. Streamlit Community Cloud dapat mengakses keduanya (untuk repositori privat, Anda perlu memberikan otorisasi).
   d.  Jangan inisialisasi repositori dengan README, .gitignore, atau license pada tahap ini jika Anda akan mengunggah folder yang sudah ada.

### 2. Unggah File Proyek ke Repositori GitHub

   Ada dua cara umum untuk melakukan ini:

   **Cara A: Menggunakan Antarmuka Web GitHub (untuk beberapa file)**

   a.  Buka repositori yang baru saja Anda buat di GitHub.
   b.  Klik tombol "Add file" dan pilih "Upload files".
   c.  Seret dan lepas semua file proyek yang diperlukan (`streamlit_mrsa_app.py`, `best_mrsa_prediction_model.joblib`, `requirements.txt`, `categorical_unique_values.txt`) ke area unggah.
   d.  Tambahkan pesan commit (misalnya, "Initial commit with Streamlit app files") dan klik "Commit changes".

   **Cara B: Menggunakan Git dari Terminal Lokal (lebih direkomendasikan untuk manajemen proyek)**

   a.  Buka terminal atau command prompt di komputer Anda.
   b.  Navigasi ke folder tempat Anda menyimpan file-file proyek.
   c.  Inisialisasi repositori Git lokal:
      ```bash
      git init
      git branch -M main
      ```
   d.  Tambahkan URL repositori remote GitHub Anda:
      ```bash
      git remote add origin https://github.com/NAMA_PENGGUNA_ANDA/NAMA_REPOSITORI_ANDA.git
      ```
      Ganti `NAMA_PENGGUNA_ANDA` dan `NAMA_REPOSITORI_ANDA` dengan detail Anda.
   e.  Tambahkan semua file proyek ke staging area:
      ```bash
      git add streamlit_mrsa_app.py best_mrsa_prediction_model.joblib requirements.txt categorical_unique_values.txt
      # Atau tambahkan semua file di folder: git add .
      ```
   f.  Commit perubahan:
      ```bash
      git commit -m "Initial commit: Add Streamlit app for MRSA prediction"
      ```
   g.  Push perubahan ke repositori GitHub:
      ```bash
      git push -u origin main
      ```

### 3. Deploy Aplikasi dari Streamlit Community Cloud

   a.  Buka [Streamlit Community Cloud](https://share.streamlit.io/) dan login.
   b.  Klik tombol "New app" atau "Deploy an app".
   c.  **Deploy from existing repo:**
      *   **Repository:** Pilih repositori GitHub yang baru saja Anda buat (misalnya, `NAMA_PENGGUNA_ANDA/mrsa-prediction-streamlit-app`). Jika ini adalah repositori privat, Anda mungkin perlu memberikan otorisasi kepada Streamlit untuk mengaksesnya.
      *   **Branch:** Pilih branch utama Anda (biasanya `main` atau `master`).
      *   **Main file path:** Masukkan nama file utama aplikasi Streamlit Anda, yaitu `streamlit_mrsa_app.py`.
   d.  **Advanced settings (Opsional tapi direkomendasikan):**
      *   Klik "Advanced settings...".
      *   Pastikan versi Python yang dipilih sesuai atau kompatibel dengan yang digunakan untuk membuat `requirements.txt` (misalnya, Python 3.9, 3.10, atau 3.11). Aplikasi ini dikembangkan dengan Python 3.11.
   e.  Klik tombol "Deploy!".

### 4. Tunggu Proses Deployment

   Streamlit Community Cloud akan mulai membangun environment untuk aplikasi Anda berdasarkan file `requirements.txt` dan kemudian menjalankan aplikasi Anda.
   Proses ini mungkin memakan waktu beberapa menit. Anda dapat melihat log build secara real-time.

### 5. Akses Aplikasi Anda

   Setelah deployment berhasil, Anda akan diberikan URL publik untuk aplikasi Streamlit Anda (misalnya, `https://nama-pengguna-anda-nama-repo-anda-streamlit-mrsa-app-xxxxxx.streamlit.app`).
   Anda dapat membagikan URL ini kepada siapa saja untuk mengakses aplikasi prediksi Anda.

## Troubleshooting Umum

*   **Error `ModuleNotFoundError`:** Pastikan semua dependensi yang dibutuhkan oleh `streamlit_mrsa_app.py` (termasuk `pandas`, `numpy`, `scikit-learn`, `joblib`, `streamlit`) tercantum dengan benar dalam file `requirements.txt`.
*   **Aplikasi tidak memuat model (`best_mrsa_prediction_model.joblib`):** Pastikan file model ada di root repositori GitHub Anda bersama dengan `streamlit_mrsa_app.py` dan `requirements.txt`. Path ke model dalam skrip Streamlit (`MODEL_PATH = "best_mrsa_prediction_model.joblib"`) harus benar relatif terhadap file aplikasi utama.
*   **Masalah dengan `categorical_unique_values.txt`:** Pastikan file ini juga ada di root repositori dan path-nya benar dalam skrip Streamlit.
*   **Build Gagal:** Periksa log build di Streamlit Community Cloud untuk pesan error spesifik. Seringkali ini terkait dengan dependensi yang tidak kompatibel atau masalah dalam `requirements.txt`.
*   **Ukuran File Model Besar:** Jika file `.joblib` sangat besar, GitHub mungkin memiliki batasan ukuran file (biasanya 100MB). Untuk file yang lebih besar, Anda mungkin perlu menggunakan Git LFS (Large File Storage) atau menghosting model di tempat lain dan memuatnya dari URL di aplikasi Streamlit Anda (ini akan memerlukan modifikasi pada skrip `streamlit_mrsa_app.py`). Model saat ini (`best_mrsa_prediction_model.joblib`) seharusnya tidak terlalu besar.

Semoga berhasil dengan deployment aplikasi Anda!
