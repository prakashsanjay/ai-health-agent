import streamlit as st
import openai

# Securely load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Page config ---
st.set_page_config(page_title="AI Health Agent", layout="centered")

# --- Session State for Role Management ---
if "role" not in st.session_state:
    st.session_state.role = None

# --- Login Logic ---
def login():
    st.title("🩺 AI Health Agent Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if email == "dr@example.com" and password == "demo123":
            st.session_state.role = "doctor"
        elif email == "patient@example.com" and password == "demo123":
            st.session_state.role = "patient"
        else:
            st.error("Invalid login credentials")

# --- Symptom Triage Prompt ---
def get_triage_response(symptoms):
    prompt = f"""
You are a healthcare assistant. A patient has described their symptoms as:
\"\"\"{symptoms}\"\"\"

Give a brief summary of the likely condition and urgency level (low, moderate, high).
Respond in plain language.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=200,
    )
    return response.choices[0].message["content"]

# --- Patient View ---
def patient_dashboard():
    st.title("👨‍⚕️ Patient Dashboard")

    symptoms = st.text_area("Describe your symptoms:")
    if st.button("Analyze"):
        if symptoms.strip() != "":
            with st.spinner("Analyzing symptoms..."):
                result = get_triage_response(symptoms)
            st.subheader("🩺 Triage Result")
            st.success(result)
        else:
            st.warning("Please enter your symptoms.")

    st.markdown("---")
    st.caption("Logged in as Patient | [Logout](#)", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.role = None

# --- Doctor View ---
def doctor_dashboard():
    st.title("🧑‍⚕️ Doctor Dashboard")

    st.markdown("Welcome, Doctor. Future features here:")
    st.markdown("- View patient summaries")
    st.markdown("- Review uploaded EHRs")
    st.markdown("- Monitor patient analytics")

    st.markdown("---")
    st.caption("Logged in as Doctor | [Logout](#)", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.role = None

# --- App Logic ---
def main():
    if st.session_state.role is None:
        login()
    elif st.session_state.role == "patient":
        patient_dashboard()
    elif st.session_state.role == "doctor":
        doctor_dashboard()

if __name__ == "__main__":
    main()
