import streamlit as st

st.title("Test 1: Streamlit works")

try:
    import google.generativeai as genai
    st.success("✅ google.generativeai imported successfully!")
except Exception as e:
    st.error(f"❌ Error importing genai: {e}")

try:
    from dotenv import load_dotenv
    st.success("✅ dotenv imported successfully!")
except Exception as e:
    st.error(f"❌ Error importing dotenv: {e}")

try:
    import os
    st.success("✅ os imported successfully!")
except Exception as e:
    st.error(f"❌ Error importing os: {e}")

st.write("All imports tested!")