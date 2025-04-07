import streamlit as st
import numpy as np
import pandas as pd
import joblib
from io import BytesIO

# 页面配置
st.set_page_config(
    page_title="Phosphate Adsorption Prediction",
    layout="centered"
)

# 🌿 样式：小清新 + 自定义标题大小
st.markdown("""
    <style>
    .stApp {
        max-width: 610px;
        margin: auto;
        background-color: #f9fcfb;
        padding: 2rem 2rem 4rem 2rem;
    }
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    .custom-title {
        font-size: 1.5rem;
        margin-bottom: 0.2rem;
        line-height: 1.3;
        font-weight: 600;
        color: #222;
    }
    .stMarkdown h1 + p {
        font-size: 1.02rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .stNumberInput label {
        font-size: 0.98rem;
        font-weight: 500;
        color: #333;
    }
    .stButton>button {
        background-color: #4caf91;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.55rem 1.1rem;
        border-radius: 10px;
        border: none;
        margin-top: 1.3rem;
    }
    .stSuccess {
        background-color: #e6f9ed;
        color: #1b5e20;
        padding: 0.85rem;
        border-radius: 8px;
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 模型加载
@st.cache_resource
def load_model():
    return joblib.load("Catboost.pkl")

model = load_model()

# 🌐 中英切换
lang = st.radio("🌐 Language / 语言", ["English", "中文"], horizontal=True)

# 文本内容（语言包）
text = {
    "English": {
        "title": "🔬 Machine learning prediction of phosphate adsorption on Mg@SBC/CS",
        "description": "This application predicts the phosphate adsorption capacity (mg/g) of Mg@SBC/CS under specified experimental conditions.",
        "input_labels": [
            "⏱ Adsorption Time (min)",
            "🌡 Solution pH",
            "🧪 Adsorbent Dosage (g/L)",
            "💧 Initial Phosphate Concentration (mg/L)",
            "🌤 Temperature (°C)"
        ],
        "button_predict": "🔍 Predict Adsorption Capacity",
        "button_export": "📁 Export CSV",
        "result_prefix": "✅ Predicted phosphate adsorption capacity:",
        "file_name": "prediction_result.csv"
    },
    "中文": {
        "title": "🔬 Mg@SBC/CS 对磷酸盐吸附的机器学习预测",
        "description": "本应用基于实验条件预测 Mg@SBC/CS 对磷酸盐的单位吸附量（mg/g）。",
        "input_labels": [
            "⏱ 吸附时间 (分钟)",
            "🌡 溶液 pH",
            "🧪 吸附剂投加量 (g/L)",
            "💧 初始磷酸盐浓度 (mg/L)",
            "🌤 温度 (°C)"
        ],
        "button_predict": "🔍 预测吸附量",
        "button_export": "📁 导出 CSV",
        "result_prefix": "✅ 预测的磷酸盐吸附量为：",
        "file_name": "预测结果.csv"
    }
}[lang]

# 🎯 页面内容
st.markdown(f'<h1 class="custom-title">{text["title"]}</h1>', unsafe_allow_html=True)
st.markdown(text["description"])

# 输入字段
ads_time = st.number_input(text["input_labels"][0], min_value=0.0, value=120.0, step=1.0)
pH = st.number_input(text["input_labels"][1], min_value=1.0, max_value=14.0, value=7.0, step=0.1)
dosage = st.number_input(text["input_labels"][2], min_value=0.0, value=1.0, step=0.1)
c0 = st.number_input(text["input_labels"][3], min_value=0.0, value=50.0, step=1.0)
temperature = st.number_input(text["input_labels"][4], min_value=0.0, value=25.0, step=1.0)

# 🧠 预测 & 导出数据
prediction = None
df_result = None

if st.button(text["button_predict"]):
    input_data = np.array([[ads_time, pH, dosage, c0, temperature]])
    prediction = model.predict(input_data)[0]
    st.success(f"{text['result_prefix']} **{prediction:.2f} mg/g**")

    # 构建结果 DataFrame
    df_result = pd.DataFrame([{
        "Time": ads_time,
        "pH": pH,
        "Dosage (g/L)": dosage,
        "C0 (mg/L)": c0,
        "Temperature (°C)": temperature,
        "Predicted Adsorption (mg/g)": round(prediction, 2)
    }])

# 📁 导出 CSV 按钮
if prediction is not None and df_result is not None:
    towrite = BytesIO()
    df_result.to_csv(towrite, index=False)
    st.download_button(
        label=text["button_export"],
        data=towrite.getvalue(),
        file_name=text["file_name"],
        mime="text/csv"
    )


