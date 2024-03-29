import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

bike_df = pd.read_csv("kumpulan_data.csv")
bike_df.head()

def generate_daily_rent_data(df):
    daily_rent_data = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_data

def generate_daily_casual_rent_data(df):
    daily_casual_rent_data = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_data

def generate_daily_registered_rent_data(df):
    daily_registered_rent_data = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_data
    
def generate_seasonal_rent_data(df):
    seasonal_rent_data = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return seasonal_rent_data

def generate_monthly_rent_data(df):
    monthly_rent_data = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_data = monthly_rent_data.reindex(ordered_months, fill_value=0)
    return monthly_rent_data

def generate_weekday_rent_data(df):
    weekday_rent_data = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_data

def generate_workingday_rent_data(df):
    workingday_rent_data = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_data

def generate_holiday_rent_data(df):
    holiday_rent_data = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_data

def generate_weather_rent_data(df):
    weather_rent_data = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_data

# Membuat komponen filter
min_date = pd.to_datetime(bike_df['dateday']).dt.date.min()
max_date = pd.to_datetime(bike_df['dateday']).dt.date.max()
with st.sidebar:
    st.image('Sepeda.jpg')
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
main_df = bike_df[(bike_df['dateday'] >= str(start_date)) & 
                (bike_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_data = generate_daily_rent_data(main_df)
daily_casual_rent_data = generate_daily_casual_rent_data(main_df)
daily_registered_rent_data = generate_daily_registered_rent_data(main_df)
seasonal_rent_data = generate_seasonal_rent_data(main_df)
monthly_rent_data = generate_monthly_rent_data(main_df)
weekday_rent_data = generate_weekday_rent_data(main_df)
workingday_rent_data = generate_workingday_rent_data(main_df)
holiday_rent_data = generate_holiday_rent_data(main_df)
weather_rent_data = generate_weather_rent_data(main_df)

#judul
st.header('Bike Rental Dashboard')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_casual_count = daily_casual_rent_data['casual'].sum()
    st.metric('Casual User', value= daily_casual_count)
with col2:
    daily_registered_count = daily_registered_rent_data['registered'].sum()
    st.metric('Registered User', value= daily_registered_count)
with col3:
    daily_total_count = daily_rent_data['count'].sum()
    st.metric('Total User', value= daily_total_count)


# Membuat jumlah penyewaan bulanan
st.subheader('Monthly')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_data.index,
    monthly_rent_data['count'],
    marker='o', 
    linewidth=2,
    color='tab:orange'
    
)
for index, row in enumerate(monthly_rent_data['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader('Weatherly')
fig, ax = plt.subplots(figsize=(16, 8))
colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_rent_data.index,
    y=weather_rent_data['count'],
    palette=colors,
    ax=ax
)
for index, row in enumerate(weather_rent_data['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuat jumlah penyewaan Mingguan
colors1=["tab:blue", "tab:orange"]
colors2=["tab:blue", "tab:orange"]
colors3=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

st.subheader('Workingday and Holiday')
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
axes[0].pie(workingday_rent_data['count'], labels=workingday_rent_data['workingday'], colors=colors1, autopct='%1.1f%%')
axes[0].set_title('Number of Rents based on Working Day')
axes[1].pie(holiday_rent_data['count'], labels=holiday_rent_data['holiday'], colors=colors2, autopct='%1.1f%%')
axes[1].set_title('Number of Rents based on Holiday')

plt.tight_layout()
st.pyplot(fig)