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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================
# Header & Logo
# =====================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("elo_logo.png", width=260)
with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'>🧮 Math AI</h1>
    <p style='font-size:14px;'>
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
    "📊 Function Plot"
])

# ======================================================
# TAB 1 – Math Operations
# ======================================================
with tab1:
    st.subheader("Basic Math Operations")

    c1, c2 = st.columns(2)
    with c1:
        a = st.number_input("First number", value=0.0)
    with c2:
        b = st.number_input("Second number", value=0.0)

    op = st.radio(
        "Choose operation:",
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

# ======================================================
# TAB 2 – Equation Solver
# ======================================================
with tab2:
    st.subheader("Quadratic Equation Solver")
    st.caption("Standard form: ax² + bx + c = 0")

    # ---------- Suggested equations ----------
    st.markdown("### Suggested equations:")

    examples = {
        "x² - 4x + 3 = 0": "x^2 - 4x + 3 = 0",
        "x² + 5x + 6 = 0": "x^2 + 5x + 6 = 0",
        "2x² - 3x - 2 = 0": "2x^2 - 3x - 2 = 0"
    }

    if "eq_value" not in st.session_state:
        st.session_state.eq_value = ""

    cols = st.columns(len(examples))
    for col, (label, value) in zip(cols, examples.items()):
        with col:
            if st.button(label):
                st.session_state.eq_value = value

    eq = st.text_input(
        "Enter equation",
        value=st.session_state.eq_value,
        placeholder="Example: x^2 - 4x + 3 = 0"
    )

    colA, colB, colC = st.columns(3)

    # ---------- Direct Solution ----------
    with colA:
        if st.button("🔹 Direct Solution"):
            try:
                left, right = convert_math(eq).split("=")
                expr = expand(sympify(left) - sympify(right))
                solutions = solve(expr, x)

                st.latex(f"{latex(expr)} = 0")
                for s in solutions:
                    st.latex(f"x = {latex(s)}")
            except:
                st.error("Invalid equation")

    # ---------- Quadratic Formula ----------
    with colB:
        if st.button("🔹 Quadratic Formula"):
            try:
                left, right = convert_math(eq).split("=")
                expr = expand(sympify(left) - sympify(right))

                a = expr.coeff(x, 2)
                b = expr.coeff(x, 1)
                c = expr.coeff(x, 0)

                if a == 0:
                    st.error("This is not a quadratic equation")
                else:
                    st.markdown("### Quadratic Formula")
                    st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")

                    st.markdown("### Coefficients")
                    st.markdown(f"a = {a}, b = {b}, c = {c}")

                    D = b**2 - 4*a*c
                    st.markdown("### Discriminant")
                    st.latex(f"D = {latex(D)}")

                    x1 = (-b + D**0.5) / (2*a)
                    x2 = (-b - D**0.5) / (2*a)

                    st.markdown("### Solutions")
                    st.latex(f"x_1 = {latex(x1)}")
                    st.latex(f"x_2 = {latex(x2)}")
            except:
                st.error("Invalid equation")

    # ---------- Step by Step ----------
    with colC:
        if st.button("🔹 Step by Step"):
            try:
                left, right = convert_math(eq).split("=")
                expr = expand(sympify(left) - sympify(right))

                a = expr.coeff(x, 2)
                b = expr.coeff(x, 1)
                c = expr.coeff(x, 0)

                if a == 0:
                    st.error("This is not a quadratic equation")
                else:
                    st.markdown("### Step 1: Write in standard form")
                    st.latex(f"{latex(expr)} = 0")

                    st.markdown("### Step 2: Identify coefficients")
                    st.markdown(f"a = {a}, b = {b}, c = {c}")

                    st.markdown("### Step 3: Compute discriminant")
                    D = b**2 - 4*a*c
                    st.latex(f"D = {latex(D)}")

                    st.markdown("### Step 4: Apply formula")
                    st.latex(r"x = \frac{-b \pm \sqrt{D}}{2a}")

                    x1 = (-b + D**0.5) / (2*a)
                    x2 = (-b - D**0.5) / (2*a)

                    st.markdown("### Final Answer")
                    st.latex(f"x_1 = {latex(x1)}")
                    st.latex(f"x_2 = {latex(x2)}")
            except:
                st.error("Invalid equation")

# ======================================================
# TAB 3 – Function Plot
# ======================================================
with tab3:
    st.subheader("Function Plot")
    func = st.text_input("Enter function (example: x^2 - 4x + 3)")

    if st.button("Plot Function"):
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
st.divider()
st.caption("© 2026 | Math AI – English Language Olympiad")
