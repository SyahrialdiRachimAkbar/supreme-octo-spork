import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px

# --- Konfigurasi Halaman (HARUS MENJADI PERINTAH STREAMLIT PERTAMA) ---
st.set_page_config(page_title="Prediktor Risiko Infeksi MRSA", layout="wide")

# --- Konfigurasi Path File ---
MODEL_PATH = "best_mrsa_prediction_model.joblib"
UNIQUE_VALUES_PATH = "categorical_unique_values.txt"
COMBINED_DATA_PATH = "combined_mrsa_hospital_data.csv"

# --- Fungsi Pemuatan (Caching) ---
@st.cache_resource
def muat_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"File model 		{MODEL_PATH}		 tidak ditemukan. Pastikan file berada di root repositori GitHub bersama skrip aplikasi.")
        return None
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None

@st.cache_data
def muat_nilai_unik():
    nilai_unik = {}
    opsi_prediksi_infeksi_default = ["0.0", "1.0", "2.0", "Tidak Tersedia"]
    opsi_kategori_rs_default = ["Tidak Diketahui", "RUMAH SAKIT PERAWATAN AKUT UMUM"]
    opsi_kabupaten_default = ["Tidak Diketahui", "Alameda"]

    if not os.path.exists(UNIQUE_VALUES_PATH):
        st.warning(f"File nilai unik 		{UNIQUE_VALUES_PATH}		 tidak ditemukan. Menggunakan opsi dropdown default.")
        nilai_unik["Infections_Predicted"] = opsi_prediksi_infeksi_default
        nilai_unik["Hospital_Category_RiskAdjustment"] = opsi_kategori_rs_default
        nilai_unik["County"] = opsi_kabupaten_default
        return nilai_unik
    
    kunci_saat_ini = None
    daftar_nilai = []
    try:
        with open(UNIQUE_VALUES_PATH, "r", encoding="utf-8") as f:
            for baris in f:
                baris = baris.strip()
                if baris.startswith("--- ") and baris.endswith(" ---"):
                    if kunci_saat_ini and daftar_nilai:
                        nilai_unik[kunci_saat_ini] = sorted(list(set(daftar_nilai)))
                    kunci_saat_ini = baris.split(" (")[0].replace("--- ", "").strip()
                    daftar_nilai = []
                elif baris and not baris.startswith("===") and not baris.startswith("Unique values") and kunci_saat_ini:
                    if "truncated" not in baris:
                         daftar_nilai.append(baris)
            if kunci_saat_ini and daftar_nilai:
                nilai_unik[kunci_saat_ini] = sorted(list(set(daftar_nilai)))
    except Exception as e:
        st.error(f"Gagal membaca 		{UNIQUE_VALUES_PATH}		: {e}. Menggunakan opsi dropdown default.")
        nilai_unik["Infections_Predicted"] = opsi_prediksi_infeksi_default
        nilai_unik["Hospital_Category_RiskAdjustment"] = opsi_kategori_rs_default
        nilai_unik["County"] = opsi_kabupaten_default
        return nilai_unik
        
    kunci_yang_diharapkan = ["Infections_Predicted", "Hospital_Category_RiskAdjustment", "County"]
    for kunci in kunci_yang_diharapkan:
        if kunci not in nilai_unik or not nilai_unik[kunci]:
            st.warning(f"Kunci 		{kunci}		 hilang atau kosong di 		{UNIQUE_VALUES_PATH}		. Menggunakan nilai default untuk dropdown ini.")
            if kunci == "Infections_Predicted": nilai_unik[kunci] = opsi_prediksi_infeksi_default
            elif kunci == "Hospital_Category_RiskAdjustment": nilai_unik[kunci] = opsi_kategori_rs_default
            elif kunci == "County": nilai_unik[kunci] = opsi_kabupaten_default
            else: nilai_unik[kunci] = ["Tidak Diketahui"]
    return nilai_unik

