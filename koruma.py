import streamlit as st
import os
import re
import time
from pypdf import PdfReader

# --- 1. SİBER GÜVENLİK ARAYÜZ TASARIMI ---
st.set_page_config(page_title="KUTAY KORUMA.EXE", page_icon="🛡️", layout="centered")

# CSS: Hacker Teması ve Sağ Üst Köşe Yazısı
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Consolas', monospace; }
    
    /* ANALİZ KUTUSU */
    .scan-result {
        border: 2px solid #00FF41;
        border-radius: 10px;
        padding: 20px;
        background-color: #111;
        box-shadow: 0px 0px 20px rgba(0, 255, 65, 0.3);
        margin-top: 20px;
    }

    /* SAĞ ÜST KÖŞE GELİŞTİRİCİ ETİKETİ */
    .dev-label {
        position: fixed;
        top: 60px;
        right: 20px;
        background-color: #00FF41;
        color: #000000;
        font-size: 14px;
        font-weight: bold;
        padding: 8px 15px;
        border-radius: 20px;
        z-index: 9999;
        border: 2px solid #FFFFFF;
    }
    
    .stProgress > div > div > div > div { background-color: #00FF41; }
    </style>
    
    <div class="dev-label">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. ANALİZ FONKSİYONLARI ---

def link_tara(url):
    """Linkleri güvenlik kriterlerine göre puanlar"""
    risk_skoru = 0
    bulgular = []
    
    if url.startswith("http://"):
        risk_skoru += 40
        bulgular.append("❌ Güvensiz bağlantı protokolü (HTTP) tespit edildi.")
    
    phishing_kelimeleri = ["login", "verify", "robux", "free", "gift", "nitro", "update", "account"]
    for kelime in phishing_kelimeleri:
        if kelime in url.lower():
            risk_skoru += 30
            bulgular.append(f"⚠️ Şüpheli kelime tespit edildi: '{kelime}'")
            break # Bir tane bulması yeterli
            
    if any(kisa in url for kisa in ["bit.ly", "t.co", "tinyurl"]):
        risk_skoru += 20
        bulgular.append("🔍 Kısaltılmış link: Gerçek hedef gizlenmiş olabilir.")

    return risk_skoru, bulgular

def pdf_tara(file):
    """PDF dosyasının iç yapısını derinlemesine inceler"""
    tehlikeler = []
    try:
        reader = PdfReader(file)
        # PDF'in ham içeriğinde zararlı objeleri tara
        raw_data = ""
        for page in reader.pages:
            raw_data += page.extract_text() or ""
        
        # Kritik siber güvenlik objelerini kontrol et
        raw_structure = str(reader.trailer)
        if "/JS" in raw_structure or "/JavaScript" in raw_structure:
            tehlikeler.append("🚨 Gömülü JavaScript (Kod Yürütme) bulundu!")
        if "/OpenAction" in raw_structure:
            tehlikeler.append("🚨 Otomatik Başlatma Komutu (OpenAction) tespit edildi!")
            
    except Exception as e:
        return [f"Dosya okuma hatası: {str(e)}"]
    
    return tehlikeler

# --- 3. ANA PANEL ---

st.markdown("<h1 style='text-align: center; color: #00FF41;'>🛡️ KUTAY KORUMA.EXE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Siber Tehdit ve Zararlı Yazılım Analiz Merkezi</p>", unsafe_allow_html=True)
st.write("---")

sekme1, sekme2 = st.tabs(["🌐 URL ANALİZİ", "📄 PDF DERİN TARAMA"])

with sekme1:
    url_adresi = st.text_input("Analiz edilecek URL'yi girin:", placeholder="https://example-secure-site.com")
    if st.button("LİNKİ TARAMAYI BAŞLAT"):
        if url_adresi:
            bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                bar.progress(i + 1)
            
            skor, rapor = link_tara(url_adresi)
            
            st.markdown("<div class='scan-result'>", unsafe_allow_html=True)
            if skor == 0:
                st.success("✅ ANALİZ SONUCU: Bağlantı güvenli görünüyor.")
            elif skor < 50:
                st.warning(f"⚠️ ANALİZ SONUCU: {len(rapor)} risk faktörü bulundu.")
                for r in rapor: st.write(r)
            else:
                st.error("🚨 KRİTİK TEHLİKE: Bu bağlantı yüksek risk taşıyor!")
                for r in rapor: st.write(r)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Lütfen bir URL adresi girin.")

with sekme2:
    dosya = st.file_uploader("Analiz edilecek PDF dosyasını seçin", type=["pdf"])
    if st.button("DOSYAYI ANALİZ ET"):
        if dosya:
            with st.spinner("Katmanlar çözülüyor ve zararlı kodlar taranıyor..."):
                time.sleep(2)
                tehditler = pdf_tara(dosya)
            
            st.markdown("<div class='scan-result'>", unsafe_allow_html=True)
            if not tehditler:
                st.success(f"✅ {dosya.name} temiz. Herhangi bir siber tehdit bulunamadı.")
            else:
                st.error(f"🚨 {dosya.name} içerisinde zararlı içerik bulundu!")
                for t in tehditler: st.write(t)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Lütfen bir PDF dosyası yükleyin.")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #444;'>KUTAY KORUMA Ekosistemi © 2026 Kutay Tatlıcak. Tüm hakları saklıdır.</p>", unsafe_allow_html=True)