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
# Language & Theme Selector
# =====================
col_lang, col_theme = st.columns([1, 1])
with col_lang:
    language = st.selectbox("Choose Language / اختر اللغة:", ["English", "عربي"])
with col_theme:
    theme = st.radio("Choose Theme / اختر الوضع:", ["Light", "Dark"])

# =====================
# Texts Dictionary
# =====================
texts = {
    "English": {
        "title": "Math AI 🧮",
        "subtitle": "Official Training Platform for English Language Olympiad (ELO)",
        "math_ops": "Basic Math Operations",
        "first_number": "First number",
        "second_number": "Second number",
        "operation": "Operation",
        "calculate": "Calculate",
        "equation_solver": "Solve an Equation",
        "enter_eq": "Enter equation (example: x^2 - 4x + 3 = 0)",
        "choose_method": "Choose solution method:",
        "direct_solve": "Direct Solve",
        "quadratic_formula": "Quadratic Formula",
        "step_by_step": "Step by Step",
        "plot_function": "Plot a Function",
        "enter_func": "Enter function (example: x^2 - 4x + 3)"
    },
    "عربي": {
        "title": "ذكاء رياضي 🧮",
        "subtitle": "المنصة الرسمية لتدريب أولمبياد اللغة الإنجليزية",
        "math_ops": "العمليات الحسابية الأساسية",
        "first_number": "الرقم الأول",
        "second_number": "الرقم الثاني",
        "operation": "العملية",
        "calculate": "احسب",
        "equation_solver": "حل المعادلة",
        "enter_eq": "ادخل المعادلة (مثال: x^2 - 4x + 3 = 0)",
        "choose_method": "اختر طريقة الحل:",
        "direct_solve": "الحل المباشر",
        "quadratic_formula": "القانون العام",
        "step_by_step": "خطوة بخطوة",
        "plot_function": "رسم الدالة",
        "enter_func": "ادخل الدالة (مثال: x^2 - 4x + 3)"
    }
}

# =====================
# Apply Theme
# =====================
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {background-color:#121212;}
        .css-1v3fvcr {color:white;}
        </style>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {background-color:white;}
        .css-1v3fvcr {color:black;}
        </style>
        """, unsafe_allow_html=True
    )

# =====================
# Header & Logo
# =====================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("elo_logo.png", width=None, use_column_width=True)
with col2:
    st.markdown(f"""
    <h1 style='margin-bottom:0; font-size:calc(24px + 1vw);'>{texts[language]["title"]}</h1>
    <p style='font-size:calc(12px + 0.5vw);'>{texts[language]["subtitle"]}</p>
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
    st.subheader(texts[language]["math_ops"])
    a = st.number_input(texts[language]["first_number"], value=0.0)
    b = st.number_input(texts[language]["second_number"], value=0.0)
    op = st.selectbox(texts[language]["operation"], ["Add", "Subtract", "Multiply", "Divide"])
    if st.button(texts[language]["calculate"], key="calc1"):
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
    st.subheader(texts[language]["equation_solver"])
    eq = st.text_input(texts[language]["enter_eq"])
    method = st.radio(
        texts[language]["choose_method"],
        [texts[language]["direct_solve"], texts[language]["quadratic_formula"], texts[language]["step_by_step"]]
    )

    if st.button(texts[language]["calculate"], key="solve_eq"):
        try:
            left, right = convert_math(eq).split("=")
            expr = expand(sympify(left) - sympify(right))
            st.latex(f"{latex(expr)} = 0")

            # Direct Solve
            if method == texts[language]["direct_solve"]:
                sols = solve(expr, x)
                for s in sols:
                    st.latex(f"x = {latex(s)}")

            # Quadratic Formula
            elif method == texts[language]["quadratic_formula"]:
                degree = expr.as_poly(x).degree()
                coeffs = expr.as_poly(x).all_coeffs()
                if degree == 2:
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
                    st.warning(f"Quadratic formula only works for degree 2 equations. Using Direct Solve instead.")
                    sols = solve(expr, x)
                    for s in sols:
                        st.latex(f"x = {latex(s)}")

            # Step by Step
            elif method == texts[language]["step_by_step"]:
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
    st.subheader(texts[language]["plot_function"])
    func = st.text_input(texts[language]["enter_func"])
    if st.button(texts[language]["calculate"], key="plot_func"):
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