@st.cache_data
def muat_data_untuk_slider(path_data=COMBINED_DATA_PATH):
    rentang_slider = {
        "Patient_Days": (0.0, 200000.0, 5000.0),
        "SIR": (0.0, 10.0, 1.0)
    }
    if not os.path.exists(path_data):
        st.warning(f"File data untuk rentang slider 		{path_data}		 tidak ditemukan. Slider akan menggunakan rentang default.")
        return rentang_slider
    try:
        df = pd.read_csv(path_data, low_memory=False)
        fitur_statistik = ["Patient_Days", "SIR"]
        df_bersih = df.dropna(subset=fitur_statistik).copy()

        if "Patient_Days" in df_bersih.columns and pd.api.types.is_numeric_dtype(df_bersih["Patient_Days"]) and not df_bersih["Patient_Days"].empty:
            df_bersih.loc[:, "Patient_Days"] = pd.to_numeric(df_bersih["Patient_Days"], errors='coerce') # FIXED: errors=	coerce	 to errors='coerce'
            df_bersih.dropna(subset=["Patient_Days"], inplace=True)
            if not df_bersih["Patient_Days"].empty:
                rentang_slider["Patient_Days"] = (
                    float(df_bersih["Patient_Days"].min()), 
                    float(df_bersih["Patient_Days"].max()),
                    float(df_bersih["Patient_Days"].median())
                )
        if "SIR" in df_bersih.columns and pd.api.types.is_numeric_dtype(df_bersih["SIR"]) and not df_bersih["SIR"].empty:
            df_bersih.loc[:, "SIR"] = pd.to_numeric(df_bersih["SIR"], errors='coerce') # FIXED: errors=	coerce	 to errors='coerce'
            df_bersih.dropna(subset=["SIR"], inplace=True)
            if not df_bersih["SIR"].empty:
                 rentang_slider["SIR"] = (
                    float(df_bersih["SIR"].min()), 
                    float(df_bersih["SIR"].max()),
                    float(df_bersih["SIR"].median())
                )
    except Exception as e:
        st.warning(f"Gagal memproses 		{path_data}		 untuk rentang slider: {e}. Menggunakan rentang default.")
    return rentang_slider

@st.cache_data
def muat_data_analisis(path_data=COMBINED_DATA_PATH):
    if not os.path.exists(path_data):
        st.error(f"File data 		{path_data}		 tidak ditemukan untuk analisis.")
        return pd.DataFrame() # Kembalikan DataFrame kosong jika file tidak ada
    try:
        df = pd.read_csv(path_data, low_memory=False)
        # Pembersihan dasar untuk analisis (bisa disesuaikan)
        kolom_numerik_penting = ["Patient_Days", "SIR", "Infections", "Infections_Predicted"]
        for kol in kolom_numerik_penting:
            if kol in df.columns:
                df[kol] = pd.to_numeric(df[kol], errors='coerce') # FIXED: errors=	coerce	 to errors='coerce'
        return df
    except Exception as e:
        st.error(f"Gagal memuat atau memproses data untuk analisis: {e}")
        return pd.DataFrame()

# --- Inisialisasi --- 
model = muat_model()
nilai_unik_input = muat_nilai_unik()
rentang_slider_input = muat_data_untuk_slider()
df_analisis = muat_data_analisis()

# --- Tampilan Aplikasi dengan Tab ---
st.title("🔬 Prediktor dan Analisis Risiko Infeksi MRSA")

tab_prediksi, tab_analisis_data = st.tabs(["Prediksi Risiko Infeksi", "Analisis Data Eksploratif"])

