
import streamlit as st
from streamlit_option_menu import option_menu

# Initialize Session State
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# Login Page
def login_page():
    st.title("EduTutor AI Login")
    login_method = st.radio("Login Method", ["Manual Login", "Google Login"])

    if login_method == "Manual Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Select Role", ["Student", "Educator"])
        if st.button("Login"):
            if username and password:
                st.session_state.is_logged_in = True
                st.session_state.user_role = role
                st.success(f"Welcome {role}: {username}")
                st.experimental_rerun()
            else:
                st.error("Please enter username and password")
    elif login_method == "Google Login":
        st.info("🔒 Google Login integration placeholder. Needs OAuth setup.")

# Logout Button
def logout_button():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.is_logged_in = False
        st.session_state.user_role = None
        st.experimental_rerun()

# Student Panel
def student_panel():
    st.sidebar.success("Logged in as Student")
    logout_button()
    selected = option_menu(
        menu_title="Student Panel",
        options=["Dashboard", "Take Quiz", "Quiz History"],
        icons=["speedometer", "pencil", "clock-history"],
        menu_icon="cast",
        default_index=0
    )
    if selected == "Dashboard":
        st.title("📊 Student Dashboard")
        st.info("Welcome to your personalized dashboard.")
    elif selected == "Take Quiz":
        st.title("📝 Take a Quiz")
        st.info("Quiz functionality goes here.")
    elif selected == "Quiz History":
        st.title("📚 Quiz History")
        st.info("Your previous quiz records will appear here.")

# Educator Panel
def educator_panel():
    st.sidebar.success("Logged in as Educator")
    logout_button()
    selected = option_menu(
        menu_title="Educator Panel",
        options=["Dashboard"],
        icons=["bar-chart"],
        menu_icon="cast",
        default_index=0
    )
    if selected == "Dashboard":
        st.title("📈 Educator Dashboard - Student Analytics")
        st.info("View all student analytics here.")

# Main App
def main():
    st.set_page_config(page_title="EduTutor AI", layout="wide")

    if not st.session_state.is_logged_in:
        login_page()
    else:
        if st.session_state.user_role == "Student":
            student_panel()
        elif st.session_state.user_role == "Educator":
            educator_panel()
        else:
            st.error("Unknown role. Please log in again.")
            st.session_state.is_logged_in = False
            st.session_state.user_role = None
            st.experimental_rerun()

# Entry Point
if __name__ == "__main__":
    main()
