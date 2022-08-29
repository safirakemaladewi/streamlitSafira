import pty
import streamlit as st
import numpy as np
import pandas as pd
import lorem
import altair as alt
from vega_datasets import data
import seaborn as sns
import matplotlib.pyplot as plt
from numerize import numerize
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from vega_datasets import data
import warnings
warnings.filterwarnings('ignore')

#Title
st.markdown("<h1 style='text-align: center; color: black;'>Menelisik Potensi Pasar Sektor Perikanan Indonesia</h1>", unsafe_allow_html=True)
st.markdown("---")


intro = st.container()

with intro:
    st.subheader('Latar Belakang')
    st.write("""
Sebagai negara kepulauan terbesar di dunia, Indonesia memiliki berbagai macam potensi ekosistem pesisir dan laut diantaranya 
sumber daya perikanan. Indonesia dikenal sebagai salah satu surga perikanan dunia dan produsen ikan terbesar di Asia Tenggara.
Sumber daya ini mempunyai nilai protein yang tinggi sehingga ikan dapat menjadi sumber protein hewani utama untuk masa depan. 
Potensi produksi perikanan budidaya di Indonesia mencapai 100 juta ton/tahun dengan nilai produksi mencapai USD 251 Miliar 
(Dahuri, 2019) dengan potensi ekonomi sektor kelautan perikanan mencapai 1.6 kali lipat PDB Nasional. Namun sayangnya, 
meskipun potensi dan pemanfaatan sumber daya perikanan relatif tinggi, **tingkat konsumsi 
ikan masyarakat Indonesia tertinggal jauh di bawah negara-negara lain yang memiliki potensi sumber daya perikanan yang jauh 
lebih kecil**. 
"""
    )

st.subheader('Perkembangan Sektor Perikanan Indonesia')

#Load Data
df = pd.read_csv("produksi_perikanan_provinsi.csv")

df = df.rename(columns = {'Volume_Produksi': 'Volume Produksi (Ton)', 'Jenis_Usaha' : 'Jenis Usaha', 'Jenis_Ikan' : 'Jenis Ikan'})

# Data Cleaning
df_nan = df[(df['Volume Produksi (Ton)']==0.0) & (df['Nilai_Produksi']==0.0)]
df.drop(df_nan.index, inplace=True)

df['Tahun'] = df['Tahun'].astype('str')

# Data Exploration
# Graph 1
df1 = df[['Jenis Usaha', 'Tahun', 'Volume Produksi (Ton)', 'Nilai_Produksi']]
df1 = df1[['Jenis Usaha','Tahun','Volume Produksi (Ton)']].groupby(['Jenis Usaha','Tahun'], as_index=False).sum()

"""
"""


# Penggunaan Kolom
graph1 = st.container()
with graph1:
    c = alt.Chart(df1, title="Produksi Akuakultur di Indonesia", height=400, width=750).mark_bar().encode(
        x='Tahun',
        y='Volume Produksi (Ton)',
        color='Jenis Usaha',
        tooltip=['Tahun', 'Volume Produksi (Ton)', 'Jenis Usaha']
        )
    lines = alt.Chart(df1).mark_line(color='red').encode(
            x='Tahun',
            y = 'max(Volume Produksi (Ton))'
            )
    st.altair_chart((c + lines).interactive(),use_container_width=True)

text1 = st.container()
with text1:
    st.write("""
    Grafik di samping menunjukkan bahwa jumlah **produksi perikanan budidaya dan tangkap di Indonesia meningkat dalam 
    satu dekade terakhir**, dari tahun 2010 sebesar 11,66 juta Ton hingga mencapai 21,83 juta ton pada tahun 2020 dengan 
    tingkat pertumbuhan sebesar 87,22%. Akan tetapi, produksi perikanan Indonesia mulai mengalami penurunan sejak tahun 2018.
    
    Berdasarkan data Badan Pusat Statistik (BPS) tahun 2020, kontribusi sub-sektor perikanan terhadap 
    total PDB Indonesia adalah 2,78% atau meningkat sebesar 0,13% dari tahun 2019. Hal ini menunjukkan sub-sektor perikanan
    tetap mengalami peningkatan meskipun pandemi COVID-19 cukup memukul pertumbuhan ekonomi Indonesia secara keseluruhan. 
            
    Lebih lanjut, produktivitas sektor akuakultur Indonesia tidak mengalami penurunan yang cukup signifikan akibat pandemi, 
    dengan proporsi produksi perikanan budidaya lebih besar dibandingkan perikanan tangkap. Pada tahun 2020, subsektor budidaya (akuakultur) 
    Indonesia berkisar 14,85 juta Ton, sedangkan subsektor tangkap berkisar 7 juta Ton.
    """)