# --- Tab Prediksi Risiko Infeksi ---
with tab_prediksi:
    st.header("Prediksi Risiko Infeksi MRSA")
    st.markdown("""
    Aplikasi ini memprediksi kemungkinan sebuah rumah sakit memiliki tingkat infeksi bloodstream Methicillin-resistant Staphylococcus aureus (MRSA) 
    yang lebih buruk (	Worse	) dibandingkan dengan standar nasional. Masukkan informasi rumah sakit di bawah ini untuk mendapatkan prediksi.
    """)

    with st.form("form_prediksi"):
        st.subheader("Data Rumah Sakit dan Pasien")
        kol1, kol2 = st.columns(2)

        with kol1:
            patient_days = st.number_input(
                "Jumlah Hari Pasien Dirawat (Total hari pasien di rumah sakit)", 
                min_value=rentang_slider_input["Patient_Days"][0],
                max_value=rentang_slider_input["Patient_Days"][1],
                value=rentang_slider_input["Patient_Days"][2], 
                step=100.0, 
                help="Masukkan total hari rawat pasien untuk fasilitas tersebut."
            )
            with st.expander("Mengapa Jumlah Hari Pasien Dirawat Penting?"):
                st.markdown("""
                Total akumulasi jumlah hari semua pasien dirawat. Ini mencerminkan volume layanan dan durasi paparan pasien terhadap lingkungan rumah sakit. 
                Semakin tinggi, semakin besar potensi paparan terhadap patogen. Model menggunakan ini untuk menilai skala operasi dan potensi risiko.
                """)

            opsi_prediksi_infeksi = nilai_unik_input.get("Infections_Predicted", ["0.0"])
            indeks_ip_default = 0
            if opsi_prediksi_infeksi:
                default_umum_ip = [val for val in ["0.0", "1.0", "2.0"] if val in opsi_prediksi_infeksi]
                if default_umum_ip:
                    indeks_ip_default = opsi_prediksi_infeksi.index(default_umum_ip[0])
            
            infections_predicted = st.selectbox(
                "Jumlah Infeksi yang Diprediksi (oleh model NHSN)", 
                options=opsi_prediksi_infeksi,
                index=indeks_ip_default,
                help="Pilih jumlah infeksi yang diprediksi oleh model NHSN untuk fasilitas tersebut."
            )
            with st.expander("Mengapa Jumlah Infeksi yang Diprediksi Penting?"):
                st.markdown("""
                Estimasi jumlah infeksi MRSA yang diharapkan, berdasarkan model standar (misal NHSN). Ini menjadi dasar perbandingan. 
                Jika infeksi aktual jauh melebihi prediksi ini, ini indikasi kuat kinerja pengendalian infeksi mungkin lebih buruk.
                """)

        with kol2:
            sir_val = st.number_input(
                "Rasio Infeksi Terstandarisasi (SIR)", 
                min_value=rentang_slider_input["SIR"][0],
                max_value=rentang_slider_input["SIR"][1],
                value=rentang_slider_input["SIR"][2],
                step=0.01,
                help="Masukkan nilai SIR. SIR membandingkan infeksi aktual dengan prediksi (Aktual/Prediksi)."
            )
            with st.expander("Mengapa SIR Penting?"):
                st.markdown("""
                Metrik standar: (Infeksi Aktual) / (Infeksi Diprediksi). SIR > 1 berarti lebih banyak infeksi dari prediksi. 
                Ini adalah salah satu prediktor paling langsung dan kuat untuk risiko yang lebih buruk.
                """)

            opsi_kabupaten = nilai_unik_input.get("County", ["Tidak Diketahui"])
            indeks_kabupaten_default = 0
            if opsi_kabupaten and "Alameda" in opsi_kabupaten:
                indeks_kabupaten_default = opsi_kabupaten.index("Alameda")
            
            county = st.selectbox(
                "Kabupaten/Wilayah", 
                options=opsi_kabupaten,
                index=indeks_kabupaten_default,
                help="Pilih kabupaten tempat rumah sakit berada."
            )
            with st.expander("Mengapa Kabupaten/Wilayah Penting?"):
                st.markdown("""
                Lokasi geografis dapat menjadi proxy untuk faktor tak terukur: prevalensi MRSA di komunitas, faktor sosioekonomi, 
                praktik pengendalian infeksi regional, atau pola rujukan pasien.
                """)

        opsi_kategori_rs = nilai_unik_input.get("Hospital_Category_RiskAdjustment", ["Tidak Diketahui"])
        indeks_hc_default = 0
        if opsi_kategori_rs and "RUMAH SAKIT PERAWATAN AKUT UMUM" in opsi_kategori_rs:
            indeks_hc_default = opsi_kategori_rs.index("RUMAH SAKIT PERAWATAN AKUT UMUM")
            
        hospital_category = st.selectbox(
            "Kategori Rumah Sakit (untuk Penyesuaian Risiko)", 
            options=opsi_kategori_rs,
            index=indeks_hc_default,
            help="Pilih kategori penyesuaian risiko rumah sakit.",
            key="kategori_rs"
        )
        with st.expander("Mengapa Kategori Rumah Sakit Penting?"):
            st.markdown("""
            Jenis layanan dan kompleksitas pasien (misal, RS Umum, RS Anak) memengaruhi risiko inheren infeksi. 
            Ini memungkinkan model menyesuaikan ekspektasi risiko berdasarkan tipe fasilitas.
            """)

        tombol_submit = st.form_submit_button(label="Dapatkan Prediksi")

    if tombol_submit and model:
        data_input = pd.DataFrame({
            "Patient_Days": [patient_days],
            "Infections_Predicted": [str(infections_predicted)], 
            "Hospital_Category_RiskAdjustment": [hospital_category],
            "County": [county],
            "SIR": [sir_val]
        })
        
        st.subheader("Hasil Prediksi")
        try:
            prediksi = model.predict(data_input)[0]
            prediksi_proba = model.predict_proba(data_input)[0]
            
            if prediksi == 1:
                st.error("Prediksi: Rumah sakit berisiko memiliki tingkat infeksi MRSA yang LEBIH BURUK.", icon="🚨")
            else:
                st.success("Prediksi: Rumah sakit TIDAK berisiko memiliki tingkat infeksi MRSA yang LEBIH BURUK.", icon="✅")
            
            st.write(f"Probabilitas Tingkat Lebih Buruk: {prediksi_proba[1]:.2%}")
            st.write(f"Probabilitas Tingkat Tidak Lebih Buruk: {prediksi_proba[0]:.2%}")
            
            st.markdown("---")
            st.markdown("**Memahami Prediksi:**")
            st.markdown(""" 
            - **Tingkat Lebih Buruk:** Menunjukkan bahwa jumlah infeksi bloodstream MRSA yang diamati secara statistik signifikan lebih tinggi daripada jumlah infeksi yang diprediksi berdasarkan data nasional dan karakteristik fasilitas.
            - **Tingkat Tidak Lebih Buruk:** Menunjukkan bahwa tingkat MRSA BSI yang diamati serupa atau lebih baik dari yang diprediksi.
            
            Prediksi ini didasarkan pada model machine learning Gradient Boosting yang dilatih pada data historis dari rumah sakit di California. 
            Ini harus digunakan sebagai alat pendukung dan bukan sebagai diagnosis atau penilaian definitif.
            """)
            
            with st.expander("Lihat Data Input untuk Prediksi Ini"):
                st.dataframe(data_input)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")

    elif tombol_submit and not model:
        st.error("Model tidak dimuat. Tidak dapat membuat prediksi.")

