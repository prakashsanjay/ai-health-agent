import streamlit as st
import openai
import pandas as pd
import altair as alt

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Simulated users for role-based login
USERS = {
    "doctor@example.com": {"password": "doc123", "role": "doctor"},
    "patient@example.com": {"password": "demo123", "role": "patient"}  # Updated password
}

# Login function
def login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = USERS.get(email)
        if user and user["password"] == password:
            st.session_state.user = {"email": email, "role": user["role"]}
            st.experimental_rerun()
        else:
            st.error("❌ Invalid email or password. Please try again.")

# Symptom triage function using GPT
@st.cache_data(show_spinner=True)
def get_triage_response(symptoms):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an experienced healthcare triage assistant."},
            {"role": "user", "content": f"The patient reports the following symptoms: {symptoms}. Provide a likely triage category and brief advice."}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Patient symptom checker (no login required)
def public_symptom_checker():
    st.subheader("🤖 AI Symptom Triage Agent")
    symptoms = st.text_area("Describe your symptoms")
    if st.button("Submit Symptoms"):
        if symptoms.strip():
            with st.spinner("Analyzing your symptoms..."):
                result = get_triage_response(symptoms)
            st.success("Triage Result:")
            st.write(result)
        else:
            st.warning("Please enter symptoms before submitting.")

# Doctor Dashboard with sample analytics
def doctor_dashboard():
    st.subheader("💼 Doctor Dashboard")
    data = pd.DataFrame({
        "Users": ["patient1@example.com", "patient2@example.com", "patient3@example.com"],
        "Activity Count": [5, 3, 7]
    })
    chart = alt.Chart(data).mark_bar().encode(
        x='Users',
        y='Activity Count',
        color='Users'
    ).properties(width=600)
    st.altair_chart(chart)
    st.write("(Analytics is sample data; integrate with backend or logging system.)")

# Main app logic
def main():
    st.set_page_config(page_title="AI Health Agent", layout="centered")
    st.title("🧑‍⚕️ Welcome to the AI Health Agent")

    # Always show public triage agent
    public_symptom_checker()

    st.markdown("---")

    # Optional login for dashboard
    if "user" not in st.session_state:
        st.subheader("🔐 Login for Doctor Dashboard")
        login()
    else:
        role = st.session_state.user["role"]
        email = st.session_state.user["email"]
        st.sidebar.success(f"Logged in as: {email} ({role})")
        if st.sidebar.button("Logout"):
            del st.session_state.user
            st.experimental_rerun()

        if role == "doctor":
            doctor_dashboard()

if __name__ == "__main__":
    main()