# data exploration for graph 2
df_budidaya_2020 = df[(df['Jenis Usaha']=='BUDIDAYA') & (df['Tahun']=='2020')]
budidaya_produksi = df_budidaya_2020[['Jenis Ikan', 'Volume Produksi (Ton)']].groupby(['Jenis Ikan'], as_index=False).sum()
budidaya_produksi = budidaya_produksi.drop(31)
budidaya_produksi.sort_values(by=['Volume Produksi (Ton)'], axis=0, ascending=False, inplace=True, ignore_index=True)
budidaya_produksi = budidaya_produksi.drop(labels=range(8,40), axis=0)

"""
Saat ini, Indonesia memiliki 8 komoditas budidaya perikanan unggulan, dengan komoditas yang paling banyak diproduksi adalah 
ikan nila, lele, dan udang.
"""

fig2 = go.Figure(
    go.Pie(
        labels = budidaya_produksi['Jenis Ikan'],
        values = budidaya_produksi['Volume Produksi (Ton)'],
        hoverinfo = "value",
        textinfo = "label+percent"))
st.plotly_chart(fig2)


st.subheader('Hubungan Konsumsi dan Produksi Ikan di Indonesia')
"""
Potensi produksi perikanan budidaya turut didukung dengan pasar yang sudah siap menerima dan dapat meningkatkan konsumsi 
ikan dalam negeri yang bertujuan untuk menjaga daya saing bangsa di masa depan. Adapun KKP menargetkan tingkat konsumsi 
ikan sebesar 62,05 kg/kapita pada 2024 mendatang (Laporan KKP 2020). Dalam satu dekade terakhir, peningkatan produksi 
perikanan selaras dengan peningkatan konsumsi ikan secara nasional yang ditunjukkan oleh Angka Konsumsi Ikan per kapita 
per tahun (kg) di Indonesia.
"""

df2 = pd.read_csv('produksi_konsumsi.csv')
df2['Tahun'] = df2['Tahun'].astype(str)

# grafik perikanan budidaya 
base = alt.Chart(df2, title="Produksi Perikanan Budidaya dan Konsumsi Ikan (2010-2020)", height=300, width=700).encode(
    alt.X('Tahun', axis=alt.Axis(title='Tahun'))
)
line1 = base.mark_line(stroke='#5276A7', interpolate='monotone', point=alt.OverlayMarkDef(color="blue")).encode(
    x = 'Tahun',
    y = alt.Y('Perikanan Budidaya', 
    axis=alt.Axis(title='Perikanan Budidaya (Juta Ton)', titleColor='#5276A7'),
    scale=alt.Scale(domain=[0, 20])
    )

)

line2 = base.mark_line(stroke='#57A44C', interpolate='monotone', point=alt.OverlayMarkDef(color="green")).encode(
    y = alt.Y('Angka Konsumsi Ikan', 
    axis=alt.Axis(title='Angka Konsumsi Ikan (Kg per Kapita)', titleColor='#57A44C'),
    scale=alt.Scale(domain=[0, 60]))
)
pb = alt.layer(line1, line2).resolve_scale( y = 'independent')

# grafik perikanan tangkap
base2 = alt.Chart(df2, title="Produksi Perikanan Tangkap dan Konsumsi Ikan (2010-2020)", height=300, width=700).encode(
    alt.X('Tahun', axis=alt.Axis(title='Tahun'))
)
line3 = base2.mark_line(stroke='#5276A7', interpolate='monotone', point=alt.OverlayMarkDef(color="blue")).encode(
    x = 'Tahun',
    y = alt.Y('Perikanan Tangkap', 
    axis=alt.Axis(title='Perikanan Tangkap (Juta Ton)', titleColor='#5276A7'),
    scale=alt.Scale(domain=[0, 9])
    )
)

