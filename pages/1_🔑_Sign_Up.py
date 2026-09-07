import streamlit as st

st.set_page_config(page_title="Hospital AI Portal - Register", page_icon="🔑", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f9;
    }
    .stButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1e7e34;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔑 Practitioner Registration")
st.write("Create a secure clinical account to access patient screening tools.")

if "users" not in st.session_state:
    st.session_state["users"] = {"doctor@hospital.com": "admin123"}

with st.form("signup_form"):
    full_name = st.text_input("Full Name", placeholder="Dr. Jane Doe")
    email = st.text_input("Hospital Email", placeholder="jane.doe@hospital.com")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Register Account")

if submit:
    if not email or not password:
        st.error("⚠️ Please fill in all required fields.")
    elif password != confirm_password:
        st.error("❌ Passwords do not match.")
    elif email in st.session_state["users"]:
        st.warning("⚠️ An account with this email already exists.")
    else:
        st.session_state["users"][email] = password
        st.success("✅ Registration successful! You can now log in on the main page.")