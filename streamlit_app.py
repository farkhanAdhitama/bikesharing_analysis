import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.set_page_config(layout="centered")
# Header
st.header('Bike Sharing Dataset Analysis:')
 
# load dataset
maindata_df = pd.read_csv("main_data.csv")

# Filter berdasarkan tanggal dan sidebar
min_date = maindata_df["dteday"].min()
max_date = maindata_df["dteday"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://bikeshare.metro.net/wp-content/uploads/2016/04/cropped-metro-bike-share-favicon-1.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
filtered_df = maindata_df[(maindata_df["dteday"] >= str(start_date)) & 
                (maindata_df["dteday"] <= str(end_date))]

# CREATE DF
# daily rentals
def create_daily_df(df):
    order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    daily_df = df.groupby("weekday").cnt.mean().reindex(order).reset_index()
    return daily_df
# by season
def create_byseason_df(df):
    byseason_df = df.groupby("season").cnt.mean().reset_index()
    return byseason_df
# by weather situation
def create_byweathersit_df(df):
    byweatsit_df = df.groupby("weathersit").cnt.mean().reset_index()
    return byweatsit_df

# Panggil fungsi membuat dataset
daily_sharing = create_daily_df(filtered_df)
season_sharing = create_byseason_df(filtered_df)
weathersit_sharing = create_byweathersit_df(filtered_df)

# Plot data
# Rata-rata penyewaan setiap hari
st.subheader("Rata-Rata Penyewaan Setiap Hari")
plt.figure(figsize=(12, 5))
sns.barplot(
    y="cnt",
    x="weekday",
    data=daily_sharing,
)
plt.title("Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Hari", loc="center", fontsize=15)
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.xlabel("Hari")
st.pyplot(plt)

# Rata-rata penyewaan berdasarkan musim dan kondisi cuaca
st.subheader("Pengaruh Musim dan Cuaca")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 15))
# musim
sns.barplot(x="season", y="cnt", data=season_sharing, ax=ax[0])
ax[0].set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=30)
ax[0].set_xlabel("Musim", fontsize=30)
ax[0].set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
# kondisi cuaca
sns.barplot(x="weathersit", y="cnt", data=weathersit_sharing, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Cuaca", fontsize=30)
ax[1].set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.caption('Copyright (c) 2025')
