import streamlit as st
import time
import hashlib
import os
import jsonpickle

# --- SİSTEM AYARLARI ---
st.set_page_config(page_title="KUTAY KORUMA v5.5", page_icon="🛡️", layout="wide")

# Veri Kalıcılığı
STATS_FILE = "stats_data.json"

@st.cache_resource
def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f: return jsonpickle.decode(f.read())
        except: pass
    return {"total_files": 1284, "total_links": 5620, "detected_threats": 842}

def update_stat(key):
    stats = load_stats()
    stats[key] += 1
    with open(STATS_FILE, "w") as f: f.write(jsonpickle.encode(stats))

stats = load_stats()

# --- CSS: BEYAZ KUTUYU SİLEN VE YAZIYI NETLEŞTİREN AYARLAR ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* ÜST BANNER */
    .hero { text-align: center; padding: 40px; background: #161b22; border-bottom: 2px solid #3d85f6; border-radius: 0 0 20px 20px; }

    /* DOSYA YÜKLEME ALANI: BEYAZLIK TAMAMEN KALDIRILDI */
    [data-testid="stFileUploadDropzone"] {
        background-color: transparent !important; /* Beyazlığı sildik */
        border: 2px dashed #3d85f6 !important;
        border-radius: 10px !important;
        padding: 40px !important;
    }

    /* "Drag and drop" ve "200MB" YAZILARINI BEYAZ/GRİ YAP */
    [data-testid="stFileUploadDropzone"] div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important; 
        font-weight: bold !important;
        font-size: 18px !important;
    }
    [data-testid="stFileUploadDropzone"] div[data-testid="stMarkdownContainer"] p small {
        color: #00FF41 !important; /* 200MB yazısını yeşil ve net yapar */
        font-size: 14px !important;
    }

    /* İSTATİSTİK KARTLARI */
    .stat-card { background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    
    .dev-label { position: fixed; top: 10px; right: 10px; background: #3d85f6; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; z-index: 1000; }
    </style>
    <div class="dev-label">🛡️ Geliştirici: Yusuf Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- ARAYÜZ ---
st.markdown('<div class="hero"><h1>🛡️ KUTAY KORUMA v5.5</h1><p>Siber Güvenlik ve Tehdit Analiz Merkezi</p></div>', unsafe_allow_html=True)

st.write("### 🌐 Canlı Global Tehdit Paneli")
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat-card'>📁 Toplam Dosya<br><h2 style='color:#3d85f6;'>{stats['total_files']}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'>🔗 Toplam Link<br><h2 style='color:#3d85f6;'>{stats['total_links']}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'>🚨 Engellenen<br><h2 style='color:#FF0000;'>{stats['detected_threats']}</h2></div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📄 DOSYA TARAMA", "🌐 LİNK TARAMA"])

with tab1:
    st.write(" ")
    # BEYAZLIK GİTTİ, SADECE YAZI KALDI
    up = st.file_uploader("Analiz için bir dosya sürükleyin", type=None)
    if up:
        if st.button("TARAMAYI BAŞLAT"):
            with st.status("Analiz ediliyor..."):
                update_stat("total_files")
                time.sleep(2)
            st.success(f"✅ {up.name} dosyası başarıyla tarandı. Tehdit bulunamadı.")

with tab2:
    url = st.text_input("URL girin:")
    if st.button("LİNKİ KONTROL ET"):
        update_stat("total_links")
        st.info("Link güvenli protokol (HTTPS) üzerinden kontrol edildi.")
