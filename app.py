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
    page_icon="logo_math_ai.png",
    layout="wide"
)

# =====================
# Header & Logos
# =====================
col1, col2, col3 = st.columns([1.3, 4, 1.3])

with col1:
    st.image("logo_math_ai.png", width=120)

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
    st.image("elo_logo.png", width=110)

st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)

# =====================
# Symbol
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
    op = st.radio(
        "Operation",
        ["Add", "Subtract", "Multiply", "Divide"],
        horizontal=True
    )

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

    eq = st.text_input(
        "Enter equation (example: x^2 - 4x + 3 = 0)"
    )

    st.write("### Quick Examples")
    colA, colB, colC = st.columns(3)
    examples = [
        "x^2 - 4x + 3 = 0",
        "x^2 + 5x + 6 = 0",
        "2x^2 - 3x - 2 = 0"
    ]

    for col, ex in zip([colA, colB, colC], examples):
        if col.button(ex):
            eq = ex

    if st.button("Solve Equation"):
        try:
            left, right = convert_math(eq).split("=")
            expr = expand(sympify(left) - sympify(right))
            st.latex(f"{latex(expr)} = 0")
            solutions = solve(expr, x)
            st.write("Solutions:")
            for s in solutions:
                st.latex(f"x = {latex(s)}")
        except:
            st.error("Invalid equation format")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")
    func = st.text_input(
        "Enter function (example: x^2 - 4x + 3)"
    )

    if st.button("Plot Function"):
        try:
            f = sympify(convert_math(func))
            xs = np.linspace(-10, 10, 400)
            ys = [f.subs(x, i) for i in xs]

            fig, ax = plt.subplots()
            ax.plot(xs, ys, label=str(f))
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        except:
            st.error("Invalid function")

# =====================
# Footer
# =====================
st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)
st.caption("© 2026 | English Language Olympiad (ELO)")
