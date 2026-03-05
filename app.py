import streamlit as st
import numpy as np
import folium
import matplotlib.pyplot as plt
from datetime import date
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from database import *

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Suraksha-AI",
    page_icon="💜",
    layout="wide"
)

create_tables()

# ---------------- THEME ---------------- #

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f3e8ff, #f8f0ff);
}
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #111111 !important;
}
input, textarea {
    background-color: white !important;
    color: black !important;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c2f3a, #1e1f29);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
.stButton>button {
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: bold;
    background: linear-gradient(135deg, #ff4b8b, #8f44fd);
    color: white !important;
    border: none;
}
div[data-baseweb="popover"] {
    background-color: #1e1f29 !important;
}
div[data-baseweb="calendar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN / SIGNUP ---------------- #

if not st.session_state.logged_in:

    st.image("logo.png", width=120)
    st.title("🛡 Suraksha-AI")

    option = st.radio("Select Option", ["Sign In", "Sign Up"], horizontal=True)

    if option == "Sign Up":

        name = st.text_input("Full Name")

        dob = st.date_input(
            "Date of Birth",
            min_value=date(1960,1,1),
            max_value=date.today(),
            value=date(2000,1,1)
        )

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        mobile = st.text_input("Mobile Number")

        if st.button("Create Account"):
            if add_user(name, str(dob), email, password, mobile):
                st.success("Account Created Successfully 💜")
            else:
                st.error("User already exists")

    else:

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = validate_login(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------------- MAIN APP ---------------- #

else:

    user = get_user(st.session_state.email)
    name = user[1]
    email = user[3]
    mobile = user[5]

    # SIDEBAR
    with st.sidebar:
        st.image("logo.png", width=80)

        page = st.radio(
            "Go to",
            [
                "👋 Welcome",
                "🏠 Home",
                "🔍 Safety Checker",
                "📍 Hotspot Map",
                "📝 Raise Complaint",
                "📂 Complaint History",
                "📊 Complaint Analysis",
                "📞 Emergency Contacts",
                "🚨 Emergency SOS",
                "👤 Profile"
            ]
        )

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # ---------------- WELCOME ---------------- #

    if page == "👋 Welcome":

        st.title(f"Hello, {name} 💜")

        st.info(
            "Your safety is our priority.\n"
            "We are always here with you, 24/7.\n"
            "Stay confident, stay fearless."
        )

    # ---------------- HOME ---------------- #

    elif page == "🏠 Home":

        st.title("🏠 Safety Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Safety Score", "85")

        with col2:
            st.metric("Contacts", len(get_contacts(email)))

        with col3:
            st.metric("Risk Level", "Low")

        st.markdown("## Quick Actions")

        qa1, qa2, qa3 = st.columns(3)

        with qa1:
            if st.button("🚨 Emergency SOS"):
                st.session_state["redirect"] = "🚨 Emergency SOS"

        with qa2:
            if st.button("🔍 Safety Checker"):
                st.session_state["redirect"] = "🔍 Safety Checker"

        with qa3:
            if st.button("📍 Hotspot Map"):
                st.session_state["redirect"] = "📍 Hotspot Map"

        qa4, qa5, qa6 = st.columns(3)

        with qa4:
            if st.button("📝 Complaint"):
                st.session_state["redirect"] = "📝 Raise Complaint"

        with qa5:
            if st.button("📞 Contacts"):
                st.session_state["redirect"] = "📞 Emergency Contacts"

        with qa6:
            if st.button("📊 Analysis"):
                st.session_state["redirect"] = "📊 Complaint Analysis"

        st.markdown("### 💜 Remember, you are never alone. Stay safe and confident!")

    # ---------------- SAFETY CHECKER ---------------- #

    elif page == "🔍 Safety Checker":

        st.header("Safety Checker")

        location = st.text_input("Enter Location")

        if st.button("Predict Risk"):

            if location.strip() == "":
                st.error("Please enter location.")
            else:
                score = np.random.randint(0, 101)

                if score >= 70:
                    st.success("🟢 Risk Level: Low")
                elif score >= 40:
                    st.warning("🟡 Risk Level: Medium")
                else:
                    st.error("🔴 Risk Level: High")

                st.info(f"Safety Score: {score}/100")

    # ---------------- HOTSPOT MAP ---------------- #

    elif page == "📍 Hotspot Map":

        st.header("📍 Hotspot Map")

        location_data = streamlit_geolocation()

        if location_data and location_data["latitude"]:

            lat = location_data["latitude"]
            lon = location_data["longitude"]

            st.success(f"Your Location: {lat}, {lon}")

            m = folium.Map(location=[lat, lon], zoom_start=14)

            folium.Marker(
                [lat, lon],
                tooltip="You are here",
                icon=folium.Icon(color="purple")
            ).add_to(m)

            st_folium(m, width=700, height=450)

        else:
            st.info("Please allow location access.")

    # ---------------- RAISE COMPLAINT ---------------- #

    elif page == "📝 Raise Complaint":

        st.header("Raise a Complaint")

        category = st.selectbox(
            "Select Category",
            ["Rape", "Kidnap & Abduction", "Domestic Violence",
             "Women Trafficking", "Harassment"]
        )

        subject = st.text_input("Subject")
        description = st.text_area("Describe Incident")
        location = st.text_input("Location")

        if st.button("Submit Complaint"):
            add_complaint(email, category, subject, description, location)
            st.success("Complaint Submitted Successfully")

    # ---------------- COMPLAINT HISTORY ---------------- #

    elif page == "📂 Complaint History":

        st.header("Your Complaints")

        complaints = get_user_complaints(email)

        if complaints:
            for c in complaints:
                st.write(f"📌 {c[1]} - {c[2]} ({c[3]})")
        else:
            st.info("No complaints found.")

    # ---------------- COMPLAINT ANALYSIS ---------------- #

    elif page == "📊 Complaint Analysis":

        st.header("Complaint Analysis")

        data = get_complaint_counts()

        if data:
            categories = [row[0] for row in data]
            counts = [row[1] for row in data]

            fig, ax = plt.subplots()
            ax.bar(categories, counts)
            ax.set_xlabel("Category")
            ax.set_ylabel("Count")
            st.pyplot(fig)
        else:
            st.info("No complaint data available.")

    # ---------------- CONTACTS ---------------- #

    elif page == "📞 Emergency Contacts":

        st.header("Emergency Contacts")

        cname = st.text_input("Contact Name")
        cnum = st.text_input("Contact Number")

        if st.button("Save Contact"):
            add_contact(email, cname, cnum)
            st.success("Contact Saved")

        contacts = get_contacts(email)
        for c in contacts:
            st.write(f"{c[0]} - {c[1]}")

    # ---------------- SOS ---------------- #

    elif page == "🚨 Emergency SOS":

        st.header("Emergency SOS")

        if st.button("TRIGGER SOS"):
            st.error("🚨 SOS Triggered Successfully!")

    # ---------------- PROFILE ---------------- #

    elif page == "👤 Profile":

        st.header("Your Profile")

        st.text_input("Email", value=email, disabled=True)

        new_name = st.text_input("Name", value=name)
        new_mobile = st.text_input("Mobile", value=mobile)

        if st.button("Update Profile"):
            update_profile(email, new_name, new_mobile)
            st.success("Profile Updated Successfully 💜")