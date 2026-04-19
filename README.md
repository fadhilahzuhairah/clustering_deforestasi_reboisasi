# clustering_deforestasi_reboisasi

🌍 Clustering Negara Berdasarkan Pola Deforestasi dan Reboisasi Global untuk Mendukung Kebijakan Lingkungan menggunakan Agglomerative

📌 Deskripsi Project
Project ini bertujuan untuk mengelompokkan negara-negara di dunia berdasarkan pola deforestasi dan reboisasi global menggunakan algoritma Agglomerative Clustering. Hasil clustering diharapkan dapat mendukung pengambilan kebijakan lingkungan yang lebih tepat sasaran.

🧠 Algoritma yang Digunakan
Algoritma Parameter Terbaik Silhouette Score Agglomerative ⭐k=3, linkage=complete0.9543, DBSCAN eps=1.180.8953,
K-Meansk=30.9278

✅ Algoritma terbaik: Agglomerative Clustering dengan kualitas cluster 95.43%


📊 Fitur Dashboard

📌 Ringkasan data (jumlah negara, cluster, kualitas)
🏆 Perbandingan 3 algoritma clustering
📊 Distribusi jumlah negara per cluster
🗺️ Peta persebaran cluster negara
📈 Profil rata-rata fitur per cluster
📉 Analisis fitur per cluster (box plot interaktif)
🌲 10 negara dengan deforestasi tertinggi
🌱 10 negara dengan reboisasi tertinggi
🧾 Data hasil clustering lengkap dengan fitur pencarian


🗂️ Struktur File
├── app.py                          # Dashboard Streamlit
├── requirements.txt                # Library yang dibutuhkan
├── hasil_clustering_negara_final.csv  # Hasil clustering
├── hasil_evaluasi_3_algoritma.csv  # Hasil evaluasi algoritma
├── global 1.csv                    # Dataset asli
└── Tugas_Final_Machine_Learning.ipynb  # Notebook Colab

⚙️ Fitur Model Terbaik

Forest_Cover_Mean
Forest_Area_to_Land_Ratio
Carbon_per_Forest_Area
Forest_Cover_Change_Ratio


🚀 Cara Menjalankan Secara Lokal

1. Clone repository ini

bash
git clone https://github.com/fadhilahzuhairah/clustering_deforestasi_reboisasi.git

2. Install library yang dibutuhkan

bash
pip install -r requirements.txt

3. Jalankan dashboard

bash
streamlit run app.py (usahakan tujuan lokasi nya sudah benar)

🌐 Link Dashboard / streamlit
🔗 https://clusteringdeforestasireboisasi-rfjzwgr3mxycm7msgb7sg2.streamlit.app/

👩‍💻 Author
Fadhilah Zuhairah
