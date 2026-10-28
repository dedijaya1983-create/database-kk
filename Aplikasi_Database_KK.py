import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Database Kartu Keluarga", page_icon="🗂️", layout="wide")

# Nama file untuk menyimpan data secara permanen
FILE_DATA = "database_kk.csv"

# Fungsi untuk memuat data dari file lokal
def muat_data():
    if os.path.exists(FILE_DATA):
        return pd.read_csv(FILE_DATA, dtype={'No_KK': str, 'NIK': str})
    else:
        return pd.DataFrame(columns=["No_KK", "Kepala_Keluarga", "Alamat", "RT_RW", "Desa_Kelurahan", "Kecamatan", "NIK", "Nama_Anggota", "Hubungan", "Jenis_Kelamin"])

# Inisialisasi data
if 'df_kk' not in st.session_state:
    st.session_state.df_kk = muat_data()

st.title("🗂️ Aplikasi Manajemen Database Kartu Keluarga")
st.markdown("---")

# Pembagian Menu Dashboard
menu = st.sidebar.radio("Pilih Menu:", ["➕ Tambah Data KK Baru", "🔍 Cari & Cetak Digital KK", "📊 Lihat Semua Data"])

# ================= MENU 1: TAMBAH DATA =================
if menu == "➕ Tambah Data KK Baru":
    st.header("Masukkan Data Kartu Keluarga Baru")
    
    with st.form("form_kk"):
        col1, col2 = st.columns(2)
        with col1:
            no_kk = st.text_input("Nomor Kartu Keluarga (16 Digit):", max_chars=16)
            kepala_keluarga = st.text_input("Nama Lengkap Kepala Keluarga:")
            alamat = st.text_area("Alamat Rumah:")
        with col2:
            rt_rw = st.text_input("RT / RW:")
            desa = st.text_input("Desa / Kelurahan:")
            kecamatan = st.text_input("Kecamatan:")
            
        st.subheader("👨‍👩‍👧‍👦 Anggota Keluarga (Termasuk Kepala Keluarga)")
        st.info("Masukkan anggota keluarga satu per satu di bawah ini:")
        
        # Form dinamis sederhana untuk anggota keluarga
        nik = st.text_input("NIK Anggota (16 Digit):", max_chars=16)
        nama_anggota = st.text_input("Nama Lengkap Anggota:")
        hubungan = st.selectbox("Hubungan Dalam Keluarga:", ["Kepala Keluarga", "Suami", "Istri", "Anak", "Orang Tua", "Mertua", "Famili Lain"])
        jk = st.radio("Jenis Kelamin:", ["Laki-laki", "Perempuan"], horizontal=True)
        
        tombol_simpan = st.form_submit_button("Simpan Data Anggota ke KK")
        
        if tombol_simpan:
            if not no_kk or not kepala_keluarga or not nik or not nama_anggota:
                st.error("❌ Mohon isi Nomor KK, Kepala Keluarga, NIK, dan Nama Anggota terlebih dahulu!")
            else:
                data_baru = {
                    "No_KK": no_kk, "Kepala_Keluarga": kepala_keluarga, "Alamat": alamat,
                    "RT_RW": rt_rw, "Desa_Kelurahan": desa, "Kecamatan": kecamatan,
                    "NIK": nik, "Nama_Anggota": nama_anggota, "Hubungan": hubungan, "Jenis_Kelamin": jk
                }
                st.session_state.df_kk = pd.concat([st.session_state.df_kk, pd.DataFrame([data_baru])], ignore_index=True)
                st.session_state.df_kk.to_csv(FILE_DATA, index=False)
                st.success(f"✅ Data {nama_anggota} berhasil ditambahkan ke KK No. {no_kk}!")

# ================= MENU 2: CARI & CETAK =================
elif menu == "🔍 Cari & Cetak Digital KK":
    st.header("Pencarian & Cetak Digital KK")
    kata_kunci = st.text_input("Masukkan Nomor KK atau Nama Kepala Keluarga untuk dicari:")
    
    if kata_kunci:
        hasil = st.session_state.df_kk[
            (st.session_state.df_kk['No_KK'].str.contains(kata_kunci, na=False)) | 
            (st.session_state.df_kk['Kepala_Keluarga'].str.contains(kata_kunci, case=False, na=False))
        ]
        
        if not hasil.empty:
            kk_terpilih = hasil['No_KK'].iloc[0]
            detail_kk = hasil[hasil['No_KK'] == kk_terpilih]
            
            # Tampilan Dokumen KK Digital
            st.markdown(f"""
            <div style="border: 2px solid #333; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
                <h2 style="text-align: center; margin-bottom: 5px;">SALINAN KARTU KELUARGA</h2>
                <h4 style="text-align: center; margin-top: 0px;">No. {kk_terpilih}</h4>
                <table style="width:100%; border-collapse: collapse;">
                    <tr><td><b>Nama Kepala Keluarga</b></td><td>: {detail_kk['Kepala_Keluarga'].iloc[0]}</td>
                        <td><b>Kecamatan</b></td><td>: {detail_kk['Kecamatan'].iloc[0]}</td></tr>
                    <tr><td><b>Alamat</b></td><td>: {detail_kk['Alamat'].iloc[0]}</td>
                        <td><b>Desa/Kelurahan</b></td><td>: {detail_kk['Desa_Kelurahan'].iloc[0]}</td></tr>
                    <tr><td><b>RT/RW</b></td><td>: {detail_kk['RT_RW'].iloc[0]}</td>
                        <td><b>Sistem</b></td><td>: Database Lokal AI</td></tr>
                </table>
            </div>
            """, unsafe_allowed_html=True)
            
            st.write("### 👥 Daftar Anggota Keluarga")
            tabel_tampil = detail_kk[["NIK", "Nama_Anggota", "Jenis_Kelamin", "Hubungan"]].reset_index(drop=True)
            st.table(tabel_tampil)
        else:
            st.warning("⚠️ Data Kartu Keluarga tidak ditemukan.")

# ================= MENU 3: LIHAT SEMUA DATA =================
elif menu == "📊 Lihat Semua Data":
    st.header("Seluruh Isi Database Kartu Keluarga")
    if not st.session_state.df_kk.empty:
        st.dataframe(st.session_state.df_kk)
        st.caption(f"Semua data di atas tersimpan otomatis di komputer Anda pada file: `{FILE_DATA}`")
    else:
        st.info("Database masih kosong. Silakan tambah data baru terlebih dahulu.")
