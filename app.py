import streamlit as st
import os
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AI Ultimate Prompt Generator", page_icon="⚡", layout="centered")

# 2. Get API Key
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🚨 GROQ_API_KEY not found. Please add it in Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Model Llama 4 Scout
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct" 

def get_llama_enhancement(base, outfit, background, mode):
    """
    Generates a structured Stable Diffusion prompt using Llama 4.
    """
    
    # System Instruction: Strictly English & Structured
    system_instruction = """
    You are an expert AI Prompt Engineer for Midjourney and Stable Diffusion.
    Your goal is to construct a HIGHLY DETAILED prompt based on user inputs.
    
    CRITICAL RULES:
    1. OUTPUT MUST BE IN ENGLISH ONLY.
    2. Structure the prompt in this order: [Subject Description], [Outfit Details], [Background/Environment], [Lighting/Camera/Style].
    3. Do NOT merge the outfit into the body description. Keep them distinct.
    4. Use high-quality keywords: "8k, masterpiece, highly detailed, photorealistic, trending on artstation".
    5. No conversational filler. Just the raw prompt.
    """

    user_content = f"""
    Create a {mode} prompt.
    
    1. SUBJECT (Fixed): {base}
    2. OUTFIT (Variable): {outfit}
    3. BACKGROUND (Variable): {background}
    
    Combine them into a single, fluid, professional visual description.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_content}
            ],
            temperature=0.6,
            max_tokens=400,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- WEBSITE UI (Full English) ---

st.title("⚡ Llama 4 Prompt Generator")
st.markdown(f"*Powered by latest Groq Model: `{MODEL_ID}`*")

# Mode Selection
mode = st.radio("Select Style Mode:", ["Consistent Avatar (Realism)", "Anime Style", "Product Photography", "3D Disney Pixar Style"])

st.divider()

# User Inputs
with st.form("prompt_form"):
    st.subheader("1. Character / Subject Base")
    st.caption("Describe the physical traits that MUST NOT change (Face, Hair, Body Type).")
    base_input = st.text_input("Example: A cyberpunk girl, platinum bob hair, blue eyes", placeholder="Describe the face & body...")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2. Outfit / Clothing")
        outfit_input = st.text_input("Example: Wearing a yellow raincoat", placeholder="What are they wearing?")
        
    with col2:
        st.subheader("3. Background / Location")
        bg_input = st.text_input("Example: Rainy neon Tokyo street", placeholder="Where are they?")

    submitted = st.form_submit_button("✨ Generate Magic Prompt")

# Output Section
if submitted:
    if not base_input:
        st.warning("⚠️ Please describe the Character/Subject first.")
    else:
        with st.spinner("AI is crafting your masterpiece..."):
            result = get_llama_enhancement(base_input, outfit_input, bg_input, mode)
            
            st.success("✅ Prompt Generated Successfully!")
            st.text_area("Copy this prompt:", value=result, height=200)
            st.caption("Pro Tip: Paste this directly into Midjourney, Flux, or Stable Diffusion.")
