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
    st.image("elo_logo.png", width=300)
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
    st.markdown("**Tip for students:** Enter two numbers and select an operation to calculate.")
    a = st.number_input("First number", value=0.0)
    b = st.number_input("Second number", value=0.0)

    op = st.selectbox("Select Operation", ["Add", "Subtract", "Multiply", "Divide"])

    if st.button("Calculate", key="calc1"):
        if op == "Divide" and b == 0:
            st.error("Oops! Cannot divide by zero.")
        else:
            result = {
                "Add": a + b,
                "Subtract": a - b,
                "Multiply": a * b,
                "Divide": a / b
            }[op]
            st.success(f"The result is: {result}")

# ---------------------
# Tab 2: Equation Solver
# ---------------------
with tab2:
    st.subheader("Solve an Equation")
    st.markdown("**Tip for students:** Write equations like `x^2 - 4*x + 3 = 0`")
    eq = st.text_input("Enter your equation:")

    st.markdown("**Choose solving method:**")
    col1, col2, col3 = st.columns(3)
    method = None
    if col1.button("📝 Step by Step"):
        method = "Step by Step"
    if col2.button("⚡ Direct Solve"):
        method = "Direct Solve"
    if col3.button("📐 Quadratic Formula"):
        method = "Quadratic Formula"

    if method and eq:
        try:
            left, right = convert_math(eq).split("=")
            expr = expand(sympify(left) - sympify(right))
            poly = expr.as_poly(x)
            deg = poly.degree()

            # Step by Step
            if method == "Step by Step":
                st.markdown("**Step by Step Solution:**")
                st.latex(f"{latex(expr)} = 0")
                if deg == 1:
                    a_coef, b_coef = poly.all_coeffs()
                    st.markdown("Step 1: Identify coefficients for linear equation.")
                    st.latex(f"{a_coef}*x + {b_coef} = 0")
                    sol = -b_coef / a_coef
                    st.markdown("Step 2: Solve for x:")
                    st.latex(f"x = -({b_coef}) / ({a_coef}) = {sol}")
                elif deg == 2:
                    a_coef, b_coef, c_coef = poly.all_coeffs()
                    st.markdown("Step 1: Identify coefficients for quadratic equation.")
                    st.latex(f"a = {a_coef},\\ b = {b_coef},\\ c = {c_coef}")
                    try:
                        factors = expr.factor()
                        st.markdown("Step 2: Factor the equation if possible.")
                        st.latex(f"Factored form: {latex(factors)}")
                        sols = solve(expr, x)
                        st.markdown("Step 3: Solutions:")
                        for s in sols:
                            st.latex(f"x = {latex(s)}")
                    except:
                        st.markdown("Cannot factor easily. Consider using Quadratic Formula.")
                else:
                    st.markdown("Step by Step limited for equations degree > 2.")

            # Direct Solve
            elif method == "Direct Solve":
                st.markdown("**Direct Solve:**")
                sols = solve(expr, x)
                st.markdown(f"Solutions for degree {deg} equation:")
                for i, s in enumerate(sols, start=1):
                    st.latex(f"x_{i} = {latex(s)}")

            # Quadratic Formula
            elif method == "Quadratic Formula":
                if deg == 2:
                    a_coef, b_coef, c_coef = poly.all_coeffs()
                    delta = b_coef**2 - 4*a_coef*c_coef
                    st.markdown("**Quadratic Formula Step by Step:**")
                    st.latex(f"a = {a_coef},\\ b = {b_coef},\\ c = {c_coef}")
                    st.latex(f"\\Delta = b^2 - 4ac = ({b_coef})^2 - 4*({a_coef})*({c_coef}) = {delta}")
                    st.latex(f"x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}} = "
                             f"\\frac{{-({b_coef}) \\pm \\sqrt{{{delta}}}}}{{2*({a_coef})}}")
                    if delta >= 0:
                        sol1 = (-b_coef + delta**0.5)/(2*a_coef)
                        sol2 = (-b_coef - delta**0.5)/(2*a_coef)
                        st.markdown("Solutions:")
                        st.latex(f"x_1 = {sol1},\\ x_2 = {sol2}")
                    else:
                        st.markdown("Complex roots exist (Δ < 0).")
                else:
                    st.error("Quadratic Formula works only for degree 2 equations.")

        except:
            st.error("Invalid equation format. Please check your input.")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")
    st.markdown("**Tip for students:** Enter a function like `x^2 - 4*x + 3`")
    func = st.text_input("Enter function:")
    if st.button("Plot Function", key="plot_func"):
        try:
            f = sympify(convert_math(func))
            xs = np.linspace(-10, 10, 400)
            ys = [f.subs(x, i) for i in xs]
            fig, ax = plt.subplots()
            ax.plot(xs, ys, label=f"f(x) = {f}", color='blue')
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        except:
            st.error("Invalid function format. Please check your input.")

# =====================
# Footer
# =====================
st.divider()
st.caption("© 2026 | English Language Olympiad | Visit: mathai-elo.com")
