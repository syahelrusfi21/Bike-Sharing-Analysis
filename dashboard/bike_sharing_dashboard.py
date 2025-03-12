import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load Dataset
def load_data():
    df = pd.read_csv("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/raw/main/dashboard/bike_(preprocessed)_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["dayofweek"] = df["date"].dt.dayofweek
    df["day_type"] = df["dayofweek"].apply(lambda x: "Weekday" if x < 5 else "Weekend")
    return df

df = load_data()

# Sidebar - Menu Navigasi
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Pilih Halaman", ["🏠 Home", "📊 Dashboard", "📈 Insight"])

# **1️⃣ HOME PAGE**
if menu == "🏠 Home":
    st.title("🚴 Selamat Datang di Dashboard Bike Sharing System!")
    st.write(
        """
    Sistem berbagi sepeda (Bike Sharing System) adalah inovasi penyewaan sepeda yang otomatis, memungkinkan pengguna menyewa di satu lokasi dan mengembalikannya di lokasi lain. 
    Sistem ini penting untuk mengatasi masalah lalu lintas, lingkungan, dan kesehatan. Analisis didasarkan pada dataset Bike Sharing yang diunggah oleh Lakshmipathi N pada website kaggle.
         
    Link ke dataset: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset
             
    🔹 **Objektif analisis ini ingin mengetahui**:  
    - Apakah ada pola musiman dalam penyewaan sepeda?
    - Bagaimana tren penyewaan dari waktu ke waktu?  
    - Bagaimana tren penyewaan sepeda untuk untuk pengguna biasa (casual) dan terdaftar (registered)? Apakah ada perbedaan?  
    - Apakah kondisi lingkungan seperti suhu, kelembapan, dsb berpengaruh terhadap penyewa sepeda?  
        """
    )

# **2️⃣ DASHBOARD PAGE**
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard Penyewaan Sepeda")

    # 📈 **Visualisasi Tren Penyewaan Sepeda**
    st.subheader("📈 Tren Penyewaan Sepeda")

    # Konversi format tanggal
    df["date"] = pd.to_datetime(df["date"], errors='coerce')

    # Hapus data NaN
    df = df.dropna(subset=["date", "total_rentals"])

    # Pilih rentang tanggal
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    start_date, end_date = st.slider("Pilih Rentang Tanggal", min_value=min_date, max_value=max_date, value=(min_date, max_date))

    # Filter data berdasarkan rentang tanggal
    filtered_df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

    # Buat agregasi bulanan
    df["month"] = df["date"].dt.to_period("M")
    monthly_df = df.groupby("month")["total_rentals"].mean().reset_index()
    monthly_df["month"] = monthly_df["month"].astype(str)

    # 🔍 Debugging: Cek jumlah data setelah filter
    st.write("Jumlah data setelah filter:", filtered_df.shape[0])

    # Plot menggunakan matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))
        
    # Garis tren harian
    sns.lineplot(data=filtered_df, x="date", y="total_rentals", ax=ax, label="Daily", color="blue")

    # Garis tren bulanan (putus-putus)
    sns.lineplot(data=monthly_df, x="month", y="total_rentals", ax=ax, label="Monthly", color="orange", linestyle="dashed")
    ax.set_title("Bike Rentals Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Rentals")
    ax.legend()

    # Tampilkan di Streamlit
    st.pyplot(fig)
        
# # **2️⃣ DASHBOARD PAGE**
# elif menu == "📊 Dashboard":
#     st.title("📊 Dashboard Penyewaan Sepeda")
    
#     # 📈 **Visualisasi Tren Penyewaan (Harian & Bulanan)**
#     st.subheader("📈 Tren Penyewaan Sepeda")
    
#     # Load gambar
#     st.image("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/raw/main/dashboard/trend_bike_rentals.png")

#     # 👥 **Perbandingan Pengguna Terdaftar vs Biasa**
#     st.subheader("👥 Perbandingan Pengguna Terdaftar vs Biasa")

#     # Load gambar
#     st.image("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/raw/main/dashboard/user_trend.png")

#     # 🌤️ **Pengaruh Lingkungan terhadap Penyewaan**
#     st.subheader("🌤️ Pengaruh Faktor Lingkungan terhadap Jumlah Penyewa")
    
#     # Load gambar
#     st.image("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/raw/main/dashboard/environmental_condition.png")
    
#     # 📅 **Weekday vs Weekend**
#     st.subheader("📅 Weekday vs Weekend")

#     # Load gambar
#     st.image("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/raw/main/dashboard/weekday_vs_weekend.png")

# **3️⃣ INSIGHT PAGE**
elif menu == "📈 Insight":
    st.title("📈 Insight Penyewaan Sepeda")
    
    st.subheader("1️⃣ Tren Musiman Penyewaan")
    st.write(
        """
        - Penyewaan sepeda meningkat tajam pada **Maret–Juli** dan menurun pada **Oktober–Januari**.
        - Layanan ini semakin populer dari tahun ke tahun, dengan peningkatan jumlah penyewaan dari 2011 ke 2012.

        ✅ **Rekomendasi:**  
        - Optimalkan kapasitas sepeda di bulan puncak.  
        - Terapkan strategi pemasaran kreatif untuk meningkatkan penyewaan di musim sepi.  
        - Pertimbangkan ekspansi ke wilayah baru yang ramah sepeda.
        """
    )

    st.subheader("2️⃣ Perbandingan Pengguna: Terdaftar vs Biasa")
    st.write(
        """
        - Pengguna **terdaftar** mendominasi penyewaan dibandingkan pengguna biasa.  
        - Terdapat tren peningkatan jumlah pelanggan tetap.

        ✅ **Rekomendasi:**  
        - Dorong pengguna biasa untuk berlangganan melalui promosi.  
        - Tingkatkan retensi pelanggan tetap dengan fitur personal seperti **rekomendasi rute** dan **paket langganan fleksibel**.
        """
    )

    st.subheader("3️⃣ Pengaruh Lingkungan")
    st.write(
        """
        - Faktor lingkungan seperti suhu, kelembapan, kecepatan angin, dsb, memiliki pengaruh terhadap penyewaan, tetapi dampaknya relatif kecil.  
        
        ✅ **Rekomendasi:**  
        - Fokus pada strategi non-lingkungan seperti **promosi** dan **ketersediaan sepeda**.  
        - Manfaatkan informasi cuaca untuk meningkatkan pengalaman pengguna, misalnya dengan memberikan notifikasi cuaca buruk.
        """
    )

    st.subheader("4️⃣ Pola Penyewaan: Weekday vs Weekend")
    st.write(
        """
        - Penyewaan lebih tinggi pada **weekday**, terutama oleh pengguna terdaftar yang kemungkinan besar menggunakan sepeda untuk transportasi harian.
        - Pengguna biasa lebih sering menyewa di akhir pekan untuk rekreasi.

        ✅ **Rekomendasi:**  
        - Buat program langganan untuk pengguna **terdaftar** dengan harga khusus.  
        - Berikan promo menarik bagi pengguna **biasa** di akhir pekan.
        """
    )