# --- Tab Analisis Data Eksploratif ---
with tab_analisis_data:
    st.header("Analisis Data Eksploratif Infeksi MRSA")

    if df_analisis.empty:
        st.warning("Data untuk analisis tidak tersedia. Silakan periksa path file data.")
    else:
        st.markdown("Berikut adalah beberapa visualisasi interaktif dari dataset infeksi MRSA.")

        # Visualisasi 1: Distribusi SIR
        st.subheader("Distribusi Rasio Infeksi Terstandarisasi (SIR)")
        if "SIR" in df_analisis.columns and not df_analisis["SIR"].dropna().empty:
            fig_sir_dist = px.histogram(df_analisis.dropna(subset=["SIR"]), x="SIR", nbins=50, 
                                        title="Distribusi SIR di Seluruh Rumah Sakit",
                                        labels={"SIR":"Rasio Infeksi Terstandarisasi"})
            fig_sir_dist.update_layout(bargap=0.1)
            st.plotly_chart(fig_sir_dist, use_container_width=True)
            st.markdown("""
            Visualisasi ini menunjukkan sebaran nilai SIR. Nilai SIR di sekitar 1.0 menunjukkan kinerja sesuai prediksi. 
            Nilai yang jauh lebih tinggi dari 1.0 menunjukkan lebih banyak infeksi dari yang diharapkan.
            """)
        else:
            st.info("Data SIR tidak cukup untuk ditampilkan.")

        # Visualisasi 2: Jumlah Hari Pasien vs. SIR berdasarkan Kategori RS
        st.subheader("Jumlah Hari Pasien vs. SIR berdasarkan Kategori Rumah Sakit")
        required_cols_scatter = ["Patient_Days", "SIR", "Hospital_Category_RiskAdjustment"]
        if all(k in df_analisis.columns for k in required_cols_scatter) and not df_analisis.dropna(subset=required_cols_scatter).empty:
            df_sample_scatter = df_analisis.dropna(subset=required_cols_scatter)
            if len(df_sample_scatter) > 2000: # Sample jika data terlalu besar untuk performa browser
                df_sample_scatter = df_sample_scatter.sample(n=2000, random_state=1)

            fig_patient_days_sir = px.scatter(
                df_sample_scatter, 
                x="Patient_Days", 
                y="SIR", 
                color="Hospital_Category_RiskAdjustment",
                hover_name="Facility_Name" if "Facility_Name" in df_sample_scatter.columns else None,
                title="Jumlah Hari Pasien vs. SIR (Warna berdasarkan Kategori RS)",
                labels={"Patient_Days":"Jumlah Hari Pasien Dirawat", "SIR":"Rasio Infeksi Terstandarisasi", "Hospital_Category_RiskAdjustment":"Kategori RS"},
                size="Infections" if "Infections" in df_sample_scatter.columns else None, # Ukuran berdasarkan jumlah infeksi aktual
                marginal_y="violin",
                marginal_x="box"
            )
            st.plotly_chart(fig_patient_days_sir, use_container_width=True)
            st.markdown("""
            Scatter plot ini menunjukkan hubungan antara total hari pasien dirawat dan SIR, dengan warna yang membedakan kategori rumah sakit. 
            Ukuran titik (jika ada) dapat merepresentasikan jumlah infeksi aktual. Ini membantu melihat apakah ada pola tertentu 
            antara skala rumah sakit, jenisnya, dan rasio infeksinya.
            """)
        else:
            st.info("Data Jumlah Hari Pasien, SIR, atau Kategori RS tidak cukup untuk scatter plot.")

        # Visualisasi 3: Rata-rata SIR per Kabupaten (Top N)
        st.subheader("Rata-rata SIR per Kabupaten/Wilayah")
        required_cols_bar = ["County", "SIR"]
        if all(k in df_analisis.columns for k in required_cols_bar) and not df_analisis.dropna(subset=required_cols_bar).empty:
            avg_sir_county = df_analisis.dropna(subset=required_cols_bar).groupby("County")["SIR"].mean().sort_values(ascending=False).reset_index()
            
            jumlah_kabupaten_tampil = st.slider("Pilih Jumlah Kabupaten untuk Ditampilkan:", min_value=5, max_value=min(30, len(avg_sir_county)), value=10, key="slider_kabupaten")
            
            fig_avg_sir_county = px.bar(avg_sir_county.head(jumlah_kabupaten_tampil), x="County", y="SIR", 
                                        title=f"Top {jumlah_kabupaten_tampil} Kabupaten dengan Rata-rata SIR Tertinggi",
                                        labels={"County":"Kabupaten/Wilayah", "SIR":"Rata-rata SIR"},
                                        color="SIR", color_continuous_scale=px.colors.sequential.Reds)
            st.plotly_chart(fig_avg_sir_county, use_container_width=True)
            st.markdown("""
            Grafik batang ini menampilkan kabupaten/wilayah dengan rata-rata SIR tertinggi. Ini dapat membantu mengidentifikasi 
            area geografis yang mungkin memerlukan perhatian lebih dalam pengendalian infeksi MRSA.
            """)
        else:
            st.info("Data Kabupaten atau SIR tidak cukup untuk ditampilkan.")
        
        # Visualisasi 4: Jumlah Infeksi Aktual vs Prediksi
        st.subheader("Perbandingan Jumlah Infeksi Aktual vs. Prediksi")
        required_cols_actual_pred = ["Infections", "Infections_Predicted"]
        if all(k in df_analisis.columns for k in required_cols_actual_pred) and not df_analisis.dropna(subset=required_cols_actual_pred).empty:
            df_sample_inf = df_analisis.dropna(subset=required_cols_actual_pred)
            if len(df_sample_inf) > 2000:
                df_sample_inf = df_sample_inf.sample(n=2000, random_state=1)

            fig_actual_vs_predicted = px.scatter(
                df_sample_inf, 
                x="Infections_Predicted", 
                y="Infections", 
                trendline="ols", # Ordinary Least Squares regression line
                hover_name="Facility_Name" if "Facility_Name" in df_sample_inf.columns else None,
                title="Infeksi Aktual vs. Infeksi Diprediksi",
                labels={"Infections_Predicted":"Jumlah Infeksi Diprediksi", "Infections":"Jumlah Infeksi Aktual"}
            )
            # Ensure min/max are valid before drawing the reference line
            min_val_ref = df_sample_inf["Infections_Predicted"].min()
            max_val_ref = df_sample_inf["Infections_Predicted"].max()
            if pd.notna(min_val_ref) and pd.notna(max_val_ref) and min_val_ref <= max_val_ref:
                fig_actual_vs_predicted.add_shape( 
                    type=	line	, line=dict(dash=	dash	, color="grey"),
                    x0=min_val_ref, y0=min_val_ref, 
                    x1=max_val_ref, y1=max_val_ref
                )
            st.plotly_chart(fig_actual_vs_predicted, use_container_width=True)
            st.markdown("""
            Scatter plot ini membandingkan jumlah infeksi yang diprediksi dengan jumlah infeksi aktual yang dilaporkan. 
            Titik-titik di atas garis referensi (y=x, abu-abu putus-putus) menunjukkan rumah sakit dengan infeksi aktual lebih banyak dari prediksi. 
            Garis tren (OLS) menunjukkan hubungan umum antara keduanya.
            """)
        else:
            st.info("Data Infeksi Aktual atau Infeksi Diprediksi tidak cukup untuk ditampilkan.")

# --- Footer ---
st.markdown("---")
st.markdown("Dikembangkan oleh Manus AI untuk tujuan demonstrasi.")
st.markdown("Sumber Dataset: Portal Data Terbuka California Health and Human Services (Data MRSA BSI)")


