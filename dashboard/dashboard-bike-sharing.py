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

df_main['season_name'] = df_main['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df_main['weather_desc'] = df_main['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'})
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

# Sidebar Date Filter
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [df_main['dteday'].min().date(), df_main['dteday'].max().date()])
df_filtered = df_main.loc[(df_main['dteday'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))]

# KPI Section
st.subheader("📊 Overview")
st.metric("Total Rentals", df_filtered['cnt'].sum())
st.metric("Average Rentals per Day", round(df_filtered['cnt'].mean(), 2))

# 1. Tren Penyewaan Sepeda Sepanjang Tahun
st.subheader("📅 Tren Penyewaan Sepeda Sepanjang Tahun")
plt.figure(figsize=(12, 5))
sns.lineplot(data=df_main, x='month', y='cnt', hue='year', marker='o', palette='coolwarm')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.title("Tren Penyewaan Sepeda Sepanjang Tahun")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.legend(title="Tahun", labels=["2011", "2012"])
plt.grid()
st.pyplot(plt)

# 2. Pola Penyewaan Berdasarkan Hari & Jam
st.subheader("⏰ Pola Penyewaan Berdasarkan Hari & Jam")
hourly_trend = df_main.groupby(['hr', 'weekday'])['cnt'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=hourly_trend, x="hr", y="cnt", hue="weekday", palette="Set1", linewidth=2.5, marker="o")
plt.axvspan(7, 9, color='gray', alpha=0.2, label="Jam Sibuk Pagi")
plt.axvspan(16, 18, color='gray', alpha=0.2, label="Jam Sibuk Sore")
plt.title("Tren Penyewaan Sepeda Berdasarkan Jam dalam Sehari untuk Setiap Hari")
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan")
plt.xticks(ticks=range(0, 24, 2))
plt.legend(title="Hari", labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.grid()
st.pyplot(plt)

# 3. Pengaruh Musim & Cuaca terhadap Penyewaan
st.subheader("🌦️ Pengaruh Musim & Cuaca terhadap Penyewaan")
plt.figure(figsize=(12, 5))
sns.boxplot(data=df_main, x='season', y='cnt', hue='season', palette='pastel', dodge=False)
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])
plt.title("Pengaruh Musim terhadap Penyewaan Sepeda")
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

plt.figure(figsize=(12, 5))
sns.boxplot(data=df_main, x='weathersit', y='cnt', hue='weathersit', palette='pastel', dodge=False)
plt.xticks(ticks=[0, 1, 2, 3], labels=['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
plt.title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

st.caption('Copyright (c) Mazdalifah Hanuranda 2025')