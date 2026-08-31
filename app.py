import streamlit as st
import pandas as pd
import pickle
import lightgbm 

st.set_page_config(
    page_title="Retinopathy Screening Tool", page_icon="👁️", layout="centered"
)

@st.cache_resource
def load_sc():
    with open("Models/standard_scalar.pkl",'rb') as file:
        sc=pickle.load(file)
    return sc

@st.cache_resource
def load_lgbm():
    with open("Models/lgbm_tuned.pkl",'rb') as file:
        lgbm=pickle.load(file)
    return lgbm

def process_input(data):
    user_input_df=pd.DataFrame([data])
    scaled_data=load_sc().transform(user_input_df)
    return scaled_data

st.title("👁️ Retinopathy Disease Risk Prediction")
st.info("""
This application is an ML-based clinical screening tool designed to assess a patient's risk of **Retinopathy** based on clinical indicators such as age, blood pressure, and cholesterol levels. 

* **Model Architecture:** Powered by a fine-tuned **LightGBM** classifier optimized for high sensitivity (Recall).
* **Purpose:** Built to assist in early detection and preliminary risk stratification. 
""")

st.divider()

with st.sidebar:
    st.title("Patient Parameters")
    age = st.slider("Age", 1, 120, 45)
    systolic_bp = st.number_input("Systolic BP (mmHg)", value=120.0)
    diastolic_bp = st.number_input("Diastolic BP (mmHg)", value=80.0)
    cholesterol = st.number_input("Cholesterol (mg/dL)", value=200.0)

    submit_btn = st.button("Assess Risk", type="primary")

if submit_btn:
    user_input={
        "age":age,
        "systolic_bp":systolic_bp,
        "diastolic_bp":diastolic_bp,
        "cholesterol":cholesterol
    }
    scaled_data=process_input(user_input)
    lgbm=load_lgbm()
    preds_proba=lgbm.predict_proba(scaled_data)
    
    st.subheader("Assessment Results")
    risk_percentage = preds_proba[0][1] * 100
    safe_percentage = preds_proba[0][0] * 100

    if preds_proba[0][1]>0.4:
        st.error(
            f"**High Risk Detected** — The model estimates a"
            f" **{risk_percentage:.1f}%** probability of retinopathy."
        )
        st.warning(
            "💡 **Recommendation:** Clinical follow-up and diagnostic confirmation"
            " are strongly advised."
        )
    else:
        st.success(
            f"**Low Risk** — The model estimates a **{safe_percentage:.1f}%**"
            " probability of a healthy profile."
        )
        st.info(
            "💡 **Recommendation:** Maintain regular health check-ups as per"
            " routine guidelines."
        )