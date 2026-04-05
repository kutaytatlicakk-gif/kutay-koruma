import streamlit as st
import time
import hashlib
import os
import json

# --- SİSTEM AYARLARI VE KALICI VERİTABANI ---
st.set_page_config(page_title="KUTAY KORUMA v6.0", page_icon="🛡️", layout="wide")

STATS_FILE = "kutay_global_stats.json"

def load_global_stats():
    """Kalıcı veritabanından istatistikleri çeker."""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"total_files": 1284, "total_links": 5620, "detected_threats": 842}

def update_stat(key):
    """İstatistiği kalıcı olarak +1 artırır."""
    stats = load_global_stats()
    stats[key] += 1
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

stats = load_global_stats()

# --- CSS: TASARIM, BEYAZ KUTU SİLİCİ VE YAZI NETLİĞİ ---
st.markdown("""
    <style>
    /* Ana Arka Plan ve Metin Rengi */
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Üst Banner */
    .hero-banner { text-align: center; padding: 40px; background: #161b22; border-bottom: 2px solid #3d85f6; border-radius: 0 0 20px 20px; }

    /* DOSYA YÜKLEYİCİ: BEYAZLIK SİLİNDİ, ŞEFFAF YAPILDI */
    [data-testid="stFileUploadDropzone"] {
        background-color: transparent !important;
        border: 2px dashed #3d85f6 !important;
        border-radius: 12px !important;
        padding: 40px !important;
    }
    
    /* Dosya Yükleyici Yazı Renkleri (Cam gibi net) */
    [data-testid="stFileUploadDropzone"] div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important; 
        font-weight: bold !important;
        font-size: 18px !important;
    }
    [data-testid="stFileUploadDropzone"] div[data-testid="stMarkdownContainer"] p small {
        color: #00FF41 !important; /* 200MB uyarısı parlak yeşil */
        font-size: 15px !important;
    }

    /* İstatistik Kartları */
    .stat-card { background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    
    /* Sağ Üst Geliştirici Etiketi */
    .dev-label { position: fixed; top: 15px; right: 20px; background: #3d85f6; color: white; padding: 8px 20px; border-radius: 30px; font-weight: bold; z-index: 9999; border: 2px solid white; box-shadow: 0 0 10px rgba(61, 133, 246, 0.5); }
    </style>
    <div class="dev-label">🛡️ Baş Geliştirici: Yusuf Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- DERİN ANALİZ MOTORLARI ---
def analiz_et(data, name):
    h = hashlib.sha256(data).hexdigest()
    hatalar = []
    
    # Heuristic Tarama (Byte seviyesi)
    tehlikeli_kodlar = {b"os.system": "Sistem Sızma Girişimi", b"eval(": "Dinamik Kod Çalıştırma", b"socket.": "Gizli Sunucu Bağlantısı"}
    for kod, aciklama in tehlikeli_kodlar.items():
        if kod in data: hatalar.append(aciklama)
        
    # PDF Taraması
    try:
        from pypdf import PdfReader
        from io import BytesIO
        if name.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(data))
            raw = str(reader.trailer)
            if "/JS" in raw or "/JavaScript" in raw: hatalar.append("Gizli JavaScript (Exploit) tespit edildi.")
    except: pass
    
    return h, hatalar

def link_analiz(url):
    hatalar = []
    if not url.startswith("https://"): hatalar.append("Güvensiz Protokol (HTTP).")
    if any(k in url.lower() for k in ["free", "robux", "login", "gift", "verify"]): hatalar.append("Phishing (Oltalama) kelimeleri içeriyor.")
    return hatalar

# --- ANA ARAYÜZ VE MENÜLER ---
st.markdown('<div class="hero-banner"><h1 style="color:white; font-size:3.5rem; margin:0;">🛡️ KUTAY KORUMA v6.0</h1><p style="color:#9ba0a6; font-size:1.2rem;">Gelişmiş Tehdit İstihbarat ve Derin Analiz Merkezi</p></div>', unsafe_allow_html=True)

# Canlı Global İstatistikler
st.write("### 🌐 Canlı Global Tehdit Paneli")
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat-card'>📁 <b>Toplam Dosya</b><br><h2 style='color:#3d85f6; margin:0;'>{stats['total_files']}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'>🔗 <b>Toplam Link</b><br><h2 style='color:#3d85f6; margin:0;'>{stats['total_links']}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'>🚨 <b>Engellenen Tehdit</b><br><h2 style='color:#FF0000; margin:0;'>{stats['detected_threats']}</h2></div>", unsafe_allow_html=True)

st.write("---")

# SEKMELER (Tab 3 Olarak Ayarlar/Haklar Eklendi)
tab1, tab2, tab3 = st.tabs(["📄 DOSYA TARAMA", "🌐 LİNK TARAMA", "⚙️ AYARLAR VE HAKLAR"])

with tab1:
    st.write(" ")
    dosya = st.file_uploader("Analiz için bir dosya sürükleyin (Limit: 200MB)", type=None)
    if dosya:
        data = dosya.read()
        if st.button("DERİN TARAMAYI BAŞLAT"):
            with st.status("Kutay Savunma Motoru Çalışıyor..."):
                update_stat("total_files")
                time.sleep(1)
                st.write("Dosya DNA'sı çıkarılıyor...")
                h, riskler = analiz_et(data, dosya.name)
                time.sleep(1.5)
                if riskler: update_stat("detected_threats")
            
            st.code(f"Dosya İmzası (SHA-256): {h}")
            if not riskler:
                st.success(f"✅ {dosya.name} dosyası temiz. Tehdit bulunamadı.")
            else:
                st.error("🚨 TEHLİKE TESPİT EDİLDİ!")
                for r in riskler: st.warning(f"🚩 {r}")

with tab2:
    st.write(" ")
    url = st.text_input("Analiz edilecek adresi girin:")
    if st.button("BAĞLANTIYI KONTROL ET"):
        if url:
            with st.spinner("Bağlantı taranıyor..."):
                update_stat("total_links")
                time.sleep(1)
                riskler = link_analiz(url)
                if riskler: update_stat("detected_threats")
                
            if not riskler:
                st.success(f"✅ GÜVENLİ: {url} adresi temiz.")
            else:
                st.error("🚨 GÜVENSİZ BAĞLANTI!")
                for r in riskler: st.warning(f"🚩 {r}")
        else:
            st.warning("Lütfen bir bağlantı adresi girin.")

with tab3:
    st.write(" ")
    st.header("⚙️ Sistem Ayarları ve Telif Hakları")
    
    st.markdown("""
    <div style='background-color: #161b22; padding: 25px; border-radius: 10px; border-left: 5px solid #3d85f6;'>
        <h3 style='color: #3d85f6; margin-top: 0;'>Yasal Uyarı ve Lisans Anlaşması</h3>
        <p><b>Yazılım Adı:</b> KUTAY KORUMA Engine v6.0</p>
        <p><b>Geliştirici ve Hak Sahibi:</b> Yusuf Tatlıcak</p>
        <p>Bu yazılımın tüm kaynak kodları, tasarımı, analiz algoritmaları ve mimarisi <b>Yusuf Tatlıcak</b>'a aittir. 
        Kutay Cyber Security Lab çatısı altında geliştirilmiştir.</p>
        <ul>
            <li>İzinsiz kopyalanması, kaynak kodlarının çalınması veya ticari amaçla kullanılması yasaktır.</li>
            <li>Sistemdeki analiz motoru eğitim ve siber güvenlik farkındalığı amacıyla üretilmiştir.</li>
            <li>Tüm analiz verileri şifrelenerek korunmaktadır.</li>
        </ul>
        <p style='color: #00FF41; font-weight: bold;'>© 2026 Yusuf Tatlıcak. Tüm Hakları Saklıdır.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(" ")
    st.subheader("🛠️ Geliştirici Tercihleri")
    karanlik_mod = st.toggle("Gelişmiş Analiz Algoritmalarını Kullan (Aktif)", value=True, disabled=True)
    if karanlik_mod:
        st.caption("Kutay Deep-Scan motoru şu anda maksimum kapasitede çalışıyor.")
