import streamlit as st
import numpy as np
import pandas as pd
import lorem
import seaborn as sns
import matplotlib.pyplot as plt
from numerize import numerize
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from vega_datasets import data
import altair as alt
import warnings
warnings.filterwarnings('ignore')

TITLE = 'Menelisik Produksi Perikanan dan Sebaran Konsumsi Ikan di Indonesia'

#Title
st.set_page_config(TITLE, layout='wide')
st.title(TITLE)
st.markdown("---")

"""
Sebagai negara kepulauan terbesar di dunia, Indonesia memiliki berbagai macam ekosistem pesisir dan laut diantaranya 
sumber daya perikanan. Indonesia dikenal sebagai salah satu surga perikanan dunia dan produsen ikan terbesar di Asia Tenggara.
Sumber daya ini mempunyai nilai protein yang tinggi sehingga ikan dapat menjadi sumber protein hewani utama ntuk masa depan. 
Potensi produksi perikanan budidaya di Indonesia mencapai 100 juta ton/tahun dengan nilai produksi mencapai USD 251 Miliar 
(Dahuri, 2019) dengan potensi ekonomi sektor kelautan perikanan mencapai 1.6 kali lipat PDB Nasional. Namun sayangnya, 
meskipun potensi dan pemanfaatan sumber daya perikanan relatif tinggi, tingkat konsumsi 
ikan masyarakat Indonesia tertinggal jauh di bawah negara-negara lain yang memiliki potensi sumber daya perikanan jauh 
lebih kecil. Konsumsi ikan di Indonesia dianggap masih rendah dan tidak merata antar wilayah.
"""

#Load Data
produksi = pd.read_csv("produksi_perikanan_provinsi.csv")

produksi = produksi.rename(columns = {'Volume_Produksi': 'Volume Produksi (Ton)'})

# Data Cleaning
produksi['Tahun'] = produksi['Tahun'].astype('str')
produksi_nan = produksi[(produksi['Volume Produksi (Ton)']==0.0) & (produksi['Nilai_Produksi']==0.0)]
produksi.drop(produksi_nan.index, inplace=True)

# Data Exploration
prod_pivot = pd.pivot_table(
    data=produksi,
    index='Tahun',
    columns='Jenis_Usaha',
    values='Volume Produksi (Ton)',
    aggfunc='sum'
  )
prod_pivot['TANGKAP']=prod_pivot['TANGKAP LAUT'] + prod_pivot['TANGKAP PUD']
prod_pivot.drop(['TANGKAP LAUT', 'TANGKAP PUD'], axis=1, inplace = True)

# Penggunaan Kolom
col1, col2= st.columns([2,1])

with col1:
    fig1, ax1 = plt.subplots(figsize=(15,15))
    prod_pivot.plot(
        ax = ax1,
        kind='bar', 
        figsize=(10,5),
        stacked=True,
        colormap='Dark2',
        legend=True
        )
    sns.lineplot(
        ax = ax1,
        data = produksi.groupby(produksi['Tahun']).sum()['Volume Produksi (Ton)'],
        marker='o',
        color='orange',
        dashes=True)
    st.pyplot(fig1)


with col2:
    st.write(
        """
Grafik di samping menunjukkan bahwa jumlah produksi perikanan budidaya dan tangkap di Indonesia 
terus meningkat dalam satu dekade terakhir, daro tahun 2010 sebesar 11,66 juta Ton hingga mencapai 21,83 
juta ton pada tahun 2020 dengan tingkat pertumbuhan sebesar 87,22%. 

Menurut data Badan Pusat Statistik (BPS) tahun 2020, kontribusi sub-sektor perikanan terhadap 
total PDB Indonesia menurut harga berlaku mencapai 2,80 persen atau meningkat 0,15 persen dibandingkan tahun 2019 
yang mencapai 2,65 persen, penurunan ini disebabkan oleh dampak pandemi tahun 2020. 

Meski demikian, produktivitas sektor akuakultur Indonesia tidak mengalami penurunan yang cukup signifikan,dengan 
proporsi produksi perikanan budidaya lebih besar dibandingkan 
perikanan tangkap. Pada tahun 2020, subsektor budidaya (akuakultur) Indonesia berkisar 14,85 juta Ton, sedangakn subsektor tangkap berkisar
7 juta Ton.
""")


df_budidaya = produksi[(produksi['Jenis_Usaha']=='BUDIDAYA') & (produksi['Tahun']=='2020')]
budidaya_produksi = df_budidaya[['Jenis_Ikan', 'Volume Produksi (Ton)']].groupby(['Jenis_Ikan'], as_index=False).sum()
budidaya_produksi = budidaya_produksi.drop(31)
budidaya_produksi.sort_values(by=['Volume Produksi (Ton)'], axis=0, ascending=False, inplace=True, ignore_index=True)
budidaya_produksi = budidaya_produksi.drop(labels=range(8,40), axis=0)

