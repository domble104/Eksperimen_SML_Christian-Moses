import pandas as pd
import os

# ==========================================
# KONFIGURASI PATH
# ==========================================
# Gunakan path relatif lokal sesuai struktur folder tugas
# Pastikan file csv sudah Anda download dan taruh di folder 'online_retail_II_raw'
INPUT_PATH = "D:\\KULIAH\\STUPEN\\AKHIRR\\Eksperimen_SML_Christian Moses\\online_retail_II_raw.csv"
OUTPUT_PATH = "online_retail_II_preprocessing/data_clean.csv"

def load_data(path):
    print("1. Loading Data...")
    try:
        # Coba encoding umum. Jika error, ganti 'ISO-8859-1' atau 'cp1252'
        df = pd.read_csv(path, encoding='ISO-8859-1')
        print(f"   Data loaded. Shape awal: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"   [ERROR] File tidak ditemukan di: {path}")
        return None

def clean_data(df):
    print("2. Cleaning Data...")
    
    # Copy agar tidak merusak data asli di memori
    df = df.copy()

    # --- Logika Pembersihan Anda ---
    
    # 1. Handling Missing Values pada Customer ID
    # Catatan: Cek apakah nama kolom di CSV 'Customer ID' (pakai spasi) atau 'CustomerID'
    # Kode di bawah mengasumsikan pakai spasi sesuai kode asli Anda
    if 'Customer ID' in df.columns:
        df = df.dropna(subset=["Customer ID"])
    elif 'CustomerID' in df.columns:
        df = df.dropna(subset=["CustomerID"])
    
    # 2. Hapus Transaksi Cancel (Invoice diawali 'C')
    # Pastikan kolom Invoice string
    df["Invoice"] = df["Invoice"].astype(str)
    mask_cancel = df["Invoice"].str.startswith("C")
    df = df[~mask_cancel]
    
    # 3. Hapus Duplikat
    df = df.drop_duplicates(keep="first")
    
    # 4. Konversi Tipe Data
    # Mengonversi Quantity dan Price ke numerik, error jadi NaN
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    
    # Hapus baris yang gagal dikonversi (NaN)
    df = df.dropna(subset=["Quantity", "Price"])
    
    # 5. Buat Total Amount & Filter Positif
    df["Total Amount"] = df["Quantity"] * df["Price"]
    df = df[df["Total Amount"] > 0]

    # 6. Konversi Tanggal (Penting untuk Time Series/RFM nanti)
    if 'InvoiceDate' in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    print(f"   Shape setelah cleaning: {df.shape}")
    return df

def main():
    # Jalankan Fungsi Load
    df = load_data(INPUT_PATH)
    
    if df is not None:
        # Jalankan Fungsi Clean
        df_clean = clean_data(df)
        
        # Jalankan Fungsi Save
        # Buat folder output jika belum ada
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        
        df_clean.to_csv(OUTPUT_PATH, index=False)
        print(f"3. Sukses! Data bersih disimpan di: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()