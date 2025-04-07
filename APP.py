import streamlit as st
import numpy as np
import joblib

# 页面配置
st.set_page_config(
    page_title="ML Prediction of Phosphate Adsorption",
    layout="centered"
)

# 小清新样式 + 黄金比例排版
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        max-width: 610px;  /* 宽度被限制，营造“高大感” */
        margin: auto;
        background-color: #f9fcfb;
        padding: 2.2rem 2rem 5rem 2rem;
    }
    h1 {
        font-size: 2.3rem;
        margin-bottom: 0.4rem;
    }
    .stMarkdown h1 + p {
        font-size: 1.05rem;
        color: #4f4f4f;
        margin-bottom: 1.7rem;
    }
    .stNumberInput label {
        font-size: 1rem;
        font-weight: 500;
    }
    .stButton>button {
        background-color: #4caf91;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        border: none;
        margin-top: 1.3rem;
    }
    .stSuccess {
        background-color: #e6f9ed;
        color: #1b5e20;
        padding: 0.95rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 标题与说明
st.title("🧪 ML Prediction of Phosphate Adsorption on Mg@SBC/CS")

st.markdown("""
This application predicts the phosphate adsorption capacity (mg/g) of Mg@SBC/CS under specified experimental conditions.  
Please enter the relevant parameters below:
""")

# 输入字段（竖排，保持黄金高宽比视觉）
ads_time = st.number_input("⏱ Adsorption Time (min)", min_value=0.0, value=120.0, step=1.0)
pH = st.number_input("🌡 Solution pH", min_value=1.0, max_value=14.0, value=7.0, step=0.1)
dosage = st.number_input("🧪 Adsorbent Dosage (g/L)", min_value=0.0, value=1.0, step=0.1)
c0 = st.number_input("💧 Initial Phosphate Concentration (mg/L)", min_value=0.0, value=50.0, step=1.0)
temperature = st.number_input("🌤 Temperature (°C)", min_value=0.0, value=25.0, step=1.0)

# 加载模型
@st.cache_resource
def load_model():
    return joblib.load("Catboost.pkl")

model = load_model()

# 预测按钮与展示
if st.button("🔍 Predict Adsorption Capacity"):
    input_data = np.array([[ads_time, pH, dosage, c0, temperature]])
    prediction = model.predict(input_data)[0]
    st.success(f"✅ Predicted Phosphate Adsorption Capacity: **{prediction:.2f} mg/g**")
