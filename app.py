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
    st.image("elo_logo.png", width=300)  # أكبر حجم صورة الشعار
with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'> Math AI🧮</h1>
    <p style='font-size:12px;'>
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
    """Convert user input into a sympy-compatible expression."""
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
    st.subheader("Solve an Equation")

    # Session state for input
    if "eq_input" not in st.session_state:
        st.session_state.eq_input = ""

    # Input field
    st.session_state.eq_input = st.text_input(
        "Enter your quadratic equation:", st.session_state.eq_input
    )

    # Quick examples as buttons
    st.write("### Quick Examples:")
    col1, col2, col3 = st.columns(3)
    examples = ["x^2 - 4x + 3 = 0", "x^2 + 5x + 6 = 0", "2x^2 - 3x - 2 = 0"]
    for i, col in enumerate([col1, col2, col3]):
        if col.button(examples[i]):
            st.session_state.eq_input = examples[i]

    # Solution buttons
    st.write("### Solve Using:")
    col_dir, col_quad, col_step = st.columns(3)

    # Direct Solve
    with col_dir:
        if st.button("📝 Direct Solve"):
            try:
                left, right = convert_math(st.session_state.eq_input).split("=")
                expr = expand(sympify(left) - sympify(right))
                st.latex(f"{latex(expr)} = 0")
                sols = solve(expr, x)
                st.write("Roots:")
                for s in sols:
                    st.latex(f"x = {latex(s)}")
            except:
                st.error("Invalid equation format")

    # Quadratic Formula
    with col_quad:
        if st.button("📏 Quadratic Formula"):
            try:
                left, right = convert_math(st.session_state.eq_input).split("=")
                expr = expand(sympify(left) - sympify(right))
                coeffs = expr.as_coefficients_dict()
                a = coeffs.get(x**2, 0)
                b = coeffs.get(x, 0)
                c = coeffs.get(1, 0)
                st.latex(f"x = (-b ± √(b² - 4ac)) / 2a")
                st.latex(f"a={a}, b={b}, c={c}")
                discriminant = b**2 - 4*a*c
                root1 = (-b + discriminant**0.5) / (2*a)
                root2 = (-b - discriminant**0.5) / (2*a)
                st.write("Roots:")
                st.latex(f"x₁ = {root1}")
                st.latex(f"x₂ = {root2}")
            except:
                st.error("Invalid quadratic equation")

    # Step by Step
    with col_step:
        if st.button("➡️ Step by Step"):
            try:
                left, right = convert_math(st.session_state.eq_input).split("=")
                expr = expand(sympify(left) - sympify(right))
                st.write("Step 1: Standard form:")
                st.latex(f"{latex(expr)} = 0")
                coeffs = expr.as_coefficients_dict()
                a = coeffs.get(x**2, 0)
                b = coeffs.get(x, 0)
                c = coeffs.get(1, 0)
                st.write("Step 2: Identify coefficients:")
                st.latex(f"a={a}, b={b}, c={c}")
                st.write("Step 3: Compute discriminant Δ = b² - 4ac")
                discriminant = b**2 - 4*a*c
                st.latex(f"Δ = {discriminant}")
                st.write("Step 4: Apply quadratic formula:")
                st.latex(f"x = (-b ± √Δ) / (2a)")
                root1 = (-b + discriminant**0.5) / (2*a)
                root2 = (-b - discriminant**0.5) / (2*a)
                st.write("Step 5: Roots:")
                st.latex(f"x₁ = {root1}")
                st.latex(f"x₂ = {root2}")
            except:
                st.error("Invalid quadratic equation")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")
    func = st.text_input("Enter function (example: x^2 - 4x + 3)", key="func_input")
    if st.button("Plot Function"):
        try:
            f = sympify(convert_math(func))
            xs = np.linspace(-10, 10, 400)
            ys = [f.subs(x, i) for i in xs]

            fig, ax = plt.subplots()
            ax.plot(xs, ys, label=str(f))
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        except:
            st.error("Invalid function")

# =====================
# Footer
# =====================
st.divider()
st.caption("© 2026 | English Language Olympiad")
