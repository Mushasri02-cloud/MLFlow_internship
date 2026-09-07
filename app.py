import streamlit as st

st.set_page_config(page_title="Hospital AI Portal - Login", page_icon="🏥", layout="centered")

# Hospital Themed Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f9;
    }
    .main-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        border-top: 5px solid #0056b3;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .hospital-title {
        color: #0056b3;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #6c757d;
        text-align: center;
        font-size: 14px;
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #0056b3;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #003d80;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "users" not in st.session_state:
    st.session_state["users"] = {"doctor@hospital.com": "admin123"}

st.markdown("""
    <div class="main-card">
        <h2 class="hospital-title">🏥 Clinical AI Decision Portal</h2>
        <p class="sub-title">Diabetes Risk Prediction & Patient Care System</p>
    </div>
""", unsafe_allow_html=True)

st.subheader("🔑 Practitioner Login")

with st.form("login_form"):
    email = st.text_input("Hospital Email / ID", placeholder="doctor@hospital.com")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Sign In")

if submit:
    if email in st.session_state["users"] and st.session_state["users"][email] == password:
        st.session_state["logged_in"] = True
        st.session_state["user_email"] = email
        st.success("✅ Login successful! Go to the 'Diabetes Risk' page in the sidebar.")
    else:
        st.error("❌ Invalid credentials. Please try again or Sign Up.")

if st.session_state["logged_in"]:
    st.info(f"Currently logged in as: **{st.session_state['user_email']}**")