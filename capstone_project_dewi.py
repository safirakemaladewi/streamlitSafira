from cProfile import label
from datetime import datetime
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
import plotly.express as px
import time
import branca
import warnings
warnings.filterwarnings('ignore')

#Title
st.markdown("<h1 style='text-align: center; color: black;'>Menelisik Potensi Pasar Sektor Perikanan Indonesia</h1>", unsafe_allow_html=True)
st.markdown("---")

st.write("Streamlit App by [Safira Kemala Dewi](https://www.linkedin.com/in/safirakemaladewi/)")


intro = st.container()

with intro:
    st.write("""
Sebagai negara kepulauan terbesar di dunia, Indonesia memiliki berbagai macam potensi ekosistem pesisir dan laut diantaranya 
sumber daya perikanan. Indonesia dikenal sebagai produsen perikanan terbesar di Asia Tenggara dan produsen kedua terbesar 
secara global setelah China (FAO, 2020). Hasil perikanan dan hasil industri perikanan Indonesia menyumbang 2,73% dari produk 
domestik bruto Indonesia pada kuartal III/2020 (KKP, 2020). Potensi sumber daya perikanan yang sangat tinggi ini dapat memberikan 
kontribusi untuk memasok total kebutuhan konsumsi protein di Indonesia, khususnya sumber protein hewani. Namun sayangnya, 
**tingkat konsumsi ikan masyarakat Indonesia tertinggal jauh di bawah negara-negara lain yang memiliki potensi sumber daya perikanan 
yang jauh lebih kecil**. 

Lantas, bagaimana negeri maritim ini dapat meningkatkan potensi lautnya jauh lebih tinggi?
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
    st.metric(label="Produksi Perikanan", value="21,83 M", delta="87%")
    c = alt.Chart(df1, title="Produksi Perikanan di Indonesia", height=400, width=750).mark_bar().encode(
        x='Tahun',
        y='Volume Produksi (Ton)',
        color='Jenis Usaha',
        tooltip=['Tahun', 'Volume Produksi (Ton)', 'Jenis Usaha']
        )
    lines = alt.Chart(df1).mark_line(color='red', point=alt.OverlayMarkDef(color="red")).encode(
            x='Tahun',
            y = 'sum(Volume Produksi (Ton))'
            )
    st.altair_chart((c + lines).interactive(),use_container_width=True)
    st.caption("""
    <a style='display: block; text-align: center;color: black;' href="https://statistik.kkp.go.id/home.php">Sumber: Statistik Kementerian Kelautan dan Perikanan (KKP)</a>
    """,unsafe_allow_html=True)
text1 = st.container()
with text1:
    st.write("""
    Grafik di atas menunjukkan bahwa jumlah **produksi perikanan budidaya dan tangkap di Indonesia meningkat dalam 
    satu dekade terakhir**, dari tahun 2010 sebesar 11,66 juta ton hingga mencapai 21,83 juta ton pada tahun 2020 dengan 
    tingkat pertumbuhan sebesar 87,22%. Akan tetapi, produksi perikanan Indonesia mulai mengalami penurunan sejak tahun 2018.
    
    Berdasarkan data Badan Pusat Statistik (BPS) tahun 2020, kontribusi sub-sektor perikanan terhadap 
    total PDB Indonesia adalah 2,78% atau meningkat sebesar 0,13% dari tahun 2019. Hal ini menunjukkan sub-sektor perikanan
    tetap mengalami peningkatan meskipun pandemi COVID-19 cukup memukul pertumbuhan ekonomi Indonesia secara keseluruhan. 
            
    Lebih lanjut, produktivitas sektor akuakultur Indonesia tidak mengalami penurunan yang cukup signifikan akibat pandemi, 
    dengan proporsi produksi perikanan budidaya lebih besar dibandingkan perikanan tangkap. Pada tahun 2020, subsektor budidaya 
    Indonesia berkisar 15 juta ton, sedangkan subsektor tangkap hanya berkisar 7 juta ton.
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

fig1 = go.Figure(
    go.Pie(
        labels = budidaya_produksi['Jenis Ikan'],
        values = budidaya_produksi['Volume Produksi (Ton)'],
        hoverinfo = "value",
        textinfo = "label+percent"))
st.plotly_chart(fig1)
st.caption("""
    <a style='display: block; text-align: center;color: black;' href="https://statistik.kkp.go.id/home.php">Sumber: Statistik Kementerian Kelautan dan Perikanan (KKP)</a>
    """,unsafe_allow_html=True)


st.subheader('Hubungan Konsumsi dan Produksi Ikan di Indonesia')
"""
Dalam satu dekade terakhir, peningkatan produksi perikanan selaras dengan peningkatan konsumsi ikan secara nasional yang ditunjukkan oleh 
Angka Konsumsi Ikan per kapita per tahun (kg) di Indonesia. Angka konsumsi ikan diperoleh dari jumlah konsumsi rumah tangga (Konsumsi Ikan 
Dalam Rumah Tangga), konsumsi luar rumah tangga, dan konsumsi tidak tercatat. Adapun KKP menargetkan tingkat konsumsi ikan sebesar 62,05 
kg/kapita pada 2024 mendatang.
"""

df2 = pd.read_csv('produksi_konsumsi.csv')
df2['Tahun']=pd.to_datetime(df['Tahun'], format='%Y')



# grafik perikanan budidaya 
base = alt.Chart(df2, title="Produksi Perikanan Budidaya dan Konsumsi Ikan (2010-2020)", height=300, width=700).encode(
    alt.X('Tahun', axis=alt.Axis(title='Tahun'))
)

line1 = base.mark_line(stroke='#5276A7', interpolate='monotone', point=alt.OverlayMarkDef(color="blue")).encode(
    x = 'Tahun',
    y = alt.Y('Perikanan Budidaya', 
    axis=alt.Axis(title='Perikanan Budidaya (Juta Ton)', titleColor='#5276A7'),
    scale=alt.Scale(domain=[0, 20]))
)


line2 = base.mark_line(stroke='#57A44C', interpolate='monotone', point=alt.OverlayMarkDef(color="green")).encode(
    y = alt.Y('Angka Konsumsi Ikan', 
    axis=alt.Axis(title='Angka Konsumsi Ikan (Kg per Kapita)', titleColor='#57A44C'),
    scale=alt.Scale(domain=[0, 60]))
)



pb = alt.layer(
    line1,line2).resolve_scale( y = 'independent')

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

grafik = st.checkbox('Klik centang untuk melihat grafik "Produksi Perikanan Budidaya dan Angka Konsumsi Ikan"')

if grafik:
    pb_graph = st.altair_chart(pb,use_container_width=True)
else:
    ptot_graph = st.altair_chart(ptot,use_container_width=True)

st.caption("""
    <a style='display: block; text-align: center;color: black;' href="https://www.bps.go.id/subject/5/konsumsi-dan-pengeluaran.html#subjekViewTab3">Sumber: Badan Pusat Statistik (BPS)</a>
    """,unsafe_allow_html=True)
df3 = df2.copy()

df3 = df3.rename(columns = {'Perikanan Budidaya': 'Budidaya', 'Perikanan Total' : 'Total', 'Angka Konsumsi Ikan' : 'AKI'})

col1, col2= st.columns([1,2.5])
# Correlation
with col1:
    correlation_matrix = df3[['Budidaya', 'Total', 'AKI']].corr()
    correlation_matrix 
with col2:
    st.write(""" 
    Selama 10 tahun terakhir, angka konsumsi ikan nasional terus mengalami peningkatan. 
    Angka konsumsi ikan nasional pada tahun 2020 sebesar 54,56 kg/kapita. Angka ini hanya naik 0,1% dibanding tahun 2019. 
    Jika dibandingkan pada 2010, maka angka konsumsi ikan nasional telah meningkat hingga 79%, dengan angka konsumsi ikan tercatat 
    hanya sebesar 30,48 kg/kapita pada tahun tersebut. 
    """)

"""
Dari tabel korelasi matriks di atas, kita menemukan fakta bahwa peningkatan produksi perikanan total berkorelasi positif 
dengan Angka Konsumsi Ikan (kg per kapita) secara nasional dari tahun 2010 hingga tahun 2020 dengan koefisien korelasi senilai 
0,82. Data ini juga menunjukkan adanya hubungan peningkatan produksi perikanan budidaya, yang menjadi fokus pemerintah dan 
perusahaan budidaya, dengan Angka Konsumsi Ikan (kg per kapita) dengan koefisien korelasi senilai ~0,78. Keduanya menunjukkan 
korelasi kuat karena nilai koefisien korelasi > 0,7. **Oleh karena itu, dapat disimpulkan bahwa selain untuk ekspor, jumlah 
konsumsi produk perikanan nasional di angka ~60 kg/kapita menunjukkan pasar Indonesia yang juga sudah siap menerima hasil peningkatan 
produksi perikanan untuk konsumsi dalam negeri.**
"""

st.subheader('Menelisik Potensi Pasar Produk Perikanan di Indonesia')

"""
Meskipun angka produksi dan konsumsi ikan mengalami tren peningkatan selama satu dekade terakhir. Akan tetapi, tingkat konsumsi ikan
nasional relatif lebih rendah dibandingkan negara ASEAN lainnya, seperti Malaysia, Vietnam, dan Myanmar. Jika masyarakat Indonesia bisa
meningkatkan konsumsi produk perikanan hingga setidaknya setara dengan negara-negara tersebut, maka sektor perikanan di Indonesia
akan bertumbuh lebih besar lagi.
"""

df4 = pd.read_csv('fish_geo_year.csv')
df_zeroes = df4 [df4['Consumption']==0.0]
df4.drop(df_zeroes.index, inplace=True)
df4 = df4.sort_values(by='Year')

fig8 = px.scatter(
    df4, 
    x='Expenditure per Capita', 
    y= 'Consumption',
    labels={"Expenditure per Capita": "Expenditure per Capita (Thousand Rupiah/Year)",
            "Consumption": "Consumption per Capita (Commodity/Week)"},
    range_x= [3500,24000], range_y=[0,2.5],
    animation_frame='Year',animation_group='District',
    opacity=0.4, hover_data=['District']
    
    )

fig8.update_layout(width=800,height=500)
st.write(fig8)
st.caption("""
    <a style='display: block; text-align: center;color: black;' href="https://www.bps.go.id/indicator/26/416/1/-metode-baru-pengeluaran-per-kapita-disesuaikan.html">Sumber: Badan Pusat Statistik (BPS)</a>
    """,unsafe_allow_html=True)

st.write("""
**Dari pengamatan tahun 2018-2020, ternyata perilaku konsumsi ikan di Indonesia kurang berkorelasi dengan kemampuan daya beli masyarakat. 
Hal ini ditunjukkan dengan data pada kabupaten/kota yang memiliki pengeluaran tinggi justru kurang berminat mengkonsumsi ikan**.
Adanya disparitas penduduk dan perbedaan kemampuan ekonomi masyarakat di setiap kabupaten/kota membuat potensi pasar perikanan 
Indonesia harus dianalisis melalui sebaran konsumsi ikan pada masing-masing kabupaten/kota. 
""")

# Penggunaan Kolom
with st.expander("Histogram Konsumsi Ikan dan Pengeluaran per Kapita setiap Kabupaten/Kota di Indonesia"):
    st.write("""
    Berdasarkan uji normalitas serta grafik histogram yang ditampilkan di bawah ini, diperoleh informasi bahwa masing-masing data tersebut tidak terdistribusi normal (p-value < 0,05). 
    Hal ini turut memvalidasi bahwa konsumsi ikan di Indonesia tidak merata antar wilayah kabupaten/kota di Indonesia.
    """)
    col3, col4= st.columns([1,1])
    with col3:
        fig2, ax2 = plt.subplots()
        sns.distplot(df4['Consumption'],ax = ax2)
        st.pyplot(fig2)
        
    with col4:
        fig3, ax3= plt.subplots()
        sns.distplot(df4['Expenditure per Capita'],ax=ax3)
        st.pyplot(fig3)

"""
Peta di bawah memvisualisasikan tingkat konsumsi ikan di kabupaten/kota Indonesia yang terbagi menjadi 3 kategori: rendah, sedang, 
dan tinggi. Terdapat data tambahan berupa _Expenditure Ratio_ yang juga berkorelasi dengan tingkat konsumsi ikan di setiap wilayah. 
"""

# map rata-rata konsumsi ikan tiap kabupaten/kota
def display_map(df_fish):
    map = folium.Map(location=[-0.789275,113.921326], zoom_start=4, scrollWheelZoom=False, tiles= 'CartoDB positron')
    choropleth = folium.Choropleth(
         geo_data='indonesia_cities.geojson',
         data=df_fish,
         columns=('District','Consumption'),
         key_on='feature.properties.Name',
         fill_color= 'YlOrRd',
         fill_opacity=0.7,
         line_opacity=0.5,
         legend_name='Level',
         highlight=True
    )
    choropleth.geojson.add_to(map)

    colormap = branca.colormap.linear.YlOrRd_05.scale(0, 2.373)
    colormap = colormap.to_step(index=[0,0.791,1.582,2.373])
    colormap.caption = 'Sebaran Tingkat Konsumsi Ikan di Indonesia Tahun 2020'
    colormap.add_to(map)

    folium.LayerControl().add_to(map)

    df_fish = df_fish.set_index('District')
    df_fish.drop_duplicates(inplace=True)
    district_name = 'BANDA ACEH'

    for feature in choropleth.geojson.data['features']:
        district_name = feature['properties']['Name']
        feature['properties']['Country'] = 'Province : ' + str (feature['properties']['Province'])
        feature['properties']['Source'] = 'Fish Consumption: ' + str (df_fish.loc[district_name, 'Consumption'] if district_name in list(df_fish.index) else 'N/A')
        feature['properties']['Code'] = 'Level : ' + str (df_fish.loc[district_name, 'Level'] if district_name in list(df_fish.index) else 'N/A')      
        feature['properties']['Kind'] = 'Expenditure Ratio : ' + str (df_fish.loc[district_name, 'Expenditure Ratio'] if district_name in list(df_fish.index) else 'N/A')  
    
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['Name','Country','Source','Code', 'Kind'], labels=False)
    )
    plt.set_loglevel('WARNING')

    st.map = st_folium(map, width=800, height=400)


