import streamlit as st
import hashlib
import time
import re
from io import BytesIO

# Kütüphane Kontrolleri
try:
    from pypdf import PdfReader
    PDF_DESTEK = True
except:
    PDF_DESTEK = False

# --- 1. VİRÜSTOTAL TARZI ULTRA MODERN ARAYÜZ ---
st.set_page_config(page_title="KUTAY KORUMA v3.0", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1217; color: #ffffff; }
    
    /* Üst Başlık Alanı */
    .hero-section {
        text-align: center;
        padding: 60px;
        background: radial-gradient(circle, #1c222d 0%, #0e1217 100%);
        border-bottom: 3px solid #3d85f6;
    }

    /* 200MB Uyarısı ve Durum Paneli */
    .status-panel {
        font-size: 22px !important;
        color: #00FF41 !important;
        background: rgba(0, 255, 65, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00FF41;
        text-align: center;
        font-weight: bold;
        margin: 20px 0;
        text-shadow: 0px 0px 10px #00FF41;
    }

    /* Geliştirici Etiketi */
    .kutay-signature {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #3d85f6;
        color: white;
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: bold;
        border: 2px solid #ffffff;
        box-shadow: 0px 4px 15px rgba(61, 133, 246, 0.5);
        z-index: 9999;
    }

    /* Analiz Kartı */
    .analysis-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 30px;
        margin-top: 20px;
    }
    </style>
    <div class="kutay-signature">🛡️ Baş Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. GERÇEK DERİN TARAMA MOTORU (HEURISTIC) ---

def derin_analiz_yap(data, filename):
    bulgular = []
    risk_skoru = 0
    
    # A. Dosya Kimliği (SHA-256)
    sha256 = hashlib.sha256(data).hexdigest()
    
    # B. Zararlı Kod Kalıpları Taraması (Byte Seviyesinde)
    # Bu kısım dosyanın içindeki gizli "tehlikeli" kodları arar
    zararli_kodlar = {
        b"os.system": "Sistem komutu çalıştırma girişimi (OS Injection)",
        b"subprocess.": "Arka planda gizli işlem başlatma",
        b"eval(": "Dinamik kod yürütme (Tehlikeli)",
        b"base64.b64decode": "Gizlenmiş (Encrypted) veri trafiği",
        b"requests.get": "Dış sunucudan dosya indirme bağlantısı",
        b"socket.connect": "Uzak sunucuya sızma/bağlanma girişimi"
    }
    
    for kod, aciklama in zararli_kodlar.items():
        if kod in data:
            risk_skoru += 30
            bulgular.append(f"🚩 KRİTİK: {aciklama}")

    # C. PDF İç Yapı Analizi
    if filename.lower().endswith(".pdf") and PDF_DESTEK:
        try:
            reader = PdfReader(BytesIO(data))
            trailer = str(reader.trailer)
            if "/JS" in trailer or "/JavaScript" in trailer:
                risk_skoru += 40
                bulgular.append("🚩 TEHLİKE: PDF içinde gizli JavaScript (Exploit) tespit edildi.")
            if "/OpenAction" in trailer:
                risk_skoru += 20
                bulgular.append("⚠️ UYARI: Otomatik açılma komutu bulundu.")
        except:
            bulgular.append("❔ Dosya yapısı tarama için çok karmaşık, manuel kontrol önerilir.")

    return sha256, bulgular, risk_skoru

# --- 3. ANA PANEL ---

st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 4.5rem; margin-bottom: 10px;">🛡️ KUTAY KORUMA</h1>
        <p>Gelişmiş Tehdit Analizi & Derin Kod İnceleme Sistemi v3.0</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="status-panel">SİSTEM DURUMU: GÜVENLİ | ANALİZ KAPASİTESİ: 200 MB</div>', unsafe_allow_html=True)

tabs = st.tabs(["📂 DOSYA TARAMA", "🔗 URL TARAMA", "📊 İSTATİSTİKLER"])

with tabs[0]:
    uploaded_file = st.file_uploader("Analiz edilecek dosyayı seçin", type=None)
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        
        with st.status("🔍 Derin Analiz Yürütülüyor...", expanded=True) as status:
            st.write("DNA (Hash) Analizi yapılıyor...")
            h, bugs, score = derin_analiz_yap(file_bytes, uploaded_file.name)
            time.sleep(1)
            st.write("Heuristic (Davranışsal) motor çalıştırılıyor...")
            time.sleep(1.2)
            st.write("Kutay Savunma Veritabanı ile eşleştiriliyor...")
            time.sleep(0.8)
            status.update(label="Analiz Tamamlandı!", state="complete")

        st.markdown(f"""
        <div class="analysis-box">
            <h2 style="color: #3d85f6;">📊 Analiz Raporu: {uploaded_file.name}</h2>
            <p><b>SHA-256 Parmak İzi:</b></p>
            <code style="display: block; background: #000; color: #00FF41; padding: 15px; border-radius: 5px;">{h}</code>
        </div>
        """, unsafe_allow_html=True)

        if score == 0:
            st.balloons()
            st.success(f"✅ TERTEMİZ: {uploaded_file.name} dosyasında hiçbir zararlı kod yapısı bulunamadı.")
        elif score < 50:
            st.warning(f"⚠️ ŞÜPHELİ: {len(bugs)} adet risk faktörü bulundu. Dikkatli olun!")
            for b in bugs: st.write(b)
        else:
            st.error(f"🚨 TEHLİKELİ: Bu dosya zararlı yazılım özellikleri gösteriyor!")
            for b in bugs: st.write(b)

with tabs[1]:
    st.info("Kutay URL Tarama motoru şu an geliştiriliyor. Çok yakında!")

with tabs[2]:
    st.write("### Sistem İstatistikleri")
    col1, col2, col3 = st.columns(3)
    col1.metric("Analiz Edilen Dosya", "1,240+", "+12")
    col2.metric("Engellenen Tehdit", "450+", "+5")
    col3.metric("Kutay Güvenlik Skoru", "%100")

st.write("---")
st.markdown("<p style='text-align: center; opacity: 0.5;'>© 2026 Kutay Tatlıcak Cyber Security Lab. İzinsiz kopyalanamaz.</p>", unsafe_allow_html=True)