line4 = base2.mark_line(stroke='#57A44C', interpolate='monotone', point=alt.OverlayMarkDef(color="green")).encode(
    y = alt.Y('Angka Konsumsi Ikan', 
    axis=alt.Axis(title='Angka Konsumsi Ikan (Kg per Kapita)', titleColor='#57A44C'),
    scale=alt.Scale(domain=[0, 60]))
)
pt = alt.layer(line3, line4).resolve_scale(y = 'independent')

# grafik perikanan total
base3 = alt.Chart(df2, title="Produksi Perikanan Total dan Konsumsi Ikan (2010-2020)", height=300, width=700).encode(
    alt.X('Tahun', axis=alt.Axis(title='Tahun'))
)
line5 = base3.mark_line(stroke='#5276A7', interpolate='monotone', point=alt.OverlayMarkDef(color="blue")).encode(
    x = 'Tahun',
    y = alt.Y('Perikanan Total', 
    axis=alt.Axis(title='Perikanan Total (Juta Ton)', titleColor='#5276A7'),
    scale=alt.Scale(domain=[0, 27])
    )
)

line6 = base3.mark_line(stroke='#57A44C', interpolate='monotone', point=alt.OverlayMarkDef(color="green")).encode(
    y = alt.Y('Angka Konsumsi Ikan', 
    axis=alt.Axis(title='Angka Konsumsi Ikan (Kg per Kapita)', titleColor='#57A44C'),
    scale=alt.Scale(domain=[0, 60]))
)

ptot = alt.layer(line5, line6).resolve_scale(y = 'independent')

grafik = st.checkbox("Centang untuk melihat Grafik Produksi Perikanan Budidaya dan Angka Konsumsi Ikan (AKI)")

if grafik:
    pb_graph = st.altair_chart(pb,use_container_width=True)
else:
    ptot_graph = st.altair_chart(ptot,use_container_width=True)

df3 = df2.copy()

df3 = df3.rename(columns = {'Perikanan Budidaya': 'Budidaya', 'Perikanan Total' : 'Total', 'Angka Konsumsi Ikan' : 'AKI'})

col1, col2= st.columns([1,2])
# Correlation
with col1:
    correlation_matrix = df3[['Budidaya', 'Total', 'AKI']].corr()
    correlation_matrix 
with col2:
    st.write("""
    Selama 10 tahun terakhir, angka konsumsi ikan nasional terus mengalami peningkatan. Angka konsumsi ikan nasional pada 
    tahun 2020 sebesar 54,56 kg/kapita. Angka ini hanya naik 0,1% dibanding tahun 2019. Jika dibandingkan pada 2010, 
    maka angka konsumsi ikan nasional telah meningkat hingga 79%, dengan angka konsumsi ikan tercatat hanya sebesar 
    30,48 kg/kapita pada tahun tersebut. 
    """)

"""
Dari tabel korelasi matriks di atas, kita menemukan fakta bahwa peningkatan produksi perikanan total berkorelasi positif 
dengan Angka Konsumsi Ikan (kg per kapita) secara nasional dari tahun 2010 hingga tahun 2020 dengan koefisien korelasi sebesar 
0,82. Data ini juga menunjukkan adanya hubungan peningkatan produksi perikanan budidaya, yang menjadi fokus pemerintah dan 
perusahaan budidaya, dengan Angka Konsumsi Ikan (kg per kapita) dengan koefisien korelasi sebesar 0,78. 
Keduanya menunjukkan korelasi kuat karena nilai koefisien korelasi > 7. **Oleh karena itu, dapat disimpulkan bahwa
selain untuk ekspor, jumlah konsumsi produk perikanan nasional di angka ~60 kg/kapita menunjukkan Indonesia juga siap menerima hasil 
peningkatan produksi perikanan untuk konsumsi dalam negeri.**
"""

st.subheader('Menelisik Potensi Pasar Produk Perikanan di Indonesia')