#LOAD DATA SPASIAL
df_fish= pd.read_csv('fish_geo1.csv')
df_fish = df_fish.rename(columns = {'AKI': '*AKI', 'Percentage': 'Expenditure Ratio'})


display_map(df_fish)
st.caption("""
    <a style='display: block; text-align: center;color: black;' href="https://statistik.kkp.go.id/home.php">Sumber: Statistik Kementerian Kelautan dan Perikanan (KKP)</a>
    """,unsafe_allow_html=True)
cap_map = """
Keterangan: Fish Consumption: Rata-Rata Konsumsi Ikan per Kapita Seminggu (Satuan Komoditas) | Level: Tingkat Konsumsi Ikan | 
Expenditure Ratio: Rasio Pengeluaran Ikan dengan Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun) | *AKI: Angka Konsumsi Ikan (Kg/Kapita/Tahun) setiap Provinsi
"""
st.caption(cap_map)
#st.write(df_fish)

"""
Pertama, jika dilihat dari volume ikan yang dikonsumsi, maka wilayah Indonesia Timur memiliki tingkat konsumsi ikan tertinggi, sedangkan
nilai konsumsi terendah ditempati oleh provinsi Jawa Tengah. Kemudian, jika ditelusuri lebih spesifik berdasarkan kabupaten/kota,
Samosir memiliki rata-rata konsumsi ikan per kapita tertinggi (2,373 per kapita seminggu).
Berdasarkan tingkat konsumsi ikan yang dibagi ke dalam 3 kategori pada tabel di atas, ditemukan bahwa **52% persen kabupaten/kota 
berada pada konsumsi ikan rendah**, 46,5% berada pada konsumsi ikan sedang, dan hanya sekitar 1,5% kabupaten/kota termasuk dalam konsumsi
ikan tinggi. \n
"""
df_chart = pd.read_csv("piechart.csv")
fig4 = go.Figure(
    go.Pie(
        labels = df_chart['Level'],
        values = df_chart['Count'],
        hoverinfo = "value",
        textinfo = "label+percent"))
