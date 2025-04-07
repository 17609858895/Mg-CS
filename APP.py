import streamlit as st
import numpy as np
import joblib

# 页面设置
st.set_page_config(page_title="机器学习预测Mg@SBC/CS对磷酸盐的吸附", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f7fcfc;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# 页面标题
st.title("🌿 机器学习预测Mg@SBC/CS对磷酸盐的吸附")
st.markdown("请填写以下实验条件，模型将预测磷酸盐的吸附量（mg/g）：")

# 输入区域
col1, col2 = st.columns(2)

with col1:
    time = st.number_input("⏱ Time (min)", min_value=0.0, value=120.0, step=1.0)
    pH = st.number_input("🧪 pH", min_value=1.0, max_value=14.0, value=7.0, step=0.1)
    dosage = st.number_input("💊 Dosage (g/L)", min_value=0.0, value=1.0, step=0.1)

with col2:
    c0 = st.number_input("🔬 C0 初始浓度 (mg/L)", min_value=0.0, value=50.0, step=1.0)
    temp = st.number_input("🌡 Temp 温度 (°C)", min_value=0.0, value=25.0, step=1.0)

# 加载模型
@st.cache_resource
def load_model():
    return joblib.load("Catboost.pkl")

model = load_model()

# 预测按钮
if st.button("🔍 预测"):
    input_data = np.array([[time, pH, dosage, c0, temp]])
    prediction = model.predict(input_data)[0]
    st.success(f"✅ 预测磷酸盐的吸附量为：{prediction:.2f} mg/g")