"""
Meskipun angka produksi dan konsumsi ikan mengalami tren peningkatan selama satu dekade terakhir. Akan tetapi, tingkat konsumsi ikan
nasional relatif lebih rendah dibandingkan negara ASEAN lainnya, seperti Malaysia, Vietnam, dan Myanmar. Jika masyarakat Indonesia bisa
meningkatkan konsumsi produk perikanan hingga setidaknya setara dengan negara-negara tersebut, maka sektor perikanan di Indonesia
akan bertumbuh lebih besar lagi. **Dengan demikian, perlu dipelajari lebih lanjut potensi pasar perikanan Indonesia melalui analisis
sebaran konsumsi ikan di Indonesia pada masing-masing kabupaten/kota, mengingat adanya disparitas penduduk dan kemampuan ekonomi setiap 
wilayah kabupaten/kota di Indonesia.**
"""

"""
Grafik di bawah menampilkan distribusi probabilitas kemungkinan masing-masing data Angka Konsumsi Ikan (AKI) dan Pengeluaran per Kapita di Indonesia.
Berdasarkan visualiasi yang ditampilkan serta uji normalitas diperoleh informasi bahwa kedua data tersebut tidak terdistribusi normal (p-value < 0,05). Hal ini turut memvalidasi bahwa konsumsi ikan di Indonesia tidak merata antar wilayah.
"""


df4 = pd.read_csv('fish_geo.csv')
# Penggunaan Kolom
col5, col6= st.columns([1,1])
with col5:
    fig5, ax5 = plt.subplots()
    sns.distplot(
        df4['Consumption'],
        ax = ax5)
    st.pyplot(fig5)

with col6:
    fig6, ax6 = plt.subplots()
    sns.distplot(
        df4['Expenditure per Capita'],
        ax=ax6)
    st.pyplot(fig6)

"""
Peta di bawah memvisualisasikan tingkat konsumsi ikan di kabupaten/kota Indonesia yang terbagi menjadi 3 kategori: rendah, sedang, 
dan tinggi. Terdapat data tambahan berupa Expenditure Ratio (Rasio Pengeluaran Konsumsi Ikan terhadap Pengeluaran Total) yang juga
berkorelasi dengan tingkat konsumsi ikan di setiap wilayah. 
"""

# map rata-rata konsumsi ikan tiap kabupaten/kota
def display_map(df_fish):
    map = folium.Map(location=[-0.789275,113.921326], zoom_start=4, scrollWheelZoom=False, tiles= 'CartoDB positron')
    choropleth = folium.Choropleth(
         geo_data='indonesia_cities.geojson',
         data=df_fish,
         columns=('District','Consumption'),
         key_on='feature.properties.Name',
         line_opacity=0.8,
         highlight=True
    )
    choropleth.geojson.add_to(map)

    df_fish = df_fish.set_index('District')
    df_fish.drop_duplicates(inplace=True)
    district_name = 'BANDA ACEH'

    for feature in choropleth.geojson.data['features']:
        district_name = feature['properties']['Name']
        feature['properties']['Country'] = 'Province : ' + str (feature['properties']['Province'])
        feature['properties']['Source'] = 'Fish Consumption: ' + str (df_fish.loc[district_name, 'Consumption'] if district_name in list(df_fish.index) else 'N/A')
        feature['properties']['Code'] = 'Level : ' + str (df_fish.loc[district_name, 'Level'] if district_name in list(df_fish.index) else 'N/A')      
        feature['properties']['Kind'] = 'Expenditure Ratio : ' + str (df_fish.loc[district_name, 'Percentage'] if district_name in list(df_fish.index) else 'N/A')  
    
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['Name','Country','Source','Code', 'Kind'], labels=False)
    )
    plt.set_loglevel('WARNING')

    st.map = st_folium(map, width=800, height=400)


#LOAD DATA SPASIAL
df_fish= pd.read_csv('fish_geo.csv')

