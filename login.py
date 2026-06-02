import streamlit as st
from database import verify_login

def login_page():

    st.title("🔐 Admin Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = verify_login(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )