import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

st.markdown(
    "<h1 style='text-align: center; font-family: Times New Roman; font-size: 24pt;'>Air Quality Dashboard</h1>", 
    unsafe_allow_html=True
)
st.write("")

# Load the data
file_kota1 = "D:/1. KULIAH/s7/BANGKIT/1/PRSA_Data_20130301-20170228/PRSA_Data_Shunyi_20130301-20170228.csv"
file_kota2 = "D:/1. KULIAH/s7/BANGKIT/1/PRSA_Data_20130301-20170228/PRSA_Data_Dongsi_20130301-20170228.csv"

df_kota1 = pd.read_csv(file_kota1)
df_kota2 = pd.read_csv(file_kota2)

df_kota1['station'] = 'Shunyi'
df_kota2['station'] = 'Dongsi'

df = pd.concat([df_kota1, df_kota2], ignore_index=True)

# Clean the data
df_clean = df.dropna(subset=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'RAIN'])

# Create a sidebar with interactive filters
st.sidebar.header("Select filters")
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
selected_pollutants = st.sidebar.multiselect("Select pollutants", pollutants, default=['PM2.5'])
selected_year = st.sidebar.selectbox("Select year", df_clean['year'].unique(), index=0)
selected_month = st.sidebar.selectbox("Select month", range(1, 13), format_func=lambda x: calendar.month_name[x])

# Filter data by selected month and year
df_clean['month'] = pd.to_datetime(df_clean['year'] * 10000 + df_clean['month'] * 100 + df_clean['day'], format='%Y%m%d').dt.month
df_filtered = df_clean[(df_clean['month'] == selected_month) & (df_clean['year'] == selected_year)]

# Create a figure for the average pollutant comparison
fig1, ax1 = plt.subplots(figsize=(10, 6))

rata_rata_polutan = df_filtered.groupby('station')[selected_pollutants].mean().reset_index()
rata_rata_polutan_melt = pd.melt(rata_rata_polutan, id_vars=['station'], value_vars=selected_pollutants)

sns.barplot(x='station', y='value', hue='variable', data=rata_rata_polutan_melt, ax=ax1)
ax1.set_title("Perbandingan Rata-rata Polutan Antar Kota")
ax1.set_xlabel("Kota")
ax1.set_ylabel("Konsentrasi Rata-rata Polutan")

# Menampilkan nilai di atas setiap bar pada grafik pertama
for p in ax1.patches:
    ax1.annotate(format(p.get_height(), '.2f'), 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha = 'center', va = 'center', 
                 xytext = (0, 9), textcoords = 'offset points')

st.pyplot(fig1)

st.write("")

# Create a figure for the pollution category distribution by month and year
bins = [0, 35, 75, 115, 150, np.inf]
labels = ['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Hazardous']
df_filtered['pollution_level'] = pd.cut(df_filtered['PM2.5'], bins=bins, labels=labels)

fig2, ax2 = plt.subplots(figsize=(10, 6))

# Menambahkan hue berdasarkan 'station' untuk memisahkan distribusi Shunyi dan Dongsi
sns.countplot(x='pollution_level', data=df_filtered, hue='station', palette='viridis', ax=ax2)

ax2.set_title(f"Distribusi Kategori PM2.5 di Shunyi dan Dongsi (Bulan {calendar.month_name[selected_month]} {selected_year})")
ax2.set_xlabel("Kategori Polusi")
ax2.set_ylabel("Jumlah Observasi")
ax2.legend(title='Kota')

# Menampilkan nilai di atas setiap bar pada grafik kedua
for p in ax2.patches:
    ax2.annotate(format(p.get_height(), '.0f'), 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha = 'center', va = 'center', 
                 xytext = (0, 9), textcoords = 'offset points')

st.pyplot(fig2)