display_map(df_fish)
cap_map = """
Keterangan: Fish Consumption: Rata-Rata Konsumsi Ikan per Kapita Seminggu (Satuan Komoditas) | Level: Tingkat Konsumsi Ikan | 
Expenditure Ratio: Rasio Pengeluaran Ikan dengan Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun) | AKI: Angka Konsumsi Ikan (Kg/Kapita/Tahun) pada setiap Provinsi
"""
st.caption(cap_map)

"""
Pertama, jika dilihat dari volume ikan yang dikonsumsi, maka wilayah Indonesia Timur memiliki nilai konsumsi tertinggi, sedangkan
nilai konsumsi terendah ditempati oleh provinsi Jawa Tengah. Kemudian, jika ditelisik lebih spesifik lagi 
berdasarkan kabupaten/kota, Samosir memiliki rata-rata konsumsi ikan per kapita tertinggi, yaitu 2,373 per kapita per seminggu.
Berdasarkan kategori tingkat konsumsi ikan yang dibagi ke dalam 3 kelas pada tabel di atas, ditemukan bahwa 52% persen kabupaten/kota 
berada pada konsumsi ikan rendah, 46,5% berada pada konsumsi ikan sedang, dan hanya sekitar 1,5% kabupaten/kota termasuk dalam konsumsi
ikan tinggi. \n
"""
df_chart = pd.read_csv("piechart.csv")
fig8 = go.Figure(
    go.Pie(
        labels = df_chart['Level'],
        values = df_chart['Count'],
        hoverinfo = "value",
        textinfo = "label+percent"))
st.plotly_chart(fig8)

"""
Kedua, **minat sebagian besar masyarakat Indonesia untuk mengkonsumsi ikan masih rendah**. Nilai 'Expenditure Ratio' merepresentasikan 
persentase pengeluaran untuk membeli ikan terhadap daya beli total masyarakat di suatu daerah, dimana rata-rata kabupaten/Kota di Pulau Jawa
memiliki persentase terkecil. Akan tetapi, **hal tersebut justru menunjukkan besarnya potensi pasar perikanan di wilayah yang memiliki Expenditure
Ratio rendah, khususnya di wilayah Pulau Jawa**. Dengan demikian, pelaku usaha perikanan di Indonesia harus menyusun strategi yang efektif dalam
melakukan penetrasi pasar dan mempromosikan produk perikanan di tengah masyarakat. 
"""

st.subheader("Lalu, apa yang bisa dilakukan oleh stakeholder sektor perikanan di Indonesia?")

"""
Tingkat konsumsi ikan nasional telah mencapai level 54,56 kg/kapita tahun 2020, namun rata-rata tingkat konsumsi ikan di Pulau Jawa 
masih berada pada level rendah. Maka dari itu, perlu adanya penguatan konsumsi ikan per kapita di Pulau Jawa mengingat pulau tersebut merupakan 
kunci perekonomian nasional saat ini.

Di samping itu, hal ini sejatinya menjadi perbaikan serius dari sektor hulu (Produsen), industri pengolahan, perusahaan perikanan/distributor produk perikanan, 
startup perikanan, dan masyarakat itu sendiri untuk menciptakan daya saing produk perikanan. Maka dari itu, direkomendasikan untuk melakukan langkah-langkah strategis, 
seperti meningkatkan infrastruktur untuk memperbaiki kualitas dan ketersediaan komoditas makanan laut, menetapkan peraturan pemerintah terkait praktik perikanan 
berkelanjutan untuk meningkatkan ketersediaan, keberlanjutan dan kualitas ikan yang didukung oleh masyarakat lokal dan pemerintah daerah. Hal ini bertujuan tidak 
hanya untuk peningkatan konsumsi ikan domestik, namun juga efisiensi rantai pasokan produk perikanan. Dengan adanya efisiensi ini, 
bukan hanya sektor hulu, seperti produsen bisa memasarkan dan perusahaan ikan dapat meningkatkan profit, tetapi masyarakat sendiri juga 
bisa mendapatkan harga ikan yang lebih kompetitif dan variasi jenis ikan lebih banyak dan berkualitas. 

"""

SUB_TITLE = 'Sumber: Kementrian Kelautan dan Perikanan (KKP), Badan Pusat Statistik (BPS)'
st.caption(SUB_TITLE)
