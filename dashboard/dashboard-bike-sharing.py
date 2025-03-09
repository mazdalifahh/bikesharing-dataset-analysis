import streamlit as st  # Streamlit untuk membuat aplikasi web interaktif dengan Python
import pandas as pd  # Pandas untuk manipulasi dan analisis data
import numpy as np  # NumPy untuk komputasi numerik dan array multidimensi
import matplotlib.pyplot as plt  # Matplotlib untuk membuat visualisasi data statis
import seaborn as sns  # Seaborn untuk visualisasi data yang lebih menarik dan kompleks
import plotly.express as px  # Plotly untuk visualisasi interaktif dan grafik kompleks

# Load Data
df_main = pd.read_csv("dashboard/main_data.csv")

# Convert dteday to datetime
df_main['dteday'] = pd.to_datetime(df_main['dteday'])
df_main['month'] = df_main['dteday'].dt.month
df_main['year'] = df_main['dteday'].dt.year
df_main['weekday'] = df_main['dteday'].dt.weekday

# Mapping season & weather labels
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_main['season_name'] = df_main['season'].map(season_map)
weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
df_main['weather_desc'] = df_main['weathersit'].map(weather_map)

df_main['usage_category'] = pd.cut(df_main['cnt'], bins=[0, 2000, 4000, 8000], labels=['Low', 'Medium', 'High'])

# Streamlit Dashboard
st.title("🚴‍♂️ Bike Sharing Data Dashboard")

# Penjelasan Singkat
st.markdown("""

**Selamat datang di dashboard Bike Sharing!**  
Dashboard ini memungkinkan Anda untuk mengeksplorasi tren penggunaan sepeda berdasarkan data peminjaman dari sistem bike sharing. Temukan pola-pola menarik, seperti:

- **Jumlah penyewaan sepeda** berdasarkan **bulan**, **hari**, dan **jam**.
- **Pengaruh cuaca** dan **musim** terhadap peminjaman sepeda.
- **Perbandingan hari kerja dan libur** dalam peminjaman sepeda.

Data ini membantu memahami bagaimana faktor-faktor seperti waktu, cuaca, dan musim memengaruhi jumlah peminjaman sepeda.
""")

# Add Pict
image_path = "dashboard/assets/Logo.png"
st.sidebar.image(image_path, use_column_width=True)

# Sidebar
st.sidebar.subheader("📌 Filter Data")
year_option = st.sidebar.selectbox("Pilih Tahun", options=df_main['year'].unique())
season_option = st.sidebar.multiselect("Pilih Musim", options=df_main['season_name'].unique(), default=list(df_main['season_name'].unique()))
weather_option = st.sidebar.multiselect("Pilih Cuaca", options=df_main['weather_desc'].unique(), default=list(df_main['weather_desc'].unique()))
usage_option = st.sidebar.multiselect("Pilih Kategori Penyewaan", options=df_main['usage_category'].unique(), default=list(df_main['usage_category'].unique()))
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [df_main['dteday'].min().date(), df_main['dteday'].max().date()])

# Filter Data
df_filtered = df_main.loc[
    (df_main['year'] == year_option) &
    (df_main['season_name'].isin(season_option)) &
    (df_main['weather_desc'].isin(weather_option)) &
    (df_main['usage_category'].isin(usage_option)) &
    (df_main['dteday'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# KPI Section
st.subheader("📊 Overview")
st.metric("Total Rentals", df_filtered['cnt'].sum())
st.metric("Average Rentals per Day", round(df_filtered['cnt'].mean(), 2))

## Tren Penyewaan Sepeda Sepanjang Tahun
st.subheader("Tren Penyewaan Sepeda Sepanjang Tahun")

# Pastikan kolom dteday sudah dalam format datetime
df_main['dteday'] = pd.to_datetime(df_main['dteday'])

# Tambahkan kolom tahun & bulan
df_main['year'] = df_main['dteday'].dt.year
df_main['month'] = df_main['dteday'].dt.month

# Plot dengan hue berdasarkan tahun
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_main, x='month', y='cnt', hue='year', marker="o")

plt.xticks(range(1, 13))  # Menampilkan angka bulan dengan benar (1-12)
plt.title("Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.grid()
st.pyplot(plt)  # Display the plot in Streamlit

## Pola Penyewaan Sepeda Berdasarkan Jam dan Hari
st.subheader("Pola Penyewaan Sepeda yang Berbeda Berdasarkan Hari dan Jam")

# Group by 'weekday' to get average count of rentals per day
daily_rentals = df_main.groupby('weekday')['cnt'].mean().reset_index()

# Plot bar chart for daily rentals
plt.figure(figsize=(10, 5))
sns.barplot(data=daily_rentals, x='weekday', y='cnt', palette="Blues_d")
plt.title('Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewa')
plt.xticks(ticks=range(7), labels=["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
plt.grid(axis='y')
st.pyplot(plt)  # Display the plot in Streamlit

# Plotkan tren penyewaan sepeda per jam
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_main, x='hr', y='cnt', marker="o")
plt.title('Pola Penyewaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewa')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(plt)  # Display the plot in Streamlit
