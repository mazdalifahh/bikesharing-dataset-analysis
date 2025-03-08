import streamlit as st  # Streamlit untuk membuat aplikasi web interaktif dengan Python
import pandas as pd  # Pandas untuk manipulasi dan analisis data
import numpy as np  # NumPy untuk komputasi numerik dan array multidimensi
import matplotlib.pyplot as plt  # Matplotlib untuk membuat visualisasi data statis
import seaborn as sns  # Seaborn untuk visualisasi data yang lebih menarik dan kompleks
import plotly.express as px  # Plotly untuk visualisasi interaktif dan grafik kompleks

# Load Data
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")


# Convert dteday to datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day['month'] = df_day['dteday'].dt.month
df_day['year'] = df_day['dteday'].dt.year
df_day['weekday'] = df_day['dteday'].dt.weekday

df_hour['hr'] = df_hour['hr'].astype(int)

# Mapping season & weather labels
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_day['season_name'] = df_day['season'].map(season_map)
weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
df_day['weather_desc'] = df_day['weathersit'].map(weather_map)

df_day['usage_category'] = pd.cut(df_day['cnt'], bins=[0, 2000, 4000, 8000], labels=['Low', 'Medium', 'High'])

# Streamlit Dashboard
st.title("🚴‍♂️ Bike Sharing Data Dashboard")

# Penjelasan Singkat
st.markdown("""

**Selamat datang di dashboard interaktif Bike Sharing!**  
Dashboard ini memungkinkan Anda untuk mengeksplorasi tren penggunaan sepeda berdasarkan data peminjaman dari sistem bike sharing. Temukan pola-pola menarik, seperti:

- **Jumlah penyewaan sepeda** berdasarkan **bulan**, **hari**, dan **jam**.
- **Pengaruh cuaca** dan **musim** terhadap peminjaman sepeda.
- **Perbandingan hari kerja dan libur** dalam peminjaman sepeda.

Data ini membantu memahami bagaimana faktor-faktor seperti waktu, cuaca, dan musim memengaruhi jumlah peminjaman sepeda.
""")

# Sidebar Filters
st.sidebar.subheader("📌 Filter Data")
year_option = st.sidebar.selectbox("Pilih Tahun", options=df_day['year'].unique())
season_option = st.sidebar.multiselect("Pilih Musim", options=df_day['season_name'].unique(), default=df_day['season_name'].unique())
weather_option = st.sidebar.multiselect("Pilih Cuaca", options=df_day['weather_desc'].unique(), default=df_day['weather_desc'].unique())
usage_option = st.sidebar.multiselect("Pilih Kategori Penyewaan", options=df_day['usage_category'].unique(), default=df_day['usage_category'].unique())

# Filter Data
df_filtered = df_day[
    (df_day['year'] == year_option) &
    (df_day['season_name'].isin(season_option)) &
    (df_day['weather_desc'].isin(weather_option)) &
    (df_day['usage_category'].isin(usage_option))
]

# KPI Section
st.subheader("📊 Overview")
st.metric("Total Rentals", df_day['cnt'].sum())
st.metric("Average Rentals per Day", round(df_day['cnt'].mean(), 2))

# Penjelasan Tren Penyewaan per Bulan
st.subheader("📈 Untuk melihat tren per bulan 2011 vs 2012")

# Pastikan kolom dteday sudah dalam format datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Tambahkan kolom tahun & bulan
df_day['year'] = df_day['dteday'].dt.year
df_day['month'] = df_day['dteday'].dt.month

# Plot Tren Penyewaan per Bulan
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_day, x='month', y='cnt', hue='year', marker="o")

plt.xticks(range(1, 13))  # Menampilkan angka bulan dengan benar (1-12)
plt.title("Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.grid()
st.pyplot(plt)  # Menampilkan plot di Streamlit

# Line Chart - Tren Penyewaan per Jam
df_hour_avg = df_hour.groupby('hr')['cnt'].mean().reset_index()
fig4 = px.line(df_hour_avg, x='hr', y='cnt', markers=True, title='Pola Penyewaan Sepeda per Jam')
st.plotly_chart(fig4)

# Boxplot - Tren Penyewaan per Hari dalam Seminggu
fig3 = px.box(df_filtered, x='weekday', y='cnt', title='Penyewaan Sepeda Berdasarkan Hari dalam Seminggu', labels={'weekday': 'Hari', 'cnt': 'Jumlah Penyewa'})
fig3.update_xaxes(tickvals=list(range(7)), ticktext=["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
st.plotly_chart(fig3)

# Boxplot - Pengaruh Musim terhadap Penyewaan
fig5 = px.box(df_filtered, x='season_name', y='cnt', title='Pengaruh Musim terhadap Penyewaan Sepeda', color='season_name')
st.plotly_chart(fig5)

# Boxplot - Pengaruh Cuaca terhadap Penyewaan
fig6 = px.box(df_filtered, x='weather_desc', y='cnt', title='Pengaruh Cuaca terhadap Penyewaan Sepeda', color='weather_desc')
st.plotly_chart(fig6)

plt.ylabel("Jumlah Penyewaan")

# Barplot - Peminjaman Hari Kerja vs Hari Libur
fig7 = px.bar(df_filtered, x='workingday', y='cnt', title='Peminjaman Sepeda pada Hari Kerja vs Hari Libur', labels={'workingday': 'Hari', 'cnt': 'Jumlah Peminjaman'})
fig7.update_xaxes(tickvals=[0,1], ticktext=['Hari Libur', 'Hari Kerja'])
st.plotly_chart(fig7)

# Heatmap Korelasi Variabel Numerik
df_day_numeric = df_day.select_dtypes(include=[np.number])
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df_day_numeric.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)

# Barplot - Peminjaman Berdasarkan Musim
fig8 = px.bar(df_filtered, x='season_name', y='cnt', title='Peminjaman Sepeda Berdasarkan Musim', color='season_name', category_orders={'season_name': ['Spring', 'Summer', 'Fall', 'Winter']})
st.plotly_chart(fig8)

# Binning Kategori Penyewaan
st.subheader("📌 Kategori Penyewaan")
st.write(df_filtered['usage_category'].value_counts())
