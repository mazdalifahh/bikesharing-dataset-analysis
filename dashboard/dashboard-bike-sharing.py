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
# Add subheader for this section
st.subheader("Tren Penyewaan Sepeda Sepanjang Tahun")

# Plotly line plot untuk tren penyewaan sepeda sepanjang tahun
fig = px.line(df_main, x='month', y='cnt', color='year',
              labels={'month': 'Bulan', 'cnt': 'Jumlah Penyewaan'},
              title="Tren Penyewaan Sepeda per Bulan (2011 vs 2012)")
fig.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.plotly_chart(fig)  # Display the plot in Streamlit

# Plotly bar plot untuk penyewaan sepeda berdasarkan hari
# Group by 'weekday' to get average count of rentals per day
daily_rentals = df_main.groupby('weekday')['cnt'].mean().reset_index()

# Add labels for weekdays
daily_rentals['weekday_label'] = daily_rentals['weekday'].map({0: 'Sen', 1: 'Sel', 2: 'Rab', 3: 'Kam', 4: 'Jum', 5: 'Sab', 6: 'Min'})

# Plotly bar plot untuk penyewaan sepeda berdasarkan hari
fig = px.bar(daily_rentals, x='weekday_label', y='cnt', 
             labels={'weekday_label': 'Hari', 'cnt': 'Jumlah Penyewa'},
             title="Penyewaan Sepeda Berdasarkan Hari dalam Seminggu", 
             color='weekday_label')
fig.update_xaxes(tickmode='array', tickvals=daily_rentals['weekday_label'], ticktext=daily_rentals['weekday_label'])
st.plotly_chart(fig)  # Display the plot in Streamlit



