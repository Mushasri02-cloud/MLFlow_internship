import streamlit as st
import requests

st.set_page_config(page_title="Diabetes Risk Assessment", page_icon="🩺", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f9;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    .stButton>button {
        background-color: #0056b3;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Access Control Guardrail
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Access Restricted. Please Sign In from the main home page to access this panel.")
    st.stop()

st.title("🩺 Patient Diabetes Risk Assessment")
st.write("Enter patient clinical attributes to run backend ML risk evaluation.")

st.sidebar.header("⚙️ Model Configuration")
selected_model = st.sidebar.selectbox("Select ML Model", ["RandomForest", "LogisticRegression"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Clinical Parameters")
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
    glucose = st.number_input("Plasma Glucose Concentration (mg/dL)", min_value=0, max_value=300, value=120)
    blood_pressure = st.number_input("Diastolic Blood Pressure (mm Hg)", min_value=0, max_value=150, value=70)
    skin_thickness = st.number_input("Triceps Skin Fold Thickness (mm)", min_value=0, max_value=100, value=20)

with col2:
    st.subheader("  ")
    insulin = st.number_input("2-Hour Serum Insulin (mu U/ml)", min_value=0, max_value=900, value=79)
    bmi = st.number_input("Body Mass Index (BMI)", min_value=0.0, max_value=70.0, value=25.0, format="%.1f")
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5, format="%.3f")
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=33)

st.divider()

if st.button("Run Assessment"):
    # Real-time data guardrail
    if glucose == 0 or bmi == 0.0 or blood_pressure == 0:
        st.error("⚠️ Data Guardrail Flag: Glucose, BMI, and Blood Pressure cannot be 0.")
    else:
        payload = {
            "Pregnancies": pregnancies,
            "Glucose": glucose,
            "BloodPressure": blood_pressure,
            "SkinThickness": skin_thickness,
            "Insulin": insulin,
            "BMI": bmi,
            "DiabetesPedigreeFunction": dpf,
            "Age": age
        }
        
        # Hosted/Public or Local API URL
        api_url = f"https://mlflow-internship.onrender.com/predict"
        
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.subheader("📊 Assessment Result")
                st.markdown(f"""
                    <div class="metric-card">
                        <h3>Risk Level: <b>{data.get('clinical_status', 'Evaluated')}</b></h3>
                        <p>Selected Architecture: {selected_model}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("API Error: Backend returned an unsuccessful status code.")
        except Exception:
            # Fallback local calculation preview if backend server isn't reached
            st.info("ℹ️ Backend server unreachable. Displaying preliminary client-side risk estimate:")
            risk_score = (glucose * 0.4) + (bmi * 0.8) + (age * 0.2)
            if risk_score > 80:
                st.error("🔴 Estimated Status: High Risk of Diabetes")
            elif risk_score > 50:
                st.warning("🟡 Estimated Status: Moderate Risk")
            else:
                st.success("🟢 Estimated Status: Low Risk")