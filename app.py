import streamlit as st
from sympy import symbols, solve, sympify, latex, expand
import numpy as np
import matplotlib.pyplot as plt
import re
import os

# =====================
# Page Configuration
# =====================
st.set_page_config(
    page_title="Math AI | ELO",
    page_icon="logo_math_ai.png",
    layout="wide"
)

# =====================
# Header & Logos (SAFE LOAD)
# =====================
col1, col2, col3 = st.columns([1.2, 4, 1.2])

with col1:
    if os.path.exists("logo_math_ai.png"):
        st.image("logo_math_ai.png", width=120)
    else:
        st.warning("⚠️ logo_math_ai.png غير موجود")

with col2:
    st.markdown("""
    <div style="text-align:center;">
        <h1 style="margin-bottom:0;">Math AI</h1>
        <p style="font-size:14px; color:gray; margin-top:4px;">
        Official Training Platform for<br>
        <strong>English Language Olympiad (ELO)</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if os.path.exists("logo_elo.png"):
        st.image("logo_elo.png", width=110)
    else:
        st.warning("⚠️ logo_elo.png غير موجود")

st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)

# =====================
# Symbols
# =====================
x = symbols("x")

# =====================
# Helper Function
# =====================
def convert_math(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    return text

# =====================
# Tabs
# =====================
tab1, tab2, tab3 = st.tabs([
    "🔢 Math Operations",
    "📐 Equation Solver",
    "📊 Function Plot",
])

# ---------------------
# Tab 1: Math Operations
# ---------------------
with tab1:
    st.subheader("Basic Math Operations")
    a = st.number_input("First number", value=0.0)
    b = st.number_input("Second number", value=0.0)
    op = st.radio("Operation", ["Add", "Subtract", "Multiply", "Divide"], horizontal=True)

    if st.button("Calculate"):
        if op == "Divide" and b == 0:
            st.error("Cannot divide by zero")
        else:
            result = {
                "Add": a + b,
                "Subtract": a - b,
                "Multiply": a * b,
                "Divide": a / b
            }[op]
            st.success(f"Result = {result}")

# ---------------------
# Tab 2: Equation Solver
# ---------------------
with tab2:
    st.subheader("Solve a Quadratic Equation")

    eq = st.text_input("Enter equation (example: x^2 - 4x + 3 = 0)")

    colA, colB, colC = st.columns(3)
    examples = ["x^2 - 4x + 3 = 0", "x^2 + 5x + 6 = 0", "2x^2 - 3x - 2 = 0"]
    for col, ex in zip([colA, colB, colC], examples):
        if col.button(ex):
            eq = ex

    if st.button("Solve"):
        try:
            left, right = convert_math(eq).split("=")
            expr = expand(sympify(left) - sympify(right))
            st.latex(f"{latex(expr)} = 0")
            sols = solve(expr, x)
            for s in sols:
                st.latex(f"x = {latex(s)}")
        except:
            st.error("Invalid equation format")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")
    func = st.text_input("Enter function (example: x^2 - 4x + 3)")

    if st.button("Plot"):
        try:
            f = sympify(convert_math(func))
            xs = np.linspace(-10, 10, 400)
            ys = [f.subs(x, i) for i in xs]

            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)
            st.pyplot(fig)
        except:
            st.error("Invalid function")

# =====================
# Footer
# =====================
st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)
st.caption("© 2026 | English Language Olympiad (ELO)")
