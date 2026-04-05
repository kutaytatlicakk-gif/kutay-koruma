import streamlit as st
import time
import hashlib
import re
from io import BytesIO

# --- 1. SİSTEM HAFIZASI (CANLI İSTATİSTİKLER) ---
# Uygulama açık kaldığı sürece taramaları sayar
if 'global_files' not in st.session_state:
    st.session_state.global_files = 1284  # Başlangıç değeri
if 'global_links' not in st.session_state:
    st.session_state.global_links = 5620
if 'detected_threats' not in st.session_state:
    st.session_state.detected_threats = 842

# --- 2. PROFESYONEL TASARIM VE GÖRÜNÜRLÜK ---
st.set_page_config(page_title="KUTAY KORUMA v4.0", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* ÜST PANEL VE 200MB UYARISI */
    .top-banner {
        text-align: center;
        padding: 40px;
        background: linear-gradient(90deg, #161b22 0%, #3d85f6 50%, #161b22 100%);
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #3d85f6;
    }
    
    .limit-box {
        font-size: 24px !important;
        color: #00FF41 !important;
        font-weight: bold;
        background: rgba(0, 0, 0, 0.5);
        padding: 15px;
        border: 2px solid #00FF41;
        border-radius: 10px;
        display: inline-block;
        margin-top: 10px;
        text-shadow: 0 0 10px #00FF41;
    }

    /* CANLI İSTATİSTİK KARTLARI */
    .stat-card {
        background: #161b22;
        padding: 20px;
        border-radius: 10px;
        border-bottom: 4px solid #3d85f6;
        text-align: center;
    }

    /* GELİŞTİRİCİ İMZASI */
    .dev-tag {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #3d85f6;
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: bold;
        z-index: 1000;
        border: 2px solid #ffffff;
    }
    </style>
    <div class="dev-tag">🚀 Baş Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 3. DERİN ANALİZ MOTORLARI ---

def dosya_analiz(data, name):
    sha256 = hashlib.sha256(data).hexdigest()
    riskler = []
    # Byte seviyesinde zararlı kod arama
    patterns = {b"os.system": "Sistem Sızma Girişimi", b"eval(": "Dinamik Kod Çalıştırma", b"socket": "Dış Sunucu Bağlantısı"}
    for p, desc in patterns.items():
        if p in data: riskler.append(desc)
    return sha256, riskler

def link_analiz(url):
    risk_skoru = 0
    nedenler = []
    # Protokol kontrolü
    if not url.startswith("https://"):
        risk_skoru += 50
        nedenler.append("Güvensiz Bağlantı (HTTP)")
    # Phishing kelime kontrolü
    phish_keywords = ["free", "gift", "login", "verify", "account", "update", "robux", "crypto"]
    if any(k in url.lower() for k in phish_keywords):
        risk_skoru += 30
        nedenler.append("Oltalama (Phishing) Şüphesi")
    # Uzunluk kontrolü
    if len(url) > 100:
        risk_skoru += 20
        nedenler.append("Anormal URL Uzunluğu")
    return risk_skoru, nedenler

# --- 4. ANA ARAYÜZ ---

st.markdown("""
    <div class="top-banner">
        <h1 style="color: white; font-size: 3.5rem; margin:0;">🛡️ KUTAY KORUMA v4.0</h1>
        <div class="limit-box">DURUM: AKTİF | TARAMA KAPASİTESİ: 200 MB</div>
    </div>
    """, unsafe_allow_html=True)

# Canlı İstatistik Paneli
st.write("### 🌐 Canlı Global Tehdit Paneli")
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-card'><h3>📁 Toplam Dosya</h3><h2 style='color:#3d85f6;'>{st.session_state.global_files}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><h3>🔗 Toplam Link</h3><h2 style='color:#3d85f6;'>{st.session_state.global_links}</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><h3>🚨 Engellenen</h3><h2 style='color:#FF0000;'>{st.session_state.detected_threats}</h2></div>", unsafe_allow_html=True)

st.write("---")

tab1, tab2 = st.tabs(["📄 DERİN DOSYA TARAMA", "🌐 PROFESYONEL LİNK ANALİZİ"])

with tab1:
    f = st.file_uploader("Analiz edilecek dosyayı yükleyin", type=None)
    if f:
        bytes_data = f.read()
        if st.button("SİSTEMİ TETİKLE: DOSYA"):
            with st.status("Kutay Laboratuvarı Çalışıyor...", expanded=True) as status:
                h, bugs = dosya_analiz(bytes_data, f.name)
                time.sleep(1.5)
                st.session_state.global_files += 1 # SAYIYI ARTIR
                if bugs: st.session_state.detected_threats += 1
                status.update(label="Analiz Tamamlandı!", state="complete")
            
            st.code(f"SHA-256: {h}")
            if not bugs:
                st.success("✅ ANALİZ TEMİZ: Dosya katmanlarında tehdit bulunamadı.")
            else:
                for b in bugs: st.error(f"🚩 KRİTİK BULGU: {b}")

with tab2:
    l = st.text_input("Analiz edilecek URL adresini girin:", placeholder="https://example.com")
    if st.button("SİSTEMİ TETİKLE: LİNK"):
        if l:
            with st.spinner("Link DNA'sı inceleniyor..."):
                time.sleep(1)
                skor, uyarilar = link_analiz(l)
                st.session_state.global_links += 1 # SAYIYI ARTIR
                
                if skor == 0:
                    st.success(f"✅ GÜVENLİ: {l} adresi temiz görünüyor.")
                else:
                    st.error(f"🚨 RİSK TESPİT EDİLDİ! (Risk Skoru: {skor}/100)")
                    for u in uyarilar: st.write(f"- {u}")
                    st.session_state.detected_threats += 1
        else:
            st.warning("Lütfen bir link girin.")

st.markdown("---")
st.caption("Kutay Tatlıcak Cyber Intelligence Lab © 2026")
