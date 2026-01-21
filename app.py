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
    st.image("elo_logo.png", width=250, use_column_width=True)
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
        method = st.radio(
            "Choose solution method:",
            ["Direct Solve", "Quadratic Formula", "Step by Step"]
        )

        if st.button("Solve Equation", key="solve_eq"):
            try:
                left, right = convert_math(eq).split("=")
                expr = expand(sympify(left) - sympify(right))
                st.latex(f"{latex(expr)} = 0")

                # ===== Direct Solve =====
                if method == "Direct Solve":
                    sols = solve(expr, x)
                    for s in sols:
                        st.latex(f"x = {latex(s)}")

                # ===== Quadratic Formula =====
                elif method == "Quadratic Formula":
                    degree = expr.as_poly(x).degree()
                    coeffs = expr.as_poly(x).all_coeffs()
                    if degree == 2:  # فقط للمعادلة التربيعية
                        a, b, c = coeffs
                        st.markdown("**Quadratic Formula:**")
                        st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                        st.markdown(f"Here, a = {a}, b = {b}, c = {c}")
                        
                        delta = b**2 - 4*a*c
                        x1 = (-b + delta**0.5) / (2*a)
                        x2 = (-b - delta**0.5) / (2*a)
                        st.markdown("**Solution:**")
                        st.latex(f"x_1 = {latex(x1)} , \\quad x_2 = {latex(x2)}")
                    else:
                        st.warning(f"Quadratic formula only works for degree 2 equations. Your equation is degree {degree}. Using Direct Solve instead.")
                        sols = solve(expr, x)
                        for s in sols:
                            st.latex(f"x = {latex(s)}")

                # ===== Step by Step =====
                elif method == "Step by Step":
                    st.markdown("**Step 1: Expand the equation**")
                    st.latex(f"{latex(expr)} = 0")
                    factored = expr.factor()
                    if factored != expr:
                        st.markdown("**Step 2: Factor the equation**")
                        st.latex(f"{latex(factored)} = 0")
                        st.markdown("**Step 3: Solve each factor**")
                        sols = solve(expr, x)
                        for s in sols:
                            st.latex(f"x = {latex(s)}")
                    else:
                        st.markdown("Cannot factor further, solving directly:")
                        sols = solve(expr, x)
                        for s in sols:
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

                fig, ax = plt.subplots(figsize=(8,5))
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
