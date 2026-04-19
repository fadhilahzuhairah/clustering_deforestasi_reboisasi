import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ------------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Clustering Negara - Deforestasi & Reboisasi",
    layout="wide"
)

# ------------------------------------------------------------------------------
# CSS STYLE
# ------------------------------------------------------------------------------
css_content = """
<style>
body {
    background-color: #fff8fc;
}
.main {
    background: linear-gradient(135deg, #ffe4f2, #e6f7ff);
}
h1, h2, h3 {
    color: #d63384;
    font-family: 'Trebuchet MS', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffd6ec, #dff6ff);
}
div.stButton > button {
    background-color: #ff99cc;
    color: white;
    border-radius: 12px;
    border: none;
}
[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.6);
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(214,51,132,0.08);
}
.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #d63384;
}
.metric-label {
    font-size: 0.9rem;
    color: #888;
}
</style>
"""
st.markdown(css_content, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# JUDUL
# ------------------------------------------------------------------------------
st.title("🌍 Clustering Negara Berdasarkan Pola Deforestasi dan Reboisasi Global untuk Mendukung Kebijakan Lingkungan menggunakan Agglomerative")

# ------------------------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------------------------
df = pd.read_csv('hasil_clustering_negara_final.csv')
df_eval = pd.read_csv('hasil_evaluasi_3_algoritma.csv')

# ------------------------------------------------------------------------------
# FITUR
# ------------------------------------------------------------------------------
model_features = [
    'Forest_Cover_Mean',
    'Forest_Area_to_Land_Ratio',
    'Carbon_per_Forest_Area',
    'Forest_Cover_Change_Ratio'
]

dashboard_features = [
    'Forest_Cover_Mean',
    'Net_Forest_Change_Mean',
    'Forest_Area_to_Land_Ratio',
    'Carbon_per_Forest_Area',
    'Deforestation_Intensity',
    'Afforestation_Intensity',
    'Forest_Cover_Change_Ratio',
    'Forest_Stability_Index'
]
dashboard_features = [f for f in dashboard_features if f in df.columns]

# ------------------------------------------------------------------------------
# INFO MODEL
# ------------------------------------------------------------------------------
best_algorithm = "Agglomerative"
best_param = "k=3, linkage=complete"
best_silhouette = 0.9543
best_quality = 95.43
best_n_clusters = 3

# ------------------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------------------
st.sidebar.header("🎀 Informasi Model")
st.sidebar.success(f"Algoritma Terbaik: {best_algorithm}")
st.sidebar.info(f"Parameter: {best_param}")
st.sidebar.info(f"Jumlah Cluster: {best_n_clusters}")
st.sidebar.info(f"Silhouette Score: {best_silhouette:.4f}")
st.sidebar.info(f"Kualitas Cluster: {best_quality:.2f}%")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Fitur Model Terbaik")
for i, feat in enumerate(model_features, 1):
    st.sidebar.markdown(f"**{i}.** {feat}")

st.sidebar.markdown("---")
cluster_options = sorted(df['Cluster'].dropna().unique().tolist())
selected_clusters = st.sidebar.multiselect(
    "Pilih Cluster",
    cluster_options,
    default=cluster_options
)

df_filtered = df[df['Cluster'].isin(selected_clusters)]

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data untuk cluster yang dipilih.")
    st.stop()

# ------------------------------------------------------------------------------
# RINGKASAN DATA
# ------------------------------------------------------------------------------
st.markdown("## 📌 Ringkasan Data")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Jumlah Negara</div>
        <div class="metric-value">{}</div>
    </div>
    """.format(len(df_filtered)), unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Jumlah Cluster</div>
        <div class="metric-value">{}</div>
    </div>
    """.format(df_filtered['Cluster'].nunique()), unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Kualitas Cluster</div>
        <div class="metric-value">{:.2f}%</div>
    </div>
    """.format(best_quality), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PERBANDINGAN 3 ALGORITMA
# ------------------------------------------------------------------------------
st.markdown("## 🏆 Perbandingan 3 Algoritma")

best_per_algo = (
    df_eval
    .sort_values(
        by=['Algoritma', 'Silhouette', 'Davies_Bouldin', 'Calinski_Harabasz'],
        ascending=[True, False, True, False]
    )
    .groupby('Algoritma', as_index=False)
    .first()
)

st.dataframe(best_per_algo, use_container_width=True)

color_map = {'Agglomerative': '#1f77b4', 'DBSCAN': '#aec7e8', 'K-Means': '#d62728'}
fig_sil = px.bar(
    best_per_algo,
    x='Algoritma',
    y='Silhouette',
    color='Algoritma',
    color_discrete_map=color_map,
    text='Silhouette',
    title="Silhouette Score Terbaik per Algoritma"
)
fig_sil.update_traces(texttemplate='%{text:.4f}', textposition='outside')
fig_sil.update_layout(yaxis_range=[0, 1.05], showlegend=True)
st.plotly_chart(fig_sil, use_container_width=True)

# ------------------------------------------------------------------------------
# DISTRIBUSI CLUSTER
# ------------------------------------------------------------------------------
st.markdown("## 📊 Distribusi Cluster")

cluster_count = df_filtered['Cluster'].value_counts().sort_index().reset_index()
cluster_count.columns = ['Cluster', 'Jumlah']

fig_count = px.bar(
    cluster_count,
    x='Cluster',
    y='Jumlah',
    color='Cluster',
    text='Jumlah',
    title="Distribusi Jumlah Negara per Cluster"
)
fig_count.update_traces(textposition='outside')
st.plotly_chart(fig_count, use_container_width=True)

# ------------------------------------------------------------------------------
# PETA PERSEBARAN NEGARA
# ------------------------------------------------------------------------------
st.markdown("## 🗺️ Peta Persebaran Negara")

fig_map = px.choropleth(
    df_filtered,
    locations="Country",
    locationmode='country names',
    color="Cluster",
    hover_name="Country",
    color_continuous_scale='Blues',
    title="Peta Persebaran Cluster Negara"
)
st.plotly_chart(fig_map, use_container_width=True)

# ------------------------------------------------------------------------------
# PROFIL RATA-RATA FITUR PER CLUSTER
# ------------------------------------------------------------------------------
st.markdown("## 📈 Profil Rata-rata Fitur per Cluster")

numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [c for c in numeric_cols if c != 'Cluster']

profil = df_filtered.groupby('Cluster')[numeric_cols].mean().reset_index()
st.dataframe(profil, use_container_width=True)

# ------------------------------------------------------------------------------
# ANALISIS FITUR PER CLUSTER
# ------------------------------------------------------------------------------
st.markdown("## 📉 Analisis Fitur per Cluster")

selected_feature = st.selectbox(
    "Pilih fitur yang ingin dianalisis",
    dashboard_features
)

fig_box = px.box(
    df_filtered,
    x='Cluster',
    y=selected_feature,
    color='Cluster',
    points='all',
    title=f"Distribusi {selected_feature} per Cluster"
)
st.plotly_chart(fig_box, use_container_width=True)

# ------------------------------------------------------------------------------
# NEGARA DEFORESTASI TERTINGGI
# ------------------------------------------------------------------------------
st.markdown("## 🌲 Negara dengan Deforestasi Tertinggi")

if 'Deforestation_Mean' in df_filtered.columns:
    top_def = df_filtered.sort_values(by='Deforestation_Mean', ascending=False).head(10)

    fig_def = px.bar(
        top_def,
        x='Deforestation_Mean',
        y='Country',
        orientation='h',
        color='Cluster',
        text='Deforestation_Mean',
        title="10 Negara dengan Deforestasi Tertinggi"
    )
    fig_def.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_def.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_def, use_container_width=True)
    st.dataframe(
        top_def[['Country', 'Cluster', 'Deforestation_Mean']],
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# NEGARA REBOISASI TERTINGGI
# ------------------------------------------------------------------------------
st.markdown("## 🌱 Negara dengan Reboisasi Tertinggi")

if 'Afforestation_Mean' in df_filtered.columns:
    top_aff = df_filtered.sort_values(by='Afforestation_Mean', ascending=False).head(10)

    fig_aff = px.bar(
        top_aff,
        x='Afforestation_Mean',
        y='Country',
        orientation='h',
        color='Cluster',
        text='Afforestation_Mean',
        title="10 Negara dengan Reboisasi Tertinggi"
    )
    fig_aff.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_aff.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_aff, use_container_width=True)
    st.dataframe(
        top_aff[['Country', 'Cluster', 'Afforestation_Mean']],
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# DATA HASIL CLUSTERING
# ------------------------------------------------------------------------------
st.markdown("## 🧾 Data Hasil Clustering")

search_country = st.text_input("🔍 Cari Negara", "")
if search_country:
    df_show = df_filtered[df_filtered['Country'].str.contains(search_country, case=False, na=False)]
else:
    df_show = df_filtered

st.dataframe(df_show, use_container_width=True)
