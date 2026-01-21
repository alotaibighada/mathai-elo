import streamlit as st
from sympy import symbols, solve, sympify, latex, expand
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# Page Configuration
# =====================
st.set_page_config(
    page_title="Math AI | ELO",  # <-- العنوان يظهر في تبويب المتصفح
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
    <h1 style='margin-bottom:0;'> Math AI</h1>
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
    "Math Operations",
    "Equation Solver",
    "Function Plot",
])

# ---------------------
# Tab 1: Math Operations
# ---------------------
with tab1:
    st.subheader("Basic Math Operations")
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
    st.subheader("Solve an Equation")
    eq = st.text_input("Enter equation (example: x^2 - 4x + 3 = 0)")

    st.markdown("**Choose solving method:**")
    col1, col2, col3 = st.columns(3)
    method = None
    if col1.button("Step by Step"):
        method = "Step by Step"
    if col2.button("Direct Solve"):
        method = "Direct Solve"
    if col3.button("Quadratic Formula"):
        method = "Quadratic Formula"

    if method and eq:
        try:
            left, right = convert_math(eq).split("=")
            expr = expand(sympify(left) - sympify(right))

            if method == "Step by Step":
                st.markdown("**Step by Step Solution:**")
                st.latex(f"{latex(expr)} = 0")

                poly = expr.as_poly(x)
                deg = poly.degree()

                if deg == 1:
                    a_coef, b_coef = poly.all_coeffs()
                    st.latex(f"{a_coef}*x + {b_coef} = 0")
                    sol = -b_coef / a_coef
                    st.latex(f"x = -({b_coef}) / ({a_coef}) = {sol}")

                elif deg == 2:
                    a_coef, b_coef, c_coef = poly.all_coeffs()
                    st.latex(f"a = {a_coef}, b = {b_coef}, c = {c_coef}")
                    try:
                        factors = expr.factor()
                        st.latex(f"Factored form: {latex(factors)}")
                        sols = solve(expr, x)
                        st.markdown("**Solutions:**")
                        for s in sols:
                            st.latex(f"x = {latex(s)}")
                    except:
                        st.markdown("Cannot factor easily, consider Quadratic Formula.")
                else:
                    st.markdown("Equation degree > 2, Step by Step limited.")

            elif method == "Direct Solve":
                st.markdown("**Direct Solve:**")
                st.latex(f"{latex(expr)} = 0")
                poly = expr.as_poly(x)
                deg = poly.degree()

                sols = solve(expr, x)
                st.markdown(f"Solutions for degree {deg} equation:")
                for i, s in enumerate(sols, start=1):
                    st.latex(f"x_{i} = {latex(s)}")

            elif method == "Quadratic Formula":
                poly = expr.as_poly(x)
                if poly.degree() == 2:
                    st.markdown("**Quadratic Formula Step by Step:**")
                    a_coef, b_coef, c_coef = poly.all_coeffs()
                    delta = b_coef**2 - 4*a_coef*c_coef
                    st.latex(f"Delta = b^2 - 4ac = ({b_coef})^2 - 4*({a_coef})*({c_coef}) = {delta}")
                    st.latex(f"x = (-b ± sqrt(Delta)) / (2a)")
                    if delta >= 0:
                        sol1 = (-b_coef + delta**0.5)/(2*a_coef)
                        sol2 = (-b_coef - delta**0.5)/(2*a_coef)
                        st.latex(f"x1 = {sol1}, x2 = {sol2}")
                    else:
                        st.latex("Complex roots exist (Delta < 0).")
                else:
                    st.error("Quadratic Formula works only for degree 2 equations.")

        except:
            st.error("Invalid equation format")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Plot a Function")
    func = st.text_input("Enter function (example: x^2 - 4x + 3)")
    if st.button("Plot Function", key="plot_func"):
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
