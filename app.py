import streamlit as st
from sympy import symbols, solve, sympify, latex, expand, sqrt
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
    st.image("elo_logo.png", width=250)
with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'> Math AI 🧮</h1>
    <p style='font-size:16px;'>
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
# Helper Functions
# =====================
def convert_math(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    return text


def equation_type(expr):
    poly = expr.as_poly(x)
    if not poly:
        return "Not a polynomial equation"
    deg = poly.degree()
    if deg == 1:
        return "Linear Equation (Degree 1)"
    elif deg == 2:
        return "Quadratic Equation (Degree 2)"
    else:
        return f"Polynomial Equation (Degree {deg})"


# =====================
# Tabs
# =====================
tab1, tab2, tab3 = st.tabs([
    "🔢 Basic Operations",
    "📐 Equation Solver",
    "📊 Function Plot",
])

# ---------------------
# Tab 1: Basic Operations
# ---------------------
with tab1:
    st.subheader("Basic Math Operations")

    a = st.number_input("First number", value=0.0)
    b = st.number_input("Second number", value=0.0)

    op = st.selectbox("Choose operation", ["Add", "Subtract", "Multiply", "Divide"])

    if st.button("Calculate", key="calc1"):
        if op == "Divide" and b == 0:
            st.error("❌ Cannot divide by zero")
        else:
            result = {
                "Add": a + b,
                "Subtract": a - b,
                "Multiply": a * b,
                "Divide": a / b
            }[op]

            st.markdown(f"""
            <div style="background:#e8f4ff;padding:15px;border-radius:10px;font-size:20px;">
            ✅ <strong>Result:</strong> {result}
            </div>
            """, unsafe_allow_html=True)

# ---------------------
# Tab 2: Equation Solver
# ---------------------
with tab2:
    st.subheader("Solve an Equation")

    st.markdown("### ✨ Quick Examples:")
    ex1, ex2, ex3 = st.columns(3)

    if ex1.button("x^2 - 5x + 6 = 0"):
        st.session_state.eq_input = "x^2 - 5x + 6 = 0"
    if ex2.button("2x + 3 = 7"):
        st.session_state.eq_input = "2x + 3 = 7"
    if ex3.button("x^2 + 4x + 5 = 0"):
        st.session_state.eq_input = "x^2 + 4x + 5 = 0"

    eq = st.text_input(
        "Enter equation (example: x^2 - 4x + 3 = 0)",
        value=st.session_state.get("eq_input", "")
    )

    st.markdown("### 🧠 Choose solving method:")
    c1, c2, c3 = st.columns(3)
    method = None
    if c1.button("📝 Step by Step"):
        method = "step"
    if c2.button("⚡ Direct Solve"):
        method = "direct"
    if c3.button("📐 Quadratic Formula"):
        method = "formula"

    if method and eq:
        try:
            left, right = convert_math(eq).split("=")
            expr = expand(sympify(left) - sympify(right))

            eq_type = equation_type(expr)
            st.info(f"📌 Equation Type: {eq_type}")

            poly = expr.as_poly(x)
            deg = poly.degree()

            # -------- Step by Step --------
            if method == "step":
                st.markdown("## ✏️ Step-by-Step Solution")
                st.latex(f"{latex(expr)} = 0")

                if deg == 1:
                    a_coef, b_coef = poly.all_coeffs()
                    st.latex(f"{a_coef}x + {b_coef} = 0")
                    sol = -b_coef / a_coef
                    st.latex(f"x = -({b_coef}) / ({a_coef}) = {sol}")

                elif deg == 2:
                    a_coef, b_coef, c_coef = poly.all_coeffs()
                    st.latex(f"a={a_coef},\\ b={b_coef},\\ c={c_coef}")
                    st.markdown("Try factoring:")
                    factors = expr.factor()
                    st.latex(latex(factors))
                    sols = solve(expr, x)
                    st.markdown("### Solutions:")
                    for s in sols:
                        st.latex(f"x = {latex(s)}")

                else:
                    st.warning("Detailed steps are available only for degree 1 and 2 equations.")

            # -------- Direct Solve --------
            elif method == "direct":
                st.markdown("## ⚡ Direct Solution")
                sols = solve(expr, x)
                for i, s in enumerate(sols, start=1):
                    st.latex(f"x_{i} = {latex(s)}")

            # -------- Quadratic Formula --------
            elif method == "formula":
                if deg == 2:
                    st.markdown("## 📐 Quadratic Formula")
                    a_coef, b_coef, c_coef = poly.all_coeffs()
                    delta = b_coef**2 - 4*a_coef*c_coef

                    st.latex(f"a={a_coef},\\ b={b_coef},\\ c={c_coef}")
                    st.latex(f"\\Delta = b^2 - 4ac = {delta}")
                    st.latex(r"x = \frac{-b \pm \sqrt{\Delta}}{2a}")

                    sol1 = (-b_coef + sqrt(delta))/(2*a_coef)
                    sol2 = (-b_coef - sqrt(delta))/(2*a_coef)

                    st.latex(f"x_1 = {latex(sol1)}")
                    st.latex(f"x_2 = {latex(sol2)}")
                else:
                    st.error("Quadratic Formula works only for quadratic equations.")

        except:
            st.error("❌ Invalid equation format")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")

    func = st.text_input("Enter function (example: x^2 - 4x + 3)")

    if st.button("📈 Plot Function"):
        try:
            f = sympify(convert_math(func))
            xs = np.linspace(-10, 10, 400)
            ys = [float(f.subs(x, i)) for i in xs]

            roots = solve(f, x)

            fig, ax = plt.subplots()
            ax.plot(xs, ys, label=str(f))

            for r in roots:
                if r.is_real:
                    ax.scatter(float(r), 0)

            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)
            ax.legend()

            st.pyplot(fig)

        except:
            st.error("❌ Invalid function")

# =====================
# Footer
# =====================
st.divider()
st.caption("© 2026 | English Language Olympiad — Math AI Educational Tool")
