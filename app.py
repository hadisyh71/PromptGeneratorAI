import streamlit as st
from groq import Groq

# --- KONFIGURASI ---
st.set_page_config(page_title="AI Super Prompt", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stButton>button { background-color: #FF4B4B; color: white; width: 100%; }
    .stTextArea textarea { font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# --- INISIALISASI GROQ ---
# Mengambil API Key dari secrets.toml secara aman
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ API Key belum dipasang di .streamlit/secrets.toml")
    st.stop()

st.title("🚀 Smart Prompt Generator (Powered by Llama 3)")
st.markdown("Masukkan ide kasar (bahkan bahasa Indonesia), AI akan menyusunnya ke struktur **Valentina** atau **Poster**.")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    mode = st.radio("Mode", ["Avatar Konsisten (Valentina)", "Poster Iklan"])
    st.info("💡 Menggunakan model: Llama 3 (via Groq)")

# --- FUNGSI OTAK AI (LLM) ---
def get_llama_enhancement(user_input, prompt_type):
    """
    Fungsi ini menyuruh Llama menerjemahkan & mempercantik input user
    menjadi deskripsi visual bahasa Inggris yang padat.
    """
    if prompt_type == "avatar":
        system_msg = "You are an expert AI Art prompter. Convert user's simple description into a detailed visual description of an ACTION and OUTFIT for a photorealistic portrait. Keep it under 20 words. Direct visual keywords only. No filler."
    else:
        system_msg = "You are an expert AI Art prompter. Convert user's simple description into a detailed visual description of a BACKGROUND and MOOD for a fashion poster. Keep it under 20 words. Direct visual keywords only."

    completion = client.chat.completions.create(
        model="llama3-8b-8192", # Ganti ke llama3-70b-8192 kalau mau lebih pintar
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Description: {user_input}"}
        ],
        temperature=0.5,
        max_tokens=100
    )
    return completion.choices[0].message.content

# --- INTERFACE UTAMA ---

if mode == "Avatar Konsisten (Valentina)":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Input Ide")
        # User bisa input bahasa Indonesia ngasal
        raw_idea = st.text_area("Karakter lagi ngapain?", value="Lagi minum kopi di senopati, bajunya kemeja flanel kotak-kotak")
        region = st.selectbox("Base Model Face", ["Latina (Valentina)", "Asian (Yuki)", "European (Elena)"])
        
    if st.button("✨ Generate Magic Prompt"):
        with st.spinner("Llama sedang meracik prompt..."):
            # 1. Minta Llama menerjemahkan ide user jadi 'Prompt Ingredients'
            enhanced_desc = get_llama_enhancement(raw_idea, "avatar")
            
            # 2. Tentukan Base Character (Hardcoded Structure Anda)
            if "Latina" in region:
                base_char = "stunning 24-year-old Latina female named Valentina, radiant olive skin, large expressive dark brown eyes"
            elif "Asian" in region:
                base_char = "stunning 24-year-old Japanese female named Yuki, porcelain skin, almond-shaped eyes"
            else:
                base_char = "stunning 24-year-old Scandinavian female named Elena, pale skin, blue eyes"

            # 3. GABUNGKAN KE STRUKTUR RAHASIA ANDA
            final_prompt = f"""Portrait of a {base_char}. Shot on 85mm portrait lens. 
She is {enhanced_desc}. 
High-end fashion photography, 8k, extreme facial detail, golden hour lighting. 
(masterpiece, best quality:1.2)."""
            
            st.success("Selesai!")
            st.markdown("### Prompt Siap Copy:")
            st.code(final_prompt, language="text")
            
            with st.expander("Lihat apa yang dilakukan Llama"):
                st.write(f"Input Asli: {raw_idea}")
                st.write(f"Terjemahan Llama: {enhanced_desc}")

elif mode == "Poster Iklan":
    col1, col2 = st.columns(2)
    with col1:
        title_text = st.text_input("Judul Poster", "BIG SALE")
        poster_idea = st.text_area("Deskripsi Suasana Poster", "Suasana pantai pas sunset, model cewek lari kegirangan")
    
    if st.button("🎨 Generate Poster Prompt"):
        with st.spinner("Membuat konsep poster..."):
            # 1. Llama mempercantik deskripsi background
            enhanced_bg = get_llama_enhancement(poster_idea, "poster")
            
            # 2. Masukkan ke Struktur Poster Anda
            final_prompt = f"""Full frame cinematic fashion poster art. A Medium Full Shot. 
Scene details: {enhanced_bg}. 
Massive negative space at the top. Huge, elegant, wide-spaced serif typography reading "{title_text}" floating in the upper space. 
Cinematic lighting, high texture details, photorealistic 8k. NO magazine mockup."""
            
            st.success("Selesai!")
            st.code(final_prompt, language="text")