# Penggunaan Kolom
"""
Saat ini, Indonesia memiliki 8 komoditas budidaya unggulan, dengan komoditas yang paling banyak diproduksi adalah ikan nila, lele, dan udang.
"""

fig2 = go.Figure(
    go.Pie(
        labels = budidaya_produksi['Jenis_Ikan'],
        values = budidaya_produksi['Volume Produksi (Ton)'],
        hoverinfo = "value",
        textinfo = "label+percent"))
st.plotly_chart(fig2)

"""
Potensi produksi perikanan budidaya turut didukung dengan pasar yang sudah siap menerima dan dapat meningkatkan konsumsi 
ikan dalam negeri yang bertujuan untuk menjaga daya saing bangsa di masa depan. Adapun KKP menargetkan tingkat konsumsi 
ikan sebesar 62,05 kg/kapita pada 2024 mendatang (Laporan KKP 2020). Dalam satu dekade terakhir, peningkatan produksi 
perikanan selaras dengan peningkatan konsumsi ikan secara nasional yang ditunjukkan oleh Angka Konsumsi Ikan per kapita 
per tahun (kg) di Indonesia.
"""



df1 = pd.read_csv('produksi_konsumsi.csv')
# Plotting the firts line with ax axes

# Penggunaan Kolom
col3, col4= st.columns([1,1])

with col3:
    fig3, ax3 = plt.subplots(figsize=(10,8))
    lns1 = ax3.plot(df1['Tahun'], df1['Perikanan Budidaya'], color='g', linewidth=2, marker='o', label='Perikanan Budidaya')
    lns2 = ax3.plot(df1['Tahun'], df1['Perikanan Tangkap'], color='k', linewidth=2, marker='o', label='Perikanan Tangkap')
    lns3 = ax3.plot(df1['Tahun'], df1['Perikanan Total'], color='r', linewidth=2, marker='o', label='Perikanan Total')
    
    # Create a twin axes ax2 using twinx() function
    ax4 = ax3.twinx()
    
    # Now, plot the second line with ax2 axes
    lns4 = ax4.plot(df1['Tahun'], df1['Angka Konsumsi Ikan'], color='blue', linewidth=2, marker='*', label='total AKI')
    
    # added these four lines
    lns = lns1+lns2+lns3+lns4
    labs = [l.get_label() for l in lns]
    ax3.legend(lns, labs, loc='best')
    
    ax3.set_xlabel('Tahun', fontsize=10)
    ax3.set_ylabel('Produksi Perikanan (Juta Ton)',fontsize=10)
    ax4.set_ylabel('Angka Konsumsi Ikan (Kg per Kapita)',fontsize=10)
    
    st.pyplot(fig3)

with col4:
    st.write("Tabel Korelasi Matriks")
    correlation_matrix = df1[['Perikanan Budidaya', 'Perikanan Tangkap', 'Perikanan Total','Angka Konsumsi Ikan']].corr()
    st.dataframe(correlation_matrix)

"""
Dari grafik di atas dapat dilihat bahwa selama 10 tahun terakhir, angka konsumsi ikan nasional terus mengalami peningkatan.
Angka konsumsi ikan nasional pada tahun 2020 sebesar 56,39 kg/kapita. Angka ini naik 3,47% dibanding tahun sebelumnya yang 
sebesar 54,5 kg/kapita. Jika dibandingkan pada 2010, maka angka konsumsi ikan nasional telah meningkat hingga 80%, dengan 
angka konsumsi ikan tercatat hanya sebesar 30,48 kg/kapita pada tahun tersebut.
"""


"""
Dari tabel korelasi matriks di atas, kita menemukan fakta bahwa peningkatan produksi perikanan total berkorelasi positif 
dengan Angka Konsumsi Ikan (kg per kapita) secara nasional dari tahun 2010 hingga tahun 2020 dengan koefisien korelasi 
sebesar 0.82. Data ini juga menunjukkan peningkatan produksi perikanan budidaya yang menjadi fokus pemerintah dan 
perusahaan budidaya ikan berkorelasi positif dengan Angka Konsumsi Ikan (kg per kapita) dengan koefisien korelsi sebesar 0.78. 
Keduanya menunjukkan korelasi kuat karena nilai koefisien korelasi di atas 7. Dengan demikian, selain untuk ekspor, 
jumlah konsumsi produk perikanan nasional di angka ~60 kg/kapita menunjukkan bahwa Indonesia juga siap menerima hasil 
peningkatan produksi perikanan untuk konsumsi dalam negeri.
"""
"""
Meskipun tren konsumsi ikan nasional selama 5 tahun terakhir (2016-2020) meningkat, tingkat konsumsi ikan nasional 
relatif lebih rendah dibandingkan negara ASEAN lainnya seperti Malaysia, Vietam, dan Myanmar. Dengan demikian, perlu 
dipelajari lebih lanjut bagaimana sebaran konsumsi ikan di Indonesia pada masing-masing kabupaten/kota.
"""

