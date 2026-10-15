
import streamlit as st
from main import app

# Create the Streamlit frontend
streamlit_app = st.App("frontend.py")

# Mount Streamlit on the FastAPI application
app.mount("/", streamlit_app)
