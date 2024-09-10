import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

day_df = pd.read_csv('https://raw.githubusercontent.com/ilhaaam24/Submission-DIcoding-Analisis-Data-dengan-Python/main/data/day.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/ilhaaam24/Submission-DIcoding-Analisis-Data-dengan-Python/main/data/hour.csv')

Q1 = (hour_df['cnt']).quantile(0.25)
Q3 = (hour_df['cnt']).quantile(0.75)
IQR = Q3 - Q1 
maximum = Q3 + (1.5*IQR)
minimum = Q1 - (1.5*IQR)
kondisi_lower_than = hour_df['cnt'] < minimum
kondisi_more_than = hour_df['cnt'] > maximum
hour_df.drop(hour_df[kondisi_lower_than].index, inplace=True)
hour_df.drop(hour_df[kondisi_more_than].index, inplace=True)
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])


with st.sidebar:
    st.markdown(
        """
        <style>
        .rounded-img {
            border-radius: 50%;
            width: 200px;
            height: 200px;
            object-fit: cover;
        }
        </style>
        <img src="https://github.com/ilhaaam24/Submission-DIcoding-Analisis-Data-dengan-Python/blob/main/assets/aboutbw.jpg?raw=true" class="rounded-img" />
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    -
    - **Author:** Muhammad Ilham
    - **Email:** mi1797128@gmail.com
    - **ID Dicoding:** ilham24
    """)

st.title('Analisis Data : Bike sharing')
st.write('Dataset ini berasal dari sistem bike-sharing Capital Bikeshare di Washington D.C., USA, yang mencakup log historis dari tahun 2011 hingga 2012. Bike-sharing adalah sistem sewa sepeda modern yang memungkinkan pengguna untuk menyewa sepeda dari satu lokasi dan mengembalikannya di lokasi lain secara otomatis. Sistem ini tidak hanya mempermudah proses sewa, tetapi juga menghasilkan data yang berharga tentang pola mobilitas kota.')


def plot_bike_sharing_data(data):
    bulanan = data.groupby(pd.Grouper(key='dteday', freq='M')).sum()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(bulanan.index, bulanan['cnt'], marker='o', linestyle='-', color='#00A3E0', linewidth=2, markersize=6)
    ax.set_xticks(bulanan.index)
    ax.set_xticklabels(bulanan.index.strftime('%b %Y'), color='lightgrey', fontsize=10)
    ax.set_yticklabels(ax.get_yticks(), color='lightgrey')
    ax.set_xlabel('Bulan', color='lightgrey')
    ax.set_ylabel('Jumlah Penyewaan', color='lightgrey')
    ax.grid(True, color='grey', linestyle='--', alpha=0.5)
    ax.set_facecolor('#1b1b1b')  # Warna latar belakang gelap
    fig.patch.set_facecolor('#1b1b1b')  # Warna latar belakang gelap
    for spine in ax.spines.values():
        spine.set_edgecolor('lightgrey')

    st.pyplot(fig)

def main():
    st.subheader("Jumlah Penyewaan Sepeda per Bulan (Jan 2011 - Des 2012)")
    plot_bike_sharing_data(hour_df)

if __name__ == "__main__":
    main()

st.subheader('Distribusi Jumlah Penyewaan Berdasarkan Tiap Kategori')
tab1, tab2 = st.tabs(['Bar chart', 'Pie chart'])

with tab1:  
  fitur = ['mnth', 'hr', 'weekday', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered']
  for feature in fitur:
    fig = px.histogram(hour_df, x=feature, y='cnt', title=f'Distribusi {feature}')
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_layout(yaxis_title='Jumlah peminjam')
    st.plotly_chart(fig)
    

with tab2:
  categories = ['season','holiday','workingday','weathersit']
  def show_pie_charts(categories):
    for category in categories: 
        fig = px.pie(hour_df, names=category, values='cnt', title=f'Distribusi Jumlah Penyewaan Berdasarkan {category}')
        st.plotly_chart(fig)
  show_pie_charts(categories)


st.header('Pertanyaan Bisnis')
st.markdown("""
- Pertanyaan 1 : Berapa total terpinjam pada bulan Desember 2011?
- Pertanyaan 2 : Pada bulan apa rata - rata peminjaman sepeda paling banyak ?
- Pertanyaan 3 : Apakah terdapat tren musiman dalam penyewaan sepeda?
""")

def plot_monthly_comparison(data):
    monthly_totals = data[data['yr'] == 1].groupby('mnth')['cnt'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_totals.plot(kind='bar', color='skyblue', ax=ax)
    
    ax.patches[11].set_color('orange')
    
    ax.set_title('Berapa total terpinjam pada bulan Desember 2011?')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Total Peminjaman')
    ax.set_xticks(range(12))
    ax.set_xticklabels([
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig

def main():
    st.subheader("Perbandingan Total Peminjaman Sepeda per Bulan Tahun 2011")
    fig = plot_monthly_comparison(hour_df)
    st.pyplot(fig)
    st.write("Total peminjaman sepeda pada bulan Desember 2011 adalah 114538")

if __name__ == "__main__":
    main()
def plot_average_rentals_per_month(data):
    average_rentals_per_month = data.groupby('mnth')['cnt'].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    average_rentals_per_month.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Rata-rata Peminjaman Sepeda per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Peminjaman Sepeda')
    ax.set_xticks(range(12))  # Ubah range ke 12 untuk 0-11
    ax.set_xticklabels([
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], rotation=0)
    ax.grid(axis='y')
    
    ax.set_xlim(-0.5, 11.5)  # 
    return fig

def main():
    st.subheader("Rata-rata Peminjaman Sepeda per Bulan")
    fig = plot_average_rentals_per_month(day_df)
    st.pyplot(fig)
    st.write("Rata-rata peminjaman sepeda paling tinggi pada bulan Juni 2011.")

if __name__ == "__main__":
    main()




def plot_seasonal_trends(data):
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    for i, season in enumerate(seasons):
        ax = axs[i // 2, i % 2]
        season_data = data[data['season'] == i+1].groupby('mnth')['cnt'].mean()
        ax.plot(season_data.index, season_data.values, marker='o', linestyle='-', color='tab:blue')
        ax.set_title(season)
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Rata-rata Peminjaman')
        ax.grid(True)
    
    plt.tight_layout()
    return fig

def main():
    st.subheader("Tren Peminjaman Sepeda per Musim")
    fig = plot_seasonal_trends(day_df)
    st.pyplot(fig)
    st.write("Tren peminjaman sepeda cenderung lebih tinggi pada musim panas dibandingkan musim lainnya.")

if __name__ == "__main__":
    main()

st.header("Conclusion")
st.markdown("""
- Conclution pertanyaan 1: Total sepeda terpinjam pada bulan Desember 2011 yaitu 114538
- Conclution pertanyaan 2: Rata - rata peminjaman sepeda paling banyak terdapat pada bulan Juni
- Conclution pertanyaan 3: Penyewaan sepeda cenderung lebih tinggi pada musim panas dibandingkan musim lainnya.
Musim semi juga menunjukkan peningkatan dalam penyewaan, tetapi tidak sekuat musim panas. Musim dingin memiliki penyewaan terendah,
kemungkinan karena cuaca yang kurang mendukung untuk bersepeda. Musim gugur menunjukkan variasi yang signifikan, dengan penurunan tajam di tengah musim.
""")
