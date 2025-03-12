import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff

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

    # Pilih rentang tanggal
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df.set_index("date", inplace=True)
    min_date = df.index.min().date()
    max_date = df.index.max().date()
    start_date, end_date = st.slider("Pilih Rentang Tanggal", min_value=min_date, max_value=max_date, value=(min_date, max_date))

    # Filter data berdasarkan rentang tanggal
    filtered_df = df.loc[start_date:end_date]

    # Resampling data
    daily_rentals = filtered_df["total_rentals"].resample("D").mean()
    monthly_rentals = filtered_df["total_rentals"].resample("M").mean()

    # 🔍 Debugging: Cek jumlah data setelah filter
    st.write("Jumlah data setelah filter:", filtered_df.shape[0])

    # Plot menggunakan matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))

    # Garis tren harian
    daily_rentals.plot(ax=ax, label="Daily", color="blue")

    # Garis tren bulanan (putus-putus)
    monthly_rentals.plot(ax=ax, label="Monthly", linestyle="dashed", color="orange")
    ax.set_title("Bike Rentals Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Rentals")
    ax.legend()

    # Tampilkan di Streamlit
    st.pyplot(fig)
    
    # 👥 **Visualisasi Tren Casual vs Registered Users**
    st.subheader("👥 Tren Penyewaan Casual vs Registered Users")

    # Resampling data
    daily_casual = filtered_df["casual_rentals"].resample("D").mean()
    daily_registered = filtered_df["registered_rentals"].resample("D").mean()

    # Plot menggunakan Matplotlib    
    fig, ax = plt.subplots(figsize=(12, 6))

    # Garis tren casual_rentals (biru)
    daily_casual.plot(ax=ax, label="Daily Casual User Trend", color="blue")

    # Garis tren registered_rentals (oranye, putus-putus)
    daily_registered.plot(ax=ax, label="Daily Registered User Trend", linestyle="dashed", color="orange")

    ax.set_title("Bike Rentals Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Rentals")
    ax.legend()

    # Tampilkan di Streamlit
    st.pyplot(fig)

    # 📅 **Visualisasi Perbandingan Penyewaan Sepeda: Weekday vs Weekend**
    st.subheader("📅 Perbandingan Penyewaan Sepeda: Weekday vs Weekend")

    # Grupkan total rental berdasarkan jenis hari (Weekday/Weekend)
    day_type_rentals = df.groupby("day_type")[["casual_rentals", "registered_rentals"]].sum().reset_index()

   # Buat plot interaktif dengan Plotly
    fig = px.bar(
        day_type_rentals,
        x="day_type",
        y=["casual_rentals", "registered_rentals"],
        labels={"value": "Total Rentals", "day_type": "Day Type"},
        barmode="group",
        text_auto=True,  # Menampilkan angka di atas bar
        color_discrete_map={"casual": "yellow", "registered": "blue"}
    )

    fig.update_layout(
        xaxis_title="Day Type",
        yaxis_title="Total Rentals",
        yaxis_tickformat=",",  # Format angka agar lebih readable
        legend_title="User Type"
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig)
    
    if not df.empty:
        # Pilih hanya kolom numerik
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns

        if len(num_cols) > 1:  # Pastikan ada lebih dari 1 kolom numerik untuk korelasi
            # Hitung korelasi
            corr_matrix = df[num_cols].corr()

            # Buat heatmap dengan Plotly
            fig = ff.create_annotated_heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns.tolist(),
                y=corr_matrix.index.tolist(),
                colorscale="Viridis",
                annotation_text=corr_matrix.round(2).values,
                showscale=True
            )

            # Tambahkan judul
            fig.update_layout(title="Matriks Korelasi Variabel Numerik", width=800, height=600)

            # Tampilkan di Streamlit
            st.plotly_chart(fig)
        else:
            st.warning("Tidak ada cukup kolom numerik untuk membuat korelasi.")
    else:
        st.error("DataFrame kosong! Pastikan dataset sudah dimuat.")

        
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