st.plotly_chart(fig4)

"""
Kedua, **minat sebagian besar masyarakat Indonesia untuk mengkonsumsi ikan masih rendah**. Nilai _Expenditure Ratio_ (ER) merupakan
rasio antara pengeluaran beli ikan dengan pengeluaran atau daya beli total masyarakat di suatu daerah, dimana sebagian besar kabupaten/kota
di Pulau Jawa memiliki rasio terkecil. Akan tetapi, **hal tersebut justru menunjukkan besarnya potensi pasar perikanan di wilayah yang 
memiliki ER rendah, khususnya di wilayah Pulau Jawa**. Dengan demikian, pelaku usaha perikanan di Indonesia harus menyusun strategi yang 
efektif dalam melakukan penetrasi pasar dan mempromosikan produk perikanan di tengah masyarakat. 
"""

st.subheader("Lalu, apa yang bisa dilakukan oleh stakeholder sektor perikanan di Indonesia?")

"""
Tingkat konsumsi ikan nasional telah mencapai level 54,56 kg/kapita tahun 2020, namun rata-rata tingkat konsumsi ikan di Pulau Jawa 
masih berada pada level rendah. Maka dari itu, perlu adanya penguatan konsumsi ikan per kapita di Pulau Jawa mengingat pulau tersebut merupakan 
kunci perekonomian nasional saat ini.

Di samping itu, perlu ada perbaikan serius dari sektor hulu (produsen dan nelayan), industri pengolahan, industri perikanan dan 
distributor produk perikanan, startup perikanan, serta masyarakat itu sendiri untuk menciptakan daya saing produk perikanan Indonesia. 
Maka dari itu, direkomendasikan untuk melakukan langkah-langkah strategis, seperti meningkatkan infrastruktur untuk memperbaiki kualitas 
dan ketersediaan komoditas makanan laut, dan **tidak hanya konsumsi ikan domestik yang harus ditingkatkan, efisiensi rantai pasok produk 
perikanan juga harus dioptimalkan**. Dengan adanya efisiensi ini, bukan hanya sektor hulu yang bisa memasarkan produk dan meningkatkan profit, 
tetapi masyarakat sendiri juga bisa mendapatkan harga ikan yang lebih kompetitif dan variasi jenis ikan yang lebih banyak dan berkualitas. 
"""


