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
# Header & Logo
# =====================
col1, col2 = st.columns([1, 5])
with col1:
    # الصورة الآن تأخذ 80% من العمود لتكون متجاوبة
    st.image("elo_logo.png", width=None, use_column_width=True)
with col2:
    st.markdown("""
    <h1 style='margin-bottom:0; font-size:calc(24px + 1vw);'> Math AI🧮</h1>
    <p style='font-size:calc(12px + 0.5vw);'>
    Official Training Platform for<br>
    <strong>English Language Olympiad (ELO)</strong>
    </p>
    """, unsafe_allow_html=True)

st.divider()

# =====================
# Symbols
# =====================
x = symbols("x")

# =====================
# Helper Function
# =====================
def convert_math(text):
    """
    Convert user input into a sympy-compatible expression.
    """
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
    with st.container():
        st.markdown("<h2 style='color:#1f77b4; font-size:calc(18px + 0.8vw);'>Basic Math Operations</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        a = st.number_input("First number", value=0.0)
        b = st.number_input("Second number", value=0.0)
        op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
        if st.button("Calculate", key="calc1"):
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
    with st.container():
        st.markdown("<h2 style='color:#ff7f0e; font-size:calc(18px + 0.8vw);'>Solve an Equation</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        eq = st.text_input("Enter equation (example: x^2 - 4x + 3 = 0)")
        if st.button("Solve Equation", key="solve_eq"):
            try:
                left, right = convert_math(eq).split("=")
                expr = expand(sympify(left) - sympify(right))
                st.latex(f"{latex(expr)} = 0")
                for s in solve(expr, x):
                    st.latex(f"x = {latex(s)}")
            except:
                st.error("Invalid equation format")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    with st.container():
        st.markdown("<h2 style='color:#2ca02c; font-size:calc(18px + 0.8vw);'>Plot a Function</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        func = st.text_input("Enter function (example: x^2 - 4x + 3)")
        if st.button("Plot Function", key="plot_func"):
            try:
                f = sympify(convert_math(func))
                xs = np.linspace(-10, 10, 400)
                ys = [f.subs(x, i) for i in xs]

                # figsize متغير لتناسب الأجهزة الصغيرة
                fig, ax = plt.subplots(figsize=(max(6, st.get_option('browser.gap', 6)), 5))
                ax.plot(xs, ys, label=str(f), color="#1f77b4")
                ax.axhline(0, color='black')
                ax.axvline(0, color='black')
                ax.grid(True)
                ax.legend(fontsize=8)
                st.pyplot(fig)
            except:
                st.error("Invalid function")

# =====================
# Footer
# =====================
st.divider()
st.caption("© 2026 | English Language Olympiad")
