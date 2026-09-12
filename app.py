import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="POD Generator", layout="centered")
st.title("🎨 POD Generator App")
st.caption("Generate desain produk Print-on-Demand dengan AI")

# Ambil token dari secrets
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except KeyError:
    st.error("❌ Error: HF_TOKEN belum disetting di Streamlit Secrets!")
    st.stop()

def generate_image(prompt):
    # GANTI KE MODEL YANG LEBIH RINGAN & STABIL
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}  # Paksa tunggu sampai model siap
    }
    
    with st.spinner("Sedang menggambar... ⏳ (Bisa butuh 30-60 detik)"):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
            elif response.status_code == 503:
                st.warning("⚠️ Model sedang loading. Coba lagi dalam 1 menit.")
                return None
            else:
                st.error(f"❌ Error API: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏰ Timeout: Server Hugging Face terlalu sibuk. Coba lagi nanti.")
            return None
        except Exception as e:
            st.error(f"❌ Koneksi gagal: {str(e)}")
            return None

# Input prompt
prompt = st.text_input(
    "Deskripsi Gambar (Bahasa Indonesia/Inggris):", 
    placeholder="Contoh: Kucing lucu pakai kacamata hitam gaya vektor, background putih"
)

if st.button("🚀 Generate Gambar", type="primary"):
    if prompt.strip():
        img = generate_image(prompt)
        if img:
            st.image(img, caption="✨ Hasil Desain POD", use_column_width=True)
            
            # Tombol download
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Download Gambar PNG",
                data=buf.getvalue(),
                file_name="pod-design.png",
                mime="image/png"
            )
    else:
        st.warning("⚠️ Mohon isi deskripsi gambar terlebih dahulu!")
