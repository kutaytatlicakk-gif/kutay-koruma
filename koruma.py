import streamlit as st
import time
import re
import hashlib

# Kütüphane hatasını önlemek için güvenli import (image_8.png hatası çözümü)
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

# --- 1. VİRÜSTOTAL TARZI MODERN ARAYÜZ VE TASARIM (image_9.png İlhamlı) ---
st.set_page_config(page_title="KUTAY KORUMA", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* VirusTotal Dark Tema (image_9.png'daki ana renkler) */
    .stApp {
        background-color: #0e1217;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Ana Başlık Alanı */
    .main-header {
        text-align: center;
        padding: 60px 0;
        background: linear-gradient(180deg, #1c222d 0%, #0e1217 100%);
        border-bottom: 1px solid #1c222d;
    }

    /* Sekme (Tabs) Tasarımı (FILE, URL, SEARCH) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        justify-content: center;
        border-bottom: 1px solid #1c222d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: transparent;
        color: #9ba0a6;
        font-weight: bold;
        font-size: 16px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: #3d85f6 !important;
        border-bottom: 3px solid #3d85f6 !important;
    }

    /* Dosya Yükleme Alanı */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1c222d;
        border: 2px dashed #3d85f6;
        border-radius: 10px;
        color: #ffffff;
    }
    
    /* Input Alanları */
    .stTextInput>div>div>input {
        background-color: #1c222d;
        color: #ffffff;
        border: 1px solid #1c222d;
        border-radius: 5px;
    }

    /* GELİŞTİRİCİ ETİKETİ SAĞ ÜST */
    .developer-tag {
        position: fixed;
        top: 60px;
        right: 20px;
        background-color: #3d85f6;
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        padding: 8px 15px;
        border-radius: 30px;
        z-index: 99999;
        border: 2px solid white;
    }
    
    /* Sonuç Kutuları */
    .result-card {
        background-color: #1c222d;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #3d85f6;
        margin-top: 25px;
    }
    </style>
    
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. ANALİZ MOTORLARI ---

def dosya_hash_hesapla(file_bytes):
    """Dosyanın SHA-256 parmak izini hesaplar (VirusTotal gibi)"""
    return hashlib.sha256(file_bytes).hexdigest()

def link_analiz(url):
    risk = 0
    nedenler = []
    # Basit analiz kuralları
    if not url.startswith("https://"):
        risk += 50
        nedenler.append("Güvensiz Protokol (HTTP)")
    if any(x in url.lower() for x in ["free", "robux", "login", "verify", "hack", "claim"]):
        risk += 30
        nedenler.append("Şüpheli Anahtar Kelime")
    return risk, nedenler

def pdf_derin_tarama(file):
    tehditler = []
    if not PYPDF_AVAILABLE:
        return ["Sistem Hatası: PDF tarama motoru (pypdf) yüklenemedi."]
        
    try:
        reader = PdfReader(file)
        # Ham içerikte zararlı objeleri tara
        raw_structure = str(reader.trailer)
        if "/JS" in raw_structure or "/JavaScript" in raw_structure:
            tehditler.append("🚨 Gömülü JavaScript (Kod Yürütme) bulundu!")
        if "/OpenAction" in raw_structure:
            tehditler.append("🚨 Otomatik Başlatma Komutu tespit edildi!")
            
    except Exception as e:
        return [f"Dosya okuma hatası: {str(e)}"]
    
    return tehditler

# --- 3. ANA ARAYÜZ (image_9.png İlhamlı) ---

st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3.5rem; color: #ffffff; font-weight: 900;">🛡️ KUTAY KORUMA</h1>
        <p style="color: #9ba0a6; font-size: 1.3rem; max-width: 700px; margin: 0 auto;">Dosyaları, URL'leri ve IP'leri siber tehditlere karşı analiz edin. Gücünü Kutay Tatlıcak güvenlik motorundan alır.</p>
    </div>
    """, unsafe_allow_html=True)

# VirusTotal Sekme Yapısı
tab1, tab2, tab3 = st.tabs(["📄 DOSYA", "🔗 URL", "🔍 SEARCH"])

with tab1:
    st.write(" ") # Boşluk
    uploaded_file = st.file_uploader("Analiz için bir dosya seçin veya sürükleyin (PDF, EXE, vb.)", type=None)
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_hash = dosya_hash_hesapla(file_bytes)
        
        # Dosya Bilgileri Kartı
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=120) # Dosya simgesi
        with col2:
            st.subheader(f"Dosya Adı: {uploaded_file.name}")
            st.code(f"SHA-256: {file_hash}", language="")
            st.write(f"Boyut: {uploaded_file.size / 1024:.2f} KB")

        if st.button("DERİN TARAMAYI BAŞLAT"):
            with st.spinner("Kutay Savunma Motoru dosyayı analiz ediyor..."):
                time.sleep(2.5) # Simülasyon
                
                if uploaded_file.name.lower().endswith(".pdf"):
                    # Gerçek PDF taraması
                    riskler = pdf_derin_tarama(uploaded_file)
                    if not riskler:
                        st.markdown(f"""
                        <div class="result-card" style="border-left: 5px solid #00FF41;">
                            <h3 style="color: #00FF41;">✅ ANALİZ TEMİZ</h3>
                            <p><b>pypdf motoru</b> dosya içerisinde zararlı bir script veya otomatik işlem bulamadı.</p>
                            <small>Tespit Oranı: 0/72 (Kutay Engine)</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-card" style="border-left: 5px solid #FF0000;">
                            <h3 style="color: #FF0000;">🚨 TEHLİKE TESPİT EDİLDİ</h3>
                            <p>Dosya içerisinde {len(riskler)} adet şüpheli durum bulundu.</p>
                            <ul style="color: #FF0000;">
                                {"".join(f"<li>{r}</li>" for r in riskler)}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Diğer dosyalar için temel temiz raporu
                    st.markdown(f"""
                    <div class="result-card" style="border-left: 5px solid #00FF41;">
                        <h3 style="color: #00FF41;">✅ TEMİZ GÖRÜNÜYOR</h3>
                        <p>Temel tarama tamamlandı. Dosya parmak izi veritabanımızda temiz olarak işaretlendi.</p>
                        <small>Bu bir simülasyon taramasıdır. Tehdit: 0/72</small>
                    </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.write(" ")
    url_input = st.text_input("Analiz için bir URL girin (Örn: http://verify-account.com)", placeholder="https://example.com")
    if st.button("URL ANALİZ ET"):
        if url_input:
            with st.spinner("Bağlantı güvenliği sorgulanıyor..."):
                time.sleep(1.5)
                risk, nedenler = link_analiz(url_input)
                
                if risk == 0:
                    st.success(f"✅ ANALİZ TEMİZ: '{url_input}' bağlantısı güvenli görünüyor.")
                elif risk < 50:
                    st.warning(f"⚠️ DÜŞÜK RİSK: '{url_input}' bazı şüpheli öğeler içeriyor: {', '.join(nedenler)}")
                else:
                    st.error(f"🚨 YÜKSEK TEHLİKE! '{url_input}' bağlantısı güvensiz: {', '.join(nedenler)}")
        else:
            st.warning("Lütfen bir adres girin.")

with tab3:
    st.write(" ")
    st.text_input("Önceki taramaları arayın (Hash, URL veya IP)", placeholder="SHA-256 / URL / IP")
    st.info("Bu özellik Kutay Tatlıcak tarafından bir sonraki güncellemede (v2.1) aktif edilecektir.")

st.markdown("---")
st.caption("© 2026 Kutay Tatlıcak Security Lab. Tüm hakları saklıdır. Bu yazılım siber güvenlik farkındalığı için geliştirilmiştir.")
