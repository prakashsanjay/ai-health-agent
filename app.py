import streamlit as st
import openai
import pandas as pd
import datetime

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App Config
st.set_page_config(page_title="AI Health Agent", layout="centered")

st.title("🤖 AI Health Agent for Symptom Triage & Doctor Booking")
st.write("Describe your health issue and get AI-driven triage + book a doctor!")

# Step 1: Symptom Checker
st.header("🩺 Symptom Checker")
symptoms = st.text_area("Enter your symptoms (e.g., cough, fever, sore throat)...")

def get_triage(symptoms):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # explicitly pass the key
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",

        messages=[
            {"role": "system", "content": "You are an experienced medical triage assistant."},
            {"role": "user", "content": f"The patient reports the following symptoms: {symptoms}. Provide a triage level, suggested specialist, and any immediate advice in 2-3 lines."}
        ],
        max_tokens=250,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


# Step 2: Run AI Triage
if st.button("Analyze Symptoms"):
    if symptoms.strip():
        with st.spinner("Analyzing your symptoms..."):
            triage_result = get_triage(symptoms)
        st.success("✅ AI Triage Result:")
        st.markdown(triage_result)
    else:
        st.warning("Please enter some symptoms before analyzing.")

# Divider
st.markdown("---")

# Step 3: Booking Section
st.header("📅 Book an Appointment")

with st.form("appointment_form"):
    name = st.text_input("Your Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    appointment_date = st.date_input("Preferred Appointment Date", min_value=datetime.date.today())
    appointment_time = st.time_input("Preferred Time")
    submitted = st.form_submit_button("📨 Book Appointment")

    if submitted:
        if name and email and phone:
            st.success(f"✅ Appointment booked for {name} on {appointment_date} at {appointment_time}.")
            st.info("📧 You'll receive a confirmation email shortly. (Demo mode)")
        else:
            st.error("❗ Please fill in all fields to book an appointment.")

# Footer
st.markdown("---")
st.caption("Powered by OpenAI · Streamlit · Demo AI Agent")
