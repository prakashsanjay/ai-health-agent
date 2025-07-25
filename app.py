
import streamlit as st
import openai
import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Initialize session state
if 'role' not in st.session_state:
    st.session_state.role = None

# Title
st.set_page_config(page_title="AI Health Agent", layout="wide")
st.title("🏥 AI Health Agent")

# Sidebar login
with st.sidebar:
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email == "dr@example.com" and password == "demo123":
            st.session_state.role = "doctor"
        elif email == "patient@example.com" and password == "demo123":
            st.session_state.role = "patient"
        else:
            st.error("Invalid credentials")

# Functions
def symptom_triage(symptoms):
    prompt = f"""
    Act as a medical assistant. A patient reports the following symptoms: {symptoms}.
    Provide an urgency level (Low, Medium, High) and a brief recommendation.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def extract_icd_codes_from_pdf(uploaded_file):
    text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    # Simulated ICD/CPT extraction (in real case, use regex or LLM)
    codes = ["ICD-10: R51", "CPT: 99213"] if "headache" in text.lower() else ["No clear codes found"]
    return codes, text

# Main
if st.session_state.role == "patient":
    st.subheader("🤒 Symptom Checker")
    symptoms = st.text_area("Describe your symptoms")
    if st.button("Check Urgency"):
        result = symptom_triage(symptoms)
        st.success(result)

    st.subheader("📅 Book an Appointment")
    date = st.date_input("Choose date")
    time = st.time_input("Choose time")
    if st.button("Book"):
        st.success(f"Appointment booked for {date} at {time}")

elif st.session_state.role == "doctor":
    st.subheader("📄 Upload EHR (PDF)")
    uploaded_file = st.file_uploader("Upload patient's medical record", type="pdf")
    if uploaded_file:
        codes, text = extract_icd_codes_from_pdf(uploaded_file)
        st.text_area("Extracted Text", text, height=200)
        st.write("🔍 Extracted Codes:")
        for code in codes:
            st.code(code)

    st.subheader("📊 Patient Activity Analytics")
    data = pd.DataFrame({
        "Activity": ["Check Triage", "Upload EHR", "Book Appointment"],
        "Count": [10, 7, 14]
    })
    fig, ax = plt.subplots()
    ax.bar(data["Activity"], data["Count"], color="skyblue")
    st.pyplot(fig)

elif st.session_state.role is None:
    st.info("Please login from the sidebar to continue.")