df = pd.read_csv('fish_geo.csv')


# Penggunaan Kolom
col5, col6= st.columns([1,1])
with col5:
    fig5, ax5 = plt.subplots()
    sns.distplot(
        df['Consumption'],
        ax = ax5)
    st.pyplot(fig5)

with col6:
    fig6, ax6 = plt.subplots()
    sns.distplot(
        df['Expenditure per Capita'],
        ax=ax6)
    st.pyplot(fig6)

# map rata-rata konsumsi ikan tiap kabupaten/kota
def display_map(df):
    map = folium.Map(location=[-0.789275,113.921326], zoom_start=4, scrollWheelZoom=False, tiles= 'CartoDB positron')
    choropleth = folium.Choropleth(
         geo_data='indonesia_cities.geojson',
         data=df,
         columns=('District','Consumption'),
         key_on='feature.properties.Name',
         line_opacity=0.8,
         highlight=True
    )
    choropleth.geojson.add_to(map)

    df = df.set_index('District')
    df.drop_duplicates(inplace=True)
    district_name = 'BANDA ACEH'

    for feature in choropleth.geojson.data['features']:
        district_name = feature['properties']['Name']
        feature['properties']['Country'] = 'Province : ' + str (feature['properties']['Province'])
        feature['properties']['Source'] = 'Fish Consumption: ' + str (df.loc[district_name, 'Consumption'] if district_name in list(df.index) else 'N/A')
        feature['properties']['Code'] = 'Level : ' + str (df.loc[district_name, 'Level'] if district_name in list(df.index) else 'N/A')      
        feature['properties']['Kind'] = 'Gap Expenditure Rate : ' + str (df.loc[district_name, 'Percentage'] if district_name in list(df.index) else 'N/A')  
    
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['Name','Country','Source','Code', 'Kind'], labels=False)
    )
    plt.set_loglevel('WARNING')

    st.map = st_folium(map, width=800, height=700)


#LOAD DATA SPASIAL
df = pd.read_csv('fish_geo.csv')

col7, col8= st.columns([4,2])
with col7:
    display_map(df)
with col8:
    st.write(df)


cap_map = """
Keterangan:\n
Fish Consumption: Rata-Rata Konsumsi Ikan per Kapita Seminggu (Satuan Komoditas)\n
Level: Tingkat Konsumsi Ikan\n
Gap Expenditure Rate: Rasio Pengeluaran Ikan dengan Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun) 
"""
st.caption(cap_map)

"""
Pertama, jika dilihat dari volume ikan yang dikonsumsi, maka wilayah Indonesia Timur memiliki nilai konsumsi tertinggi, sedangkan
nilai konsumsi terendah ditempati oleh provinsi Jawa Tengah. Kemudian, jika ditelisik lebih spesifik lagi 
berdasarkan kabupaten/kota, Samosir memiliki rata-rata konsumsi ikan per kapita tertinggi, yaitu 2,373 per kapita per seminggu.
Berdasarkan kategori tingkat konsumsi ikan yang dibagi ke dalam 3 kelas pada tabel di atas, ditemukan bahwa 52% persen kabupaten/kota 
berada pada konsumsi ikan rendah, 46,5% berada pada konsumsi ikan sedang, dan hanya sekitar 1,5% kabupaten/kota termasuk dalam konsumsi
ikan tinggi. \n
Kedua, minat sebagian besar masyarakat Indonesia untuk mengkonsumsi ikan masih rendah. Nilai 'Expenditure Ratio' merepresentasikan 
persentase pengeluaran untuk membeli ikan terhadap daya beli total masyarakat di suatu daerah, dimana rata-rata kabupaten/Kota di Pulau Jawa
memiliki persentase terkecil.
"""


st.subheader("Lalu, apa yang bisa dilakukan untuk meningkatkan konsumsi ikan di Indonesia?")

"""
Perlu ada penguatan konsumsi ikan di Pulau Jawa mengingat pulau tersebut merupakan kunci perekonomian nasional saat ini. 
Rendahnya konsumsi ikan masyarakat Indonesia khususnya di Pulau Jawa dapat disebabkan oleh preferensi 
konsumen yang cenderung untuk memilih konsumsi daging (Tengker, 2017). Oleh karena itu,
pemerintah dapat lebih menggalakkan lagi program Gerakan Memasyarakatkan Makan Ikan (Gemarikan) untuk menyadarkan masyarakat tentang
pentingnya konsumsi ikan.\n
Pemerintah bekerjasama dengan perusahaan budidaya perikanan untuk mengembangkan sistem logistik ikan 
nasional yang terintegrasi dengan menjamin kualitas ikan tetap baik sejak ditangkap hingga sampai ke pedagang di pasar, 
sehingga memperlancar akses masyarakat terhadap sumber- sumber ikan. \n
"""



SUB_TITLE = 'Sumber: Kementrian Kelautan dan Perikanan (KKP), Badan Pusat Statistik (BPS)'
st.caption(SUB_TITLE)

