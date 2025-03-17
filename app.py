import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, db
import requests

# Firebase Configuration
firebase_url = "https://taskpyapp-default-rtdb.firebaseio.com/"
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": firebase_url})

# Streamlit UI
st.set_page_config(page_title="Tasking App", page_icon="🔥", layout="wide")

st.title("🔥 Tasking Web App - Earn by Tasks")
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Tasks", "Referrals", "Withdraw", "Leaderboard"])

# Dummy User Session
if "user" not in st.session_state:
    st.session_state["user"] = None

# Login/Signup System
if st.session_state["user"] is None:
    login_option = st.radio("Login / Signup", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if login_option == "Signup":
        if st.button("Sign Up"):
            try:
                user = auth.create_user(email=email, password=password)
                db.reference(f"users/{user.uid}").set({"coins": 0, "referrals": 0})
                st.session_state["user"] = user.uid
                st.success("Signup Successful! You can now Login.")
            except:
                st.error("Signup Failed. Try a different email.")

    elif login_option == "Login":
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state["user"] = user.uid
                st.success("Login Successful!")
            except:
                st.error("Login Failed. Check your credentials.")

# Home Page
elif page == "Home":
    st.subheader("Welcome! Complete Tasks & Earn Coins")
    st.image("dashboard.png", use_column_width=True)

# Tasks Page
elif page == "Tasks":
    st.subheader("Complete Tasks & Earn")
    task_options = ["Watch Ads (5 Coins)", "Install App (5 Coins)", "Survey (5 Coins)", "Gaming Task (5 Coins)"]
    task = st.selectbox("Select Task", task_options)
    if st.button("Complete Task"):
        user_ref = db.reference(f"users/{st.session_state['user']}")
        user_data = user_ref.get()
        new_coins = user_data["coins"] + 5
        user_ref.update({"coins": new_coins})
        st.success(f"Task Completed! You earned 5 coins. Total: {new_coins}")

# Referral Page
elif page == "Referrals":
    st.subheader("Invite Friends & Earn More!")
    st.write("Share your referral link to earn more coins.")
    st.code(f"https://taskpyapp.web.app/referral/{st.session_state['user']}")

# Withdraw Page
elif page == "Withdraw":
    user_data = db.reference(f"users/{st.session_state['user']}").get()
    if user_data["coins"] >= 15000 and user_data["referrals"] >= 10:
        withdraw_method = st.selectbox("Select Withdrawal Method", ["JazzCash", "EasyPaisa", "Payoneer", "PayPal"])
        number = st.text_input(f"Enter {withdraw_method} Number")
        if st.button("Request Withdrawal"):
            st.success("Withdrawal Request Sent! It will be processed soon.")
    else:
        st.warning("You need at least 15,000 coins & 10 referrals to withdraw.")

# Leaderboard Page
elif page == "Leaderboard":
    st.subheader("Top Earners")
    users_data = db.reference("users").get()
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]["coins"], reverse=True)
    for rank, (uid, data) in enumerate(sorted_users[:10], start=1):
        st.write(f"🥇 {rank}. {uid} - {data['coins']} Coins")

# Footer
st.sidebar.markdown("Developed by **Tooncraft Studio** 🇵🇰")
