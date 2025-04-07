import streamlit as st
import numpy as np
import joblib

# Page configuration
st.set_page_config(
    page_title="ML Prediction of Phosphate Adsorption on Mg@SBC/CS",
    layout="centered"
)

# Custom styling for minimal and clean look
st.markdown("""
    <style>
    .stApp {
        background-color: #f9fcfb;
        font-family: "Segoe UI", sans-serif;
    }
    .stButton>button {
        background-color: #4caf91;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        border: none;
    }
    .stNumberInput>div>div>input {
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #dcdcdc;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🧪 ML Prediction of Phosphate Adsorption on Mg@SBC/CS")

st.markdown("""
This application predicts the phosphate adsorption capacity (mg/g) of Mg@SBC/CS based on experimental conditions.  
Please enter the relevant parameters below:
""")

# Inputs – vertically aligned
ads_time = st.number_input("⏱ Adsorption Time (min)", min_value=0.0, value=120.0, step=1.0)
pH = st.number_input("🧪 Solution pH", min_value=1.0, max_value=14.0, value=7.0, step=0.1)
dosage = st.number_input("💊 Adsorbent Dosage (g/L)", min_value=0.0, value=1.0, step=0.1)
c0 = st.number_input("🔬 Initial Phosphate Concentration (mg/L)", min_value=0.0, value=50.0, step=1.0)
temperature = st.number_input("🌡 Temperature (°C)", min_value=0.0, value=25.0, step=1.0)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("Catboost.pkl")

model = load_model()

# Predict button
if st.button("🔍 Predict Adsorption Capacity"):
    input_data = np.array([[ads_time, pH, dosage, c0, temperature]])
    prediction = model.predict(input_data)[0]
    st.success(f"✅ Predicted Phosphate Adsorption Capacity: **{prediction:.2f} mg/g**")
