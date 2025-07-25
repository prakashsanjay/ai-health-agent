import streamlit as st
import datetime
from openai import OpenAI
import os

# Set your OpenAI API key (make sure you also set this in Streamlit secrets or environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App layout
st.set_page_config(page_title="AI Health Agent", page_icon="🏥", layout="centered")

st.title("🏥 AI Health Agent")

# Symptom checker
st.header("🤔 Symptom Checker")
symptoms = st.text_area("Describe your symptoms", placeholder="I am suffering from cough and cold")

if st.button("Check Urgency"):
    if symptoms:
        with st.spinner("Analyzing symptoms..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional healthcare triage assistant."},
                    {"role": "user", "content": f"My symptoms are: {symptoms}. How urgent is this and what should I do next?"}
                ]
            )
            st.success(response.choices[0].message.content.strip())
    else:
        st.warning("Please enter your symptoms.")

# Appointment booking
st.header("📅 Book an Appointment")
appt_date = st.date_input("Choose date", datetime.date.today())
appt_time = st.time_input("Choose time", datetime.datetime.now().time())
if st.button("Book"):
    st.success(f"✅ Appointment booked on {appt_date} at {appt_time}!")

