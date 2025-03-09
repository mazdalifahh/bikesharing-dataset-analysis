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
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [df_main['dteday'].min().date(), df_main['dteday'].max().date()])

# Filter Data
df_filtered = df_main.loc[
    (df_main['dteday'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# KPI Section
st.subheader("📊 Overview")
st.metric("Total Rentals", df_filtered['cnt'].sum())
st.metric("Average Rentals per Day", round(df_filtered['cnt'].mean(), 2))

st.subheader("Tren Penyewaan Sepeda Sepanjang Tahun")

# Pastikan kolom dteday sudah dalam format datetime
df_main['dteday'] = pd.to_datetime(df_main['dteday'])

# Tambahkan kolom tahun & bulan
df_main['year'] = df_main['dteday'].dt.year
df_main['month'] = df_main['dteday'].dt.month

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = df_main[df_main['user_type'] == 'casual'].groupby('date')['cnt'].sum().sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = df_main[df_main['user_type'] == 'registered'].groupby('date')['cnt'].sum().sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = df_main.groupby('date')['cnt'].sum().sum()
    st.metric('Total Rentals', value=daily_rent_total)

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
monthly_rent_df = df_main.groupby(df_main['month'])['cnt'].sum()
ax.plot(monthly_rent_df.index, monthly_rent_df.values, marker='o', linewidth=2, color='tab:blue')

for index, row in enumerate(monthly_rent_df):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonal Rentals')

fig, ax = plt.subplots(figsize=(16, 8))
season_rent_df = df_main.groupby('season').agg({'cnt': 'sum', 'user_type': 'count'}).reset_index()

sns.barplot(x='season', y='cnt', data=season_rent_df, label='Total Rentals', color='tab:blue', ax=ax)
sns.barplot(x='season', y='user_type', data=season_rent_df, label='Casual vs Registered', color='tab:orange', ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Membuat grafik penyewaan berdasarkan cuaca
st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

weather_rent_df = df_main.groupby('weathersit')['cnt'].sum()
colors = ["tab:blue", "tab:orange", "tab:green"]

sns.barplot(x=weather_rent_df.index, y=weather_rent_df.values, palette=colors, ax=ax)

for index, row in enumerate(weather_rent_df):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Analisis berdasarkan Hari, Jam, dan Musim
st.subheader("Penyewaan Sepeda Berdasarkan Hari, Jam, dan Musim")

# Tren Penyewaan berdasarkan Tahun
st.subheader("Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_main, x='month', y='cnt', hue='year', marker="o")
plt.xticks(range(1, 13))  # Menampilkan angka bulan dengan benar (1-12)
plt.title("Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.grid()
st.pyplot(plt)  # Display the plot in Streamlit

# Penyewaan berdasarkan Hari dalam Seminggu
st.subheader("Pola Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
daily_rentals = df_main.groupby('weekday')['cnt'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(data=daily_rentals, x='weekday', y='cnt', color="steelblue")
plt.title('Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewa')
plt.xticks(ticks=range(7), labels=["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
plt.grid(axis='y')
st.pyplot(plt)  # Display the plot in Streamlit

# Penyewaan berdasarkan Jam
st.subheader("Pola Penyewaan Sepeda per Jam")
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_main, x='hr', y='cnt', marker="o", color="steelblue")
plt.title('Pola Penyewaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewa')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(plt)  # Display the plot in Streamlit

# Pengaruh Musim dan Cuaca
st.subheader("Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")

# Boxplot Musim
plt.figure(figsize=(8, 5))
sns.boxplot(data=df_main, x='season', y='cnt', hue='season', palette="pastel", dodge=False)
plt.xticks([0, 1, 2, 3], ["Spring", "Summer", "Fall", "Winter"])
plt.title("Pengaruh Musim terhadap Penyewaan Sepeda")
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan")
plt.grid()
st.pyplot(plt)  # Display the plot in Streamlit

# Boxplot Cuaca
plt.figure(figsize=(8, 5))
sns.boxplot(data=df_main, x='weathersit', y='cnt', hue='weathersit', palette="pastel", dodge=False)
plt.xticks([0, 1, 2, 3], ["Clear", "Mist", "Light Snow/Rain", "Heavy Rain/Snow"])
plt.title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Jumlah Penyewa")
plt.grid()
st.pyplot(plt)  # Display the plot in Streamlit

# Penyewaan berdasarkan Hari Kerja vs Libur
st.subheader("Peminjaman Sepeda berdasarkan Hari Kerja vs Hari Libur")
plt.figure(figsize=(8,5))
sns.barplot(data=df_main, x='workingday', y='cnt', palette="Blues_d")
plt.xticks([0, 1], ['Hari Libur', 'Hari Kerja'])
plt.xlabel('Hari')
plt.ylabel('Jumlah Peminjaman')
plt.title('Peminjaman Sepeda pada Hari Kerja vs Hari Libur')
plt.grid(axis='y')
st.pyplot(plt)  # Display the plot in Streamlit

# Peminjaman berdasarkan Musim dan Kategori Pengguna
st.subheader("Peminjaman berdasarkan Musim dan Kategori Pengguna")
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_main['season_name'] = df_main['season'].map(season_map)

plt.figure(figsize=(8, 5))
sns.barplot(data=df_main, x='season_name', y='cnt', order=['Spring', 'Summer', 'Fall', 'Winter'], palette="viridis")
plt.xlabel('Musim')
plt.ylabel('Jumlah Peminjaman')
plt.title('Peminjaman Sepeda Berdasarkan Musim')
plt.grid(axis='y')
st.pyplot(plt)  # Display the plot in Streamlit

####

## Binning dan RFM Analysis

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Misalkan df_main adalah dataframe yang sudah kamu load
# df_main = pd.read_csv('data.csv') # Contoh pengambilan data

# Pastikan kolom 'dteday' dalam format datetime
df_main['dteday'] = pd.to_datetime(df_main['dteday'])

# 1. **Recency**: Menghitung Recency (waktu terakhir penyewaan)
current_date = df_main['dteday'].max()  # Tanggal terakhir di dataset

# Menghitung Recency
df_main['Recency'] = (current_date - df_main['dteday']).dt.days

# 2. **Frequency**: Menghitung jumlah penyewaan per hari
df_main['Frequency'] = df_main['cnt']

# 3. **Monetary**: Menghitung Monetary (jumlah penyewaan)
df_main['Monetary'] = df_main['cnt']

# 4. **Binning**: Menggunakan binning untuk membagi jumlah penyewaan
# Binning jumlah penyewaan untuk kategori 'casual' dan 'registered'

# Membuat bin untuk casual
df_main['Casual_Category'] = pd.cut(df_main['casual'], bins=[0, 500, 1500, 3000, 5000], labels=['Low', 'Medium', 'High', 'Very High'])

# Membuat bin untuk registered
df_main['Registered_Category'] = pd.cut(df_main['registered'], bins=[0, 500, 1500, 3000, 5000], labels=['Low', 'Medium', 'High', 'Very High'])

# Menampilkan RFM DataFrame (tanpa duplikat)
df_rfm = df_main[['dteday', 'Recency', 'Frequency', 'Monetary', 'Casual_Category', 'Registered_Category']].drop_duplicates()

# Menampilkan DataFrame RFM di Streamlit
st.subheader("📊 RFM Analysis with Binning")
st.write("RFM Analysis dengan penambahan binning untuk kategori Casual dan Registered.")

# Menampilkan RFM DataFrame
st.write(df_rfm)

# Menambahkan keterangan copyright di footer
st.caption('Copyright (c) Mazdalifah Hanuranda 2025')

