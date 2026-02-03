import streamlit as st
from sympy import symbols, solve, sympify, latex, expand
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# Page Configuration
# =====================
st.set_page_config(
    page_title="Math AI | ELO",
    layout="wide"
)

# =====================
# Header with Logo
# =====================
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo_elo.png", width=150)  # شعارك هنا

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'> Math AI 🧮 </h1>
    <p style='font-size:12px;'>
    Official Training Platform for<br>
    <strong>English Language Olympiad (ELO)</strong>
    </p>
    """, unsafe_allow_html=True)

st.divider()
