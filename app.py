import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
import fitz  # PyMuPDF
import base64

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Dummy users for demo login
USERS = {
    "dr@example.com": {"password": "demo123", "role": "doctor"},
    "patient@example.com": {"password": "demo123", "role": "patient"}
}

# Session state login function
def login():
    st.title("🔐 Login to AI Health Agent")
    
    # Input fields
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Login"):
        user = USERS.get(email)

        # Check credentials
        if user and user["password"] == password:
            st.session_state.user = {"email": email, "role": user["role"]}
            st.rerun()  # replaces st.experimental_rerun()
        else:
            st.error("❌ Invalid email or password. Please try again.")


# New OpenAI function
def get_triage_response(symptoms):
    system_prompt = (
        "You are a medical triage assistant. Based on the user's symptoms, "
        "assess urgency (low/medium/high) and recommend next steps."
    )
    user_prompt = f"Symptoms: {symptoms}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content

def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

def patient_dashboard():
    st.header("🧑‍⚕️ Patient Dashboard")

    symptoms = st.text_area("Describe your symptoms:")
    if st.button("Submit for Triage"):
        if symptoms.strip():
            result = get_triage_response(symptoms)
            st.success("Triage Result:")
            st.write(result)
        else:
            st.warning("Please enter symptoms.")

    st.subheader("📤 Upload EHR Report (PDF)")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        with st.spinner("Extracting data..."):
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text", value=text, height=200)

def doctor_dashboard():
    st.header("👨‍⚕️ Doctor Dashboard")

    st.subheader("📈 User Activity Logs (Simulated)")
    data = pd.DataFrame({
        "Patient": ["Alice", "Bob", "Charlie", "David"],
        "Interactions": [5, 3, 6, 2]
    })
    st.dataframe(data)

    st.subheader("📊 Chart View")
    fig, ax = plt.subplots()
    ax.bar(data["Patient"], data["Interactions"], color="green")
    ax.set_title("Patient Interactions")
    st.pyplot(fig)

    st.subheader("📤 EHR Upload (PDF)")
    uploaded_file = st.file_uploader("Upload patient EHR", type="pdf")
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted EHR Text", value=text, height=200)

def main():
    if "user" not in st.session_state:
        login()
    else:
        user = st.session_state.user
        st.sidebar.write(f"Logged in as: `{user['email']}` ({user['role']})")
        if user["role"] == "doctor":
            doctor_dashboard()
        else:
            patient_dashboard()

        if st.sidebar.button("Logout"):
            del st.session_state.user
            st.experimental_rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="AI Health Agent", layout="centered")
    main()
