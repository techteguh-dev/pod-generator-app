def generate_image(prompt):
    # GANTI KE MODEL V1.5 YANG LEBIH STABIL UNTUK AKUN GRATIS
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    
    with st.spinner("Sedang menggambar... ⏳ (Bisa butuh 30-90 detik)"):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
            elif response.status_code == 503:
                st.warning("️ Model sedang loading. Coba lagi dalam 1-2 menit.")
                return None
            elif response.status_code == 401:
                st.error("❌ Token tidak valid atau belum di-approve. Cek Hugging Face Settings.")
                return None
            else:
                st.error(f"❌ Error API: {response.status_code}")
                st.code(response.text)  # Tampilkan detail error
                return None
                
        except requests.exceptions.ConnectionError as e:
            st.error(" Koneksi ke Hugging Face gagal. Server mungkin sedang down atau memblokir akses.")
            st.info("💡 Solusi: Tunggu 10 menit, lalu coba lagi. Atau gunakan VPN jika memungkinkan.")
            return None
        except Exception as e:
            st.error(f"❌ Error tak terduga: {str(e)}")
            return None
