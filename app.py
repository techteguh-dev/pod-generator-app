import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="POD Generator", layout="centered")
st.title(" POD Generator App")
st.caption("Generate desain produk Print-on-Demand dengan AI")

try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except KeyError:
    st.error("❌ Error: HF_TOKEN belum disetting di Streamlit Secrets!")
    st.stop()

def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    
    with st.spinner("Sedang menggambar... ⏳"):
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        st.error(f"Error API: {response.text}")
        return None

prompt = st.text_input("Deskripsi Gambar:", placeholder="Contoh: Cute cat wearing sunglasses, vector art style")

if st.button("🚀 Generate Gambar", type="primary"):
    if prompt:
        img = generate_image(prompt)
        if img:
            st.image(img, caption="Hasil Desain POD", use_column_width=True)
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Download Gambar",
                data=buf.getvalue(),
                file_name="pod-design.png",
                mime="image/png"
            )
    else:
        st.warning("Mohon isi deskripsi gambar terlebih dahulu!")
