import streamlit as st
from sympy import symbols, solve, sympify, latex, expand
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# Page Configuration
# =====================
st.set_page_config(
    page_title="Math AI | ELO Creative",
    layout="wide"
)

# =====================
# Symbols & Session State
# =====================
x = symbols("x")

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# For quiz results
if 'quiz_answer' not in st.session_state:
    st.session_state.quiz_answer = 0.0
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'quiz_result' not in st.session_state:
    st.session_state.quiz_result = ""

# =====================
# Helper Functions
# =====================
def convert_math(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    return text

def add_to_history(eq, solution):
    st.session_state.history.append({'equation': eq, 'solution': solution})

# =====================
# Header
# =====================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("elo_logo.png", width=250)
with col2:
    st.markdown("""
    <h1 style='color:blue; margin-bottom:0;'>Math AI 🧮</h1>
    <p>Official Training Platform for ELO</p>
    """, unsafe_allow_html=True)

st.divider()

# =====================
# Tabs
# =====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔢 Math Operations",
    "📐 Equation Solver",
    "📊 Function Plot",
    "🎯 Quiz & History"
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
    st.subheader("Equation Solver")
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

            sols = solve(expr, x)

            # Display solutions depending on method
            if method == "Direct Solve":
                st.markdown("**Solution:**")
                for s in sols:
                    st.latex(f"x = {latex(s)}")
            elif method == "Quadratic Formula":
                degree = expr.as_poly(x).degree()
                coeffs = expr.as_poly(x).all_coeffs()
                if degree == 2:
                    a_q, b_q, c_q = coeffs
                    st.markdown("**Quadratic Formula:**")
                    st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                    st.markdown(f"Here, a = {a_q}, b = {b_q}, c = {c_q}")
                    delta = b_q**2 - 4*a_q*c_q
                    x1 = (-b_q + delta**0.5) / (2*a_q)
                    x2 = (-b_q - delta**0.5) / (2*a_q)
                    st.markdown("**Solution:**")
                    st.latex(f"x_1 = {latex(x1)}, \\quad x_2 = {latex(x2)}")
                    sols = [x1, x2]
                else:
                    st.warning("Quadratic formula only works for degree 2. Using Direct Solve instead.")
            elif method == "Step by Step":
                st.markdown("**Step 1: Expand equation**")
                st.latex(f"{latex(expr)} = 0")
                factored = expr.factor()
                if factored != expr:
                    st.markdown("**Step 2: Factor equation**")
                    st.latex(f"{latex(factored)} = 0")
                st.markdown("**Step 3: Solve equation**")
                for s in sols:
                    st.latex(f"x = {latex(s)}")

            # ===== Quiz Form =====
            st.markdown("---")
            st.markdown("### Quiz: Identify the largest solution")
            with st.form("quiz_form"):
                st.session_state.quiz_answer = st.number_input(
                    "Enter the largest solution (x value) of the equation:",
                    value=st.session_state.quiz_answer
                )
                submit = st.form_submit_button("Submit Answer")
                if submit:
                    st.session_state.quiz_submitted = True
                    if float(st.session_state.quiz_answer) == float(max(sols)):
                        st.session_state.quiz_result = "✅ Correct!"
                        st.session_state.points += 1
                    else:
                        st.session_state.quiz_result = f"❌ Incorrect! Correct answer: {max(sols)}"
                    add_to_history(eq, sols)

            if st.session_state.quiz_submitted:
                st.info(st.session_state.quiz_result)

        except:
            st.error("Invalid equation format")

# ---------------------
# Tab 3: Function Plot
# ---------------------
with tab3:
    st.subheader("Function Plot")
    func = st.text_input("Enter function (example: x^2 - 4x + 3)")
    plot_button = st.button("Plot Function", key="plot_func")
    if plot_button:
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

# ---------------------
# Tab 4: Quiz & History
# ---------------------
with tab4:
    st.subheader("Your Points & History")
    st.markdown(f"**Points:** {st.session_state.points}")
    if st.session_state.history:
        st.markdown("**History of solved equations:**")
        for i, item in enumerate(st.session_state.history, 1):
            st.markdown(f"{i}. Equation: `{item['equation']}`, Solution: `{item['solution']}`")

# =====================
# Footer
# =====================
st.divider()
st.caption("© 2026 | English Language Olympiad")
