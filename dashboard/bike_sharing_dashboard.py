import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
import os

# Load Dataset
#@st.cache_data
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
    
    # 📈 **Visualisasi Tren Penyewaan (Harian & Bulanan)**
    st.subheader("📈 Tren Penyewaan Sepeda")
    
    # Load gambar
    #image_path = os.path.join("trend_bike_rentals.png")
    #image = Image.open(image_path)
    image = Image.open("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/blob/main/dashboard/trend_bike_rentals.png")

    # Tampilkan di Streamlit
    st.image(image, caption="Tren Penyewaan Sepeda Sepanjang Waktu", use_container_width=True)

    # 👥 **Perbandingan Pengguna Terdaftar vs Biasa**
    st.subheader("👥 Perbandingan Pengguna Terdaftar vs Biasa")

    # Load gambar
    #image_path = os.path.join("user_trend.png")
    #image = Image.open(image_path)
    image = Image.open("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/blob/main/dashboard/user_trend.png")

    # Tampilkan di Streamlit
    st.image(image, caption="Tren Pengguna Terdaftar vs Biasa", use_container_width=True)

    # 🌤️ **Pengaruh Lingkungan terhadap Penyewaan**
    st.subheader("🌤️ Pengaruh Faktor Lingkungan terhadap Jumlah Penyewa")
    
    # Load gambar
    #image_path = os.path.join("visualization_img", "environmental_condition.png")
    #image = Image.open(image_path)
    image = Image.open("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/blob/main/dashboard/environmental_condition.png")

    # Tampilkan di Streamlit
    st.image(image, caption="Korelasi beberapa faktor lingkungan terhadap total_rentals", use_container_width=True)
    
    # 📅 **Weekday vs Weekend**
    st.subheader("📅 Weekday vs Weekend")

    # Load gambar
    #image_path = os.path.join("visualization_img", "weekday_vs_weekend.png")
    #image = Image.open(image_path)
    image = Image.open("https://github.com/syahelrusfi21/Bike-Sharing-Analysis/blob/main/dashboard/weekday_vs_weekend.png")

    # Tampilkan di Streamlit
    st.image(image, caption="Perbandingan total penyewa sepeda pada weekday dan weekend", use_container_width=True)
    
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
