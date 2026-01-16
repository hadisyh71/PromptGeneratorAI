import streamlit as st
import os
from groq import Groq

# 1. Konfigurasi Halaman (Page Config)
st.set_page_config(page_title="AI Super Prompt Generator", page_icon="⚡")

# 2. Ambil API Key dari Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("🚨 GROQ_API_KEY not found in Secrets. Please add it in 'Manage app' > 'Secrets'.")
    st.stop()

# 3. Inisialisasi Client Groq
client = Groq(api_key=api_key)

# --- MODEL BARU SESUAI DASHBOARD GROQ ANDA ---
# Sesuai screenshot: meta-llama/llama-4-scout-17b-16e-instruct
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct" 

def get_llama_enhancement(user_idea, style):
    """
    Function to generate prompts using Llama 4 Scout.
    Forces output in English.
    """
    
    # System Prompt khusus bahasa Inggris
    system_instruction = """
    You are an expert AI Prompt Engineer.
    Your task is to convert simple ideas into highly detailed, professional image generation prompts.
    
    RULES:
    1. OUTPUT MUST BE IN ENGLISH ONLY.
    2. Do not include introductory text like "Here is the prompt". Just the prompt.
    3. Include details about lighting, camera angle, texture, and 8k resolution.
    4. For 'Avatar' style: Focus on consistency, facial features, and character design.
    5. For 'Product' style: Focus on studio lighting, flatlay composition, and luxury look.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Create a {style} prompt for this concept: {user_idea}"}
            ],
            temperature=0.7,
            max_tokens=300,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- TAMPILAN WEBSITE (UI) ---

st.title("⚡ Llama 4 Scout Prompt Generator")
st.caption(f"Powered by Groq Model: {MODEL_ID}")

# Pilihan Mode
mode = st.radio("Select Mode:", ["Consistent Avatar", "Product Photography (Flatlay)"])

# Input User
with st.form("prompt_form"):
    if mode == "Consistent Avatar":
        user_input = st.text_input("Describe your character:", placeholder="e.g., A cute cyber-punk girl with pink hair...")
        style_type = "consistent character avatar"
    else:
        user_input = st.text_input("Describe your product:", placeholder="e.g., A white t-shirt on a marble table...")
        style_type = "professional product photography flatlay"

    submitted = st.form_submit_button("✨ Generate Magic Prompt")

# Hasil Output
if submitted and user_input:
    with st.spinner("Llama 4 Scout is thinking..."):
        result = get_llama_enhancement(user_input, style_type)
        
        st.success("Prompt Generated!")
        st.code(result, language="text") # Tombol copy otomatis ada di sini
        st.caption("Copy the prompt above and paste it into Midjourney/Flux/Leonardo AI.")
