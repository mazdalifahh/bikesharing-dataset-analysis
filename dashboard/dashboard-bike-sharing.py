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

# Penjelasan Tren Penyewaan per Bulan
st.subheader("📈 Tren per bulan 2011 vs 2012")

# Pastikan kolom dteday sudah dalam format datetime
df_main['dteday'] = pd.to_datetime(df_main['dteday'])

# Tambahkan kolom tahun & bulan
df_main['year'] = df_main['dteday'].dt.year
df_main['month'] = df_main['dteday'].dt.month

# Plot Tren Penyewaan per Bulan
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_main, x='month', y='cnt', hue='year', marker="o")

plt.xticks(range(1, 13))  # Menampilkan angka bulan dengan benar (1-12)
plt.title("Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.grid()
st.pyplot(plt)  # Menampilkan plot di Streamlit

# Line Chart - Tren Penyewaan per Jam
# Mengelompokkan data berdasarkan jam dan menghitung rata-rata jumlah penyewaan
df_hour_avg = df_main.groupby('hr', as_index=False)['cnt'].mean()

# Membuat line chart dengan Plotly
fig4 = px.line(df_hour_avg, x='hr', y='cnt', markers=True, 
               title='Pola Penyewaan Sepeda per Jam', 
               labels={'hr': 'Jam', 'cnt': 'Jumlah Penyewaan'})

# Menampilkan grafik di Streamlit
st.plotly_chart(fig4)

# Warna yang berbeda untuk setiap kategori
color_discrete_map_hari = {
    "Sen": "#636EFA", "Sel": "#EF553B", "Rab": "#00CC96", 
    "Kam": "#AB63FA", "Jum": "#FFA15A", "Sab": "#19D3F3", "Min": "#FF6692"
}
color_discrete_map_musim = {
    "Spring": "#FF7F0E", "Summer": "#2CA02C", "Fall": "#D62728", "Winter": "#9467BD"
}
color_discrete_map_cuaca = {
    "Clear": "#1F77B4", "Cloudy": "#FFBB78", "Light Rain": "#8C564B", 
    "Heavy Rain": "#E377C2", "Snow": "#7F7F7F"
}

import plotly.express as px
import streamlit as st

# Warna yang berbeda untuk setiap kategori
color_discrete_map_hari = {
    "Sen": "#636EFA", "Sel": "#EF553B", "Rab": "#00CC96", 
    "Kam": "#AB63FA", "Jum": "#FFA15A", "Sab": "#19D3F3", "Min": "#FF6692"
}
color_discrete_map_musim = {
    "Spring": "#FF7F0E", "Summer": "#2CA02C", "Fall": "#D62728", "Winter": "#9467BD"
}
color_discrete_map_cuaca = {
    "Clear": "#1F77B4", "Cloudy": "#FFBB78", "Light Rain": "#8C564B", 
    "Heavy Rain": "#E377C2", "Snow": "#7F7F7F"
}

# Penjelasan untuk Boxplot Penyewaan per Hari
st.markdown("""
### Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
Grafik ini menunjukkan **distribusi jumlah penyewaan sepeda** untuk setiap hari dalam seminggu:
- **Kotak menunjukkan rentang utama data (kuartil 25%-75%)**, sedangkan garis di tengahnya menunjukkan **median (nilai tengah)**.
- **Titik-titik di luar kotak adalah outlier**, yang berarti jumlah penyewaan di hari itu jauh lebih tinggi atau rendah dibanding biasanya.
""")

# Boxplot - Tren Penyewaan per Hari dalam Seminggu
fig3 = px.box(df_main, x='weekday', y='cnt', 
              title='Penyewaan Sepeda Berdasarkan Hari dalam Seminggu', 
              labels={'weekday': 'Hari', 'cnt': 'Jumlah Penyewa'},
              color='weekday',  
              color_discrete_map=color_discrete_map_hari,  # Warna khusus untuk hari
              points="all"
             )
fig3.update_xaxes(tickvals=list(range(7)), 
                  ticktext=["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
fig3.update_traces(marker=dict(opacity=0.5), line=dict(width=2))
st.plotly_chart(fig3)

# Penjelasan untuk Boxplot Pengaruh Musim
st.markdown("""
### Pengaruh Musim terhadap Penyewaan Sepeda
Grafik ini menunjukkan bagaimana jumlah penyewaan sepeda **bervariasi berdasarkan musim**.
- **Setiap warna mewakili musim yang berbeda**.
- Seperti sebelumnya, **kotak menunjukkan persebaran utama data**, dan **outlier ditampilkan sebagai titik-titik di luar kotak**.
""")

# Boxplot - Pengaruh Musim terhadap Penyewaan
fig5 = px.box(df_main, x='season_name', y='cnt', 
              title='Pengaruh Musim terhadap Penyewaan Sepeda', 
              color='season_name',
              color_discrete_map=color_discrete_map_musim,  # Warna khusus musim
              labels={'season_name': 'Musim', 'cnt': 'Jumlah Penyewaan'},
              points="all"
             )
fig5.update_traces(marker=dict(opacity=0.5), line=dict(width=2))
st.plotly_chart(fig5)

# Penjelasan untuk Boxplot Pengaruh Cuaca
st.markdown("""
### Pengaruh Cuaca terhadap Penyewaan Sepeda
Grafik ini menunjukkan bagaimana jumlah penyewaan sepeda **dipengaruhi oleh kondisi cuaca**.
- **Setiap warna mewakili kondisi cuaca yang berbeda**.
- **Distribusi data ditampilkan dengan kotak dan garis median**, serta outlier yang ditampilkan sebagai titik-titik.
""")

# Boxplot - Pengaruh Cuaca terhadap Penyewaan
fig6 = px.box(df_main, x='weather_desc', y='cnt', 
              title='Pengaruh Cuaca terhadap Penyewaan Sepeda', 
              color='weather_desc',
              color_discrete_map=color_discrete_map_cuaca,  # Warna khusus cuaca
              labels={'weather_desc': 'Kondisi Cuaca', 'cnt': 'Jumlah Penyewaan'},
              points="all"
             )
fig6.update_traces(marker=dict(opacity=0.5), line=dict(width=2))
st.plotly_chart(fig6)

# Barplot - Peminjaman Hari Kerja vs Hari Libur
fig7 = px.bar(df_main, x='workingday', y='cnt', title='Peminjaman Sepeda pada Hari Kerja vs Hari Libur', labels={'workingday': 'Hari', 'cnt': 'Jumlah Peminjaman'})
fig7.update_xaxes(tickvals=[0,1], ticktext=['Hari Libur', 'Hari Kerja'])
st.plotly_chart(fig7)

# Barplot - Peminjaman Berdasarkan Musim
fig8 = px.bar(df_main, x='season_name', y='cnt', title='Peminjaman Sepeda Berdasarkan Musim', color='season_name', category_orders={'season_name': ['Spring', 'Summer', 'Fall', 'Winter']})
st.plotly_chart(fig8)

# Heatmap Korelasi Variabel Numerik
df_numeric = df_main.select_dtypes(include=[np.number])
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title("Heatmap Korelasi Antar Variabel Numerik dalam Penyewaan Sepeda", fontsize=12)
st.pyplot(fig)

# Analisis RFM
latest_date = df_main['dteday'].max()
df_rfm = df_main.groupby('dteday').agg({
    'cnt': ['sum', 'count'],
}).reset_index()
df_rfm.columns = ['Date', 'Monetary', 'Frequency']
df_rfm['Recency'] = (latest_date - df_rfm['Date']).dt.days

st.subheader("📊 Analisis RFM (Recency, Frequency, Monetary)")
st.write("- **Recency (Hari):** Seberapa baru transaksi terakhir pengguna")
st.write("- **Frekuensi Penyewaan (Frequency):** Seberapa sering transaksi dilakukan")
st.write("- **Total Penyewaan (Monetary):** Total nilai transaksi")
st.dataframe(df_rfm)

# Visualisasi RFM
fig_rfm = px.scatter(df_rfm, x='Recency', y='Frequency', 
                     size='Monetary', 
                     title='Distribusi RFM')

st.plotly_chart(fig_rfm)

# Buat DataFrame RFM berdasarkan tanggal
latest_date = df_main['dteday'].max()

df_rfm = df_main.groupby('dteday').agg({
    'cnt': ['sum', 'count'],  # Monetary (Total penyewaan) & Frequency (Jumlah transaksi dalam sehari)
}).reset_index()

df_rfm.columns = ['Date', 'Monetary', 'Frequency']

# Hitung Recency sebagai selisih dari tanggal terbaru
df_rfm['Recency'] = (latest_date - df_rfm['Date']).dt.days

# Sort dan pilih 5 terbaik
top_recency = df_rfm.sort_values(by="Recency", ascending=True).head(5)
top_frequency = df_rfm.sort_values(by="Frequency", ascending=False).head(5)
top_monetary = df_rfm.sort_values(by="Monetary", ascending=False).head(5)

# Buat figure
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4"] * 5  # Warna uniform

# Recency Plot
sns.barplot(y="Recency", x="Date", data=top_recency, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=12, rotation=45)

# Frequency Plot
sns.barplot(y="Frequency", x="Date", data=top_frequency, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=12, rotation=45)

# Monetary Plot
sns.barplot(y="Monetary", x="Date", data=top_monetary, palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=12, rotation=45)

plt.suptitle("Top 5 Days Based on RFM Parameters", fontsize=20)
plt.show()
st.pyplot(fig)

# Binning Kategori Penyewaan
# Menentukan batas bin berdasarkan kuantil
bins = df_main['cnt'].quantile([0, 0.25, 0.5, 0.75, 1]).values
labels = ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']

# Membuat kategori penyewaan berdasarkan bin
df_main['Kategori Penyewaan'] = pd.cut(df_main['cnt'], bins=bins, labels=labels, include_lowest=True)

# Menampilkan hasil binning
st.subheader("📌 Kategori Penyewaan")
st.write(df_main['Kategori Penyewaan'].value_counts()) 

# komentar
