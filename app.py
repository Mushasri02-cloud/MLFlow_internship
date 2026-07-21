import streamlit as st
import requests

st.set_page_config(page_title="Enterprise MLOps Diabetes System", layout="wide")

st.title("🩺 End-to-End Clinical Decision Support Pipeline")
st.write("An enterprise MLOps platform pulling live predictions via a high-performance FastAPI backend REST engine.")

# --- SIDEBAR CONTROL UNIT ---
st.sidebar.header("🕹️ System Controls")
selected_model = st.sidebar.selectbox(
    "Active Deployment Architecture",
    ["Random_Forest", "Logistic_Regression"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🏗️ System Architecture Flow")
st.sidebar.graphviz_chart('''
digraph G {
    node [shape=box, style=filled, color="#E1F5FE", fontname="Helvetica", fontsize=10];
    edge [color="#0288D1", arrowhead=vee];
    
    "Streamlit UI" -> "FastAPI Layer (Port 8000)" [label=" HTTP POST"];
    "FastAPI Layer (Port 8000)" -> "MLflow Server (Port 5000)" [label=" Fetch Binary"];
}
''')

# --- DATA ENTRY FORM LAYER ---
st.markdown("### 📋 Patient Vitals Entry Form")
col1, col2 = st.columns(2)
with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=2, step=1)
    glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=115, step=1)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=150, value=70, step=1)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=22, step=1)
with col2:
    insulin = st.number_input("Insulin Level (mu U/ml)", min_value=0, max_value=900, value=75, step=1)
    bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, max_value=70.0, value=26.5, step=0.1)
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.45, step=0.01)
    age = st.number_input("Age (Years)", min_value=1, max_value=120, value=30, step=1)

if st.button("Run Real-Time Inference", type="primary"):
    if glucose == 0 or bmi == 0.0 or blood_pressure == 0:
        st.warning("⚠️ Data Quality Guardrail: Core anatomical values (Glucose, BMI, Blood Pressure) cannot be zero.")
    else:
        # Format the exact JSON schema that our FastAPI server expects
        payload = {
            "Pregnancies": int(pregnancies),
            "Glucose": float(glucose),
            "BloodPressure": float(blood_pressure),
            "SkinThickness": float(skin_thickness),
            "Insulin": float(insulin),
            "BMI": float(bmi),
            "DiabetesPedigreeFunction": float(dpf),
            "Age": int(age)
        }
        
        try:
            # Send the data to FastAPI via an HTTP POST request
            fastapi_url = f"http://127.0.0.1:8000/predict/{selected_model}"
            response = requests.post(fastapi_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["diabetic_risk_flag"]
                status_text = result["clinical_status"]
                
                st.markdown("---")
                st.markdown("### 🔮 Diagnostic Assessment Output")
                if prediction == 1:
                    st.error(f"⚠️ Clinical Warning: {status_text} by {selected_model}.")
                else:
                    st.success(f"💚 Clinical Notification: {status_text} by {selected_model}.")
            else:
                st.error(f"Error from API server: {response.text}")
                
        except Exception as conn_err:
            st.error(f"Could not connect to FastAPI server on Port 8000. Is it running? Details: {conn_err}")