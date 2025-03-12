import streamlit as st  
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as sns  
import plotly.express as px  

# Load Data dengan Cache untuk Optimasi
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['month'] = df['dteday'].dt.month
    df['year'] = df['dteday'].dt.year
    df['weekday'] = df['dteday'].dt.weekday
    df['season_name'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    df['weather_desc'] = df['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'})
    df['usage_category'] = pd.cut(df['cnt'], bins=[0, 2000, 4000, 8000], labels=['Low', 'Medium', 'High'])
    return df

df_main = load_data()

# Streamlit Dashboard
st.title("🚴‍♂️ Bike Sharing Data Dashboard")

st.markdown("""
**Selamat datang di dashboard Bike Sharing!**  
Dashboard ini memungkinkan Anda untuk mengeksplorasi tren penggunaan sepeda berdasarkan data peminjaman.
""")

# Sidebar: Logo dan Filter Rentang Waktu
st.sidebar.image("dashboard/assets/Logo.png", use_column_width=True)
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [df_main['dteday'].min().date(), df_main['dteday'].max().date()])
df_filtered = df_main[(df_main['dteday'] >= pd.to_datetime(date_range[0])) & (df_main['dteday'] <= pd.to_datetime(date_range[1]))]

# KPI Section
st.subheader("📊 Overview")
st.metric("Total Rentals", df_filtered['cnt'].sum())
st.metric("Average Rentals per Day", round(df_filtered['cnt'].mean(), 2))

# 1. Tren Penyewaan Sepeda Sepanjang Tahun
st.subheader("📅 Tren Penyewaan Sepeda Sepanjang Tahun")
plt.figure(figsize=(12, 5))
ax = sns.lineplot(data=df_filtered, x='month', y='cnt', hue='year', marker='o', palette='coolwarm')

# Menambahkan label angka pada setiap titik
for line in ax.lines:
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        ax.text(x, y, f'{int(y)}', ha='center', va='bottom', fontsize=10)

plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.title("Tren Penyewaan Sepeda Sepanjang Tahun")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.legend(title="Tahun", labels=["2011", "2012"])
plt.grid()
st.pyplot(plt)

# 2. Pola Penyewaan Berdasarkan Hari & Jam
st.subheader("⏰ Pola Penyewaan Berdasarkan Hari & Jam")

# Pastikan data sesuai
hourly_trend = df_filtered.groupby(['hr', 'weekday'])['cnt'].mean().reset_index()

# Urutan hari (pastikan sesuai dengan dataset)
weekday_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Mapping angka weekday ke nama hari
weekday_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
hourly_trend['weekday'] = hourly_trend['weekday'].map(weekday_map)

# Mapping warna agar sesuai antara line dan legenda
colors = sns.color_palette("Set1", n_colors=7)
color_map = dict(zip(weekday_order, colors))

# Plot
plt.figure(figsize=(12, 5))
ax = sns.lineplot(
    data=hourly_trend, 
    x="hr", y="cnt", 
    hue="weekday", 
    palette=color_map,  # Pakai color mapping yang benar
    linewidth=2.5, marker="o"
)

# Highlight jam sibuk
plt.axvspan(7, 9, color='gray', alpha=0.2, label="Jam Sibuk Pagi")
plt.axvspan(16, 18, color='gray', alpha=0.2, label="Jam Sibuk Sore")

# Pastikan legenda mengikuti warna yang benar
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles, title="Hari", labels=weekday_order)

# Label dan grid
plt.title("Tren Penyewaan Sepeda Berdasarkan Jam dalam Sehari untuk Setiap Hari")
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan")
plt.xticks(ticks=range(0, 24, 2))
plt.grid()

st.pyplot(plt)

# 3. Pengaruh Musim & Cuaca terhadap Penyewaan
st.subheader("🌦️ Pengaruh Musim & Cuaca terhadap Penyewaan")

# Boxplot Musim
plt.figure(figsize=(12, 5))
ax = sns.boxplot(data=df_filtered, x='season', y='cnt', hue='season', palette='pastel', dodge=False)
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])
plt.title("Pengaruh Musim terhadap Penyewaan Sepeda")
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan")

# Menambahkan label angka di atas setiap boxplot
season_means = df_filtered.groupby('season')['cnt'].mean()
for i, mean in enumerate(season_means):
    plt.text(i, mean, f'{int(mean)}', ha='center', va='bottom', fontsize=10)

st.pyplot(plt)

# Boxplot Cuaca
plt.figure(figsize=(12, 5))
ax = sns.boxplot(data=df_filtered, x='weathersit', y='cnt', hue='weathersit', palette='pastel', dodge=False)
plt.xticks(ticks=[0, 1, 2, 3], labels=['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
plt.title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Jumlah Penyewaan")

# Menambahkan label angka di atas setiap boxplot
weather_means = df_filtered.groupby('weathersit')['cnt'].mean()
for i, mean in enumerate(weather_means):
    plt.text(i, mean, f'{int(mean)}', ha='center', va='bottom', fontsize=10)

st.pyplot(plt)

# 4. Perbandingan Penyewaan antara Hari Kerja & Hari Libur
st.subheader("🏖️ Perbandingan Penyewaan antara Hari Kerja & Hari Libur")
plt.figure(figsize=(12, 5))
sns.barplot(data=df_filtered, x='holiday', y='cnt', hue='holiday', palette='Blues', dodge=False)
plt.xticks(ticks=[0, 1], labels=['Hari Kerja', 'Hari Libur'])
plt.title("Perbandingan Penyewaan antara Hari Kerja & Hari Libur")
plt.xlabel("Kategori Hari")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(plt)

# 5. Distribusi Pengguna Sepeda (Casual vs. Registered)
st.subheader("👥 Distribusi Pengguna Sepeda (Casual vs. Registered)")
plt.figure(figsize=(12, 5))
ax = df_filtered[['casual', 'registered']].sum().plot(kind='bar', color=['lightblue', 'salmon'])

# Menambahkan label angka di atas setiap batang
totals = df_filtered[['casual', 'registered']].sum()
for i, total in enumerate(totals):
    plt.text(i, total, f'{int(total)}', ha='center', va='bottom', fontsize=12)

plt.title("Distribusi Pengguna Sepeda (Casual vs. Registered)")
plt.ylabel("Total Pengguna")
plt.xticks(rotation=0)
st.pyplot(plt)


st.caption('Copyright (c) Mazdalifah Hanuranda 2025')
