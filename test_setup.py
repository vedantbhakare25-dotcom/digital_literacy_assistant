import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("🧪 Setup Test")
st.write("Testing if everything works...")

# Test Gemini API
if st.button("Test Gemini API"):
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        st.write(f"✅ API Key found: {api_key[:15]}...")
        
        genai.configure(api_key=api_key)
        st.write("✅ genai configured")
        
        # Use gemini-2.5-flash (newest, fastest)
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.write("✅ model created")
        
        st.write("⏳ Generating response...")
        response = model.generate_content("Say hello in one sentence!")
        
        st.success("✅ Gemini API is working!")
        st.write(f"**Response:** {response.text}")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

st.write("If you see this, Streamlit is working! ✨")