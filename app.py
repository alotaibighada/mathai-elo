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
col1, col2, col3 = st.columns([1.2, 4, 1.2])

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
    st.image("logo_elo.png", width=110)

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
    a = st.number_input("First number", value=0.0, format="%f")
    b = st.number_input("Second number", value=0.0, format="%f")
    op = st.radio("Operation", ["Add", "Subtract", "Multiply", "Divide"], horizontal=True)

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
    st.subheader("Solve a Quadratic Equation")

    if "eq_input" not in st.session_state:
        st.session_state.eq_input = ""

    st.session_state.eq_input = st.text_input(
        "Enter your equation (example: x^2 - 4x + 3 = 0)",
        st.session_state.eq_input
    )

    st.write("### Quick Examples")
    colA, colB, colC = st.columns(3)
    examples = ["x^2 - 4x + 3 = 0", "x^2 + 5x + 6 = 0", "2x^2 - 3x - 2 = 0"]
    for col, ex in zip([colA, colB, colC], examples):
        if col.button(ex):
            st.session_state.eq_input = ex

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Direct Solve"):
            try:
                left, right = convert_math(st.session_state.eq_input).split("=")
                expr = expand(sympify(left) - sympify(right))
                st.latex(f"{latex(expr)} = 0")
                sols = solve(expr, x)
                for s in sols:
                    st.latex(f"x = {latex(s)}")
            except:
                st.error("Invalid equation format")

    with col2:
        if st.button("📏 Quadratic Formula"):
            try:
                left, right = convert_math(st.session_state.eq_input).split("=")
                expr = expand(sympify(left) - sympify(right))
                coeffs = expr.as_coefficients_dict()
                a = coeffs.get(x**2, 0)
                b = coeffs.get(x, 0)
                c = coeffs.get(1, 0)

                st.latex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}")
                disc = b**2 - 4*a*c
                r1 = (-b + disc**0.5) / (2*a)
                r2 = (-b - disc**0.5) / (2*a)

                st.latex(f"x_1 = {r1}")
                st.latex(f"x_2 = {r2}")
            except:
                st.error("Invalid quadratic equation")

    with col3:
        if st.button("➡️ Step by Step"):
            try:
                left, right = convert_math(st.session_state.eq_input).split("=")
                expr = expand(sympify(left) - sympify(right))
                coeffs = expr.as_coefficients_dict()
                a = coeffs.get(x**2, 0)
                b = coeffs.get(x, 0)
                c = coeffs.get(1, 0)

                st.write("Standard form:")
                st.latex(f"{latex(expr)} = 0")

                st.write("Coefficients:")
                st.latex(f"a={a}, b={b}, c={c}")

                disc = b**2 - 4*a*c
                st.latex(f"\\Delta = {disc}")

                r1 = (-b + disc**0.5) / (2*a)
                r2 = (-b - disc**0.5) / (2*a)

                st.latex(f"x_1 = {r1}")
                st.latex(f"x_2 = {r2}")
            except:
                st.error("Invalid equation")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")
    func = st.text_input("Enter function (example: x^2 - 4x + 3)")

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
