import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hospital Queue System", layout="wide")
st.title("🏥 Hospital Queue Management System")

# Fetch active doctor list from backend API
try:
    doctors_response = requests.get(f"{API_URL}/doctors").json()
    doctors_list = doctors_response.get("doctors", [])
except Exception:
    st.error("Cannot connect to backend API. Please make sure FastAPI is running on http://127.0.0.1:8000")
    st.stop()

# Sidebar Role Switcher
role = st.sidebar.radio("Select Interface Role:", ["Receptionist", "Doctor Portal"])

# ---------------------------------------------------------
# RECEPTIONIST INTERFACE
# ---------------------------------------------------------
if role == "Receptionist":
    st.header("📋 Receptionist Desk - Check-in Patient")

    with st.form("checkin_form", clear_on_submit=True):
        patient_name = st.text_input("Patient Full Name:")
        selected_doctor = st.selectbox("Assign Doctor:", doctors_list)
        submit_button = st.form_submit_button("Add Patient to Queue")

        if submit_button:
            if patient_name.strip() == "":
                st.warning("Please enter a valid patient name.")
            else:
                payload = {"name": patient_name, "doctor_name": selected_doctor}
                res = requests.post(f"{API_URL}/patients/enqueue", json=payload)
                if res.status_code == 200:
                    st.success(f"Added **{patient_name}** to {selected_doctor}'s queue!")
                else:
                    st.error("Error adding patient to queue.")

    st.markdown("---")
    st.subheader("Current Live Queues")
    cols = st.columns(len(doctors_list))

    for idx, doc in enumerate(doctors_list):
        with cols[idx]:
            st.write(f"**{doc}**")
            q_res = requests.get(f"{API_URL}/queues/{doc}").json()
            queue_data = q_res.get("queue", [])
            
            waiting_count = len([p for p in queue_data if p['status'] == 'waiting'])
            in_consult = [p['name'] for p in queue_data if p['status'] == 'in_consultation']
            
            st.metric("In Line", f"{waiting_count} waiting")
            if in_consult:
                st.info(f"Currently Consulting: **{in_consult[0]}**")
            else:
                st.caption("Status: Idle")

# ---------------------------------------------------------
# DOCTOR PORTAL INTERFACE
# ---------------------------------------------------------
elif role == "Doctor Portal":
    st.header("🩺 Doctor Portal - Patient Consultation Flow")

    doctor = st.selectbox("Select Your Profile:", doctors_list)

    if doctor:
        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button("🔔 Call Next Patient", type="primary", use_container_width=True):
                next_res = requests.post(f"{API_URL}/queues/{doctor}/next").json()
                st.toast(next_res.get("message", "Queue updated."))

        # Display Queue Status
        q_res = requests.get(f"{API_URL}/queues/{doctor}").json()
        queue_data = q_res.get("queue", [])

        current_patient = next((p for p in queue_data if p["status"] == "in_consultation"), None)
        waiting_patients = [p for p in queue_data if p["status"] == "waiting"]
        completed_patients = [p for p in queue_data if p["status"] == "completed"]

        with col2:
            st.subheader("Active Consultation")
            if current_patient:
                st.success(f"**Patient ID #{current_patient['patient_id']}:** {current_patient['name']}")
            else:
                st.warning("No active consultation right now. Click 'Call Next Patient' when ready.")

        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Waiting Room Queue", "Completed Consultations"])
        
        with tab1:
            if waiting_patients:
                for idx, p in enumerate(waiting_patients, start=1):
                    st.write(f"**Position #{idx}** — ID: #{p['patient_id']} | Name: **{p['name']}**")
            else:
                st.write("No patients currently waiting in queue.")

        with tab2:
            if completed_patients:
                for p in completed_patients:
                    st.write(f"✅ ID: #{p['patient_id']} | Name: **{p['name']}**")
            else:
                st.write("No completed consultations yet today.")