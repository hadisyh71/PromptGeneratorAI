import streamlit as st
import os
from groq import Groq

# 1. Konfigurasi Halaman
st.set_page_config(page_title="AI Super Prompt Generator", page_icon="⚡", layout="centered")

# 2. Ambil API Key
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🚨 GROQ_API_KEY not found. Please add it in Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Model Llama 4 Scout (Sesuai Dashboard Groq Anda)
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct" 

def get_llama_enhancement(base, outfit, background, mode):
    """
    Menggabungkan 3 elemen (Base, Outfit, Background) menjadi satu prompt stabil.
    """
    
    # Instruksi System agar output stabil & Bahasa Inggris
    system_instruction = """
    You are an expert Stable Diffusion Prompt Engineer.
    Your goal is to construct a HIGHLY DETAILED prompt based on user inputs.
    
    CRITICAL RULES FOR STABILITY:
    1. OUTPUT MUST BE IN ENGLISH ONLY.
    2. Structure the prompt in this order: [Subject Description], [Outfit Details], [Background/Environment], [Lighting/Camera/Style].
    3. Do NOT merge the outfit into the body description. Keep them distinct to ensure the face remains consistent.
    4. Use keywords like "8k, masterpiece, highly detailed, photorealistic".
    5. No conversational filler. Just the raw prompt.
    """

    # User Message yang terstruktur
    user_content = f"""
    Create a {mode} prompt.
    
    1. SUBJECT (Keep this exact): {base}
    2. OUTFIT (Change this): {outfit}
    3. BACKGROUND (Change this): {background}
    
    Combine them into a fluid visual description.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_content}
            ],
            temperature=0.6, # Agak rendah biar lebih stabil (nurut)
            max_tokens=400,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- TAMPILAN WEBSITE (UI) ---

st.title("⚡ Llama 4 Scout Prompt Generator")
st.markdown(f"*Powered by Groq Model: `{MODEL_ID}`*")

# Pilihan Mode
mode = st.radio("Select Style Mode:", ["Consistent Avatar (Realism)", "Anime Style", "Product Photography"])

st.divider()

# Input User dengan Kolom Terpisah (Biar Rapi)
with st.form("prompt_form"):
    st.subheader("1. Character / Subject Base")
    st.caption("Deskripsikan fisik karakter yang TIDAK BOLEH berubah (Wajah, Rambut, Ras).")
    base_input = st.text_input("Example: A cute cyberpunk girl, pink bob hair, blue eyes", placeholder="Describe the face & body...")

    # Membagi 2 kolom untuk Outfit & Background
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2. Outfit / Clothing")
        outfit_input = st.text_input("Example: Wearing a yellow raincoat", placeholder="What are they wearing?")
        
    with col2:
        st.subheader("3. Background / Location")
        bg_input = st.text_input("Example: Rainy neon tokyo street", placeholder="Where are they?")

    submitted = st.form_submit_button("✨ Generate Stable Prompt")

# Hasil Output
if submitted:
    if not base_input:
        st.warning("Please describe the Character first.")
    else:
        with st.spinner("Llama 4 Scout is crafting your prompt..."):
            # Panggil fungsi AI
            result = get_llama_enhancement(base_input, outfit_input, bg_input, mode)
            
            st.success("✅ Prompt Generated Successfully!")
            st.text_area("Copy this prompt:", value=result, height=200)
            st.caption("Tip: Paste this into Midjourney, Flux, or Stable Diffusion.")
