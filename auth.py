import streamlit as st
from db_connection import execute_query, call_procedure
from utils import hash_password, verify_password # These functions are now the simplified ones

def show_auth_page():
    st.markdown("<h1 style='text-align: center;'>Smart Study Planner & Wellness Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6C757D;'>Your integrated solution for academic success and personal wellness.</p>", unsafe_allow_html=True)
    left_space, content_col, right_space = st.columns([1, 1.5, 1])

    with content_col:
        with st.container(border=True):
            login_tab, register_tab = st.tabs(["Login", "Create an Account"])
            with login_tab:
                st.subheader("Login to Your Account")
                with st.form("login_form", border=False):
                    email = st.text_input("Email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    if st.form_submit_button("Login", use_container_width=True): handle_login(email, password)
            with register_tab:
                st.subheader("Register as a New User")
                semesters_df = execute_query("SELECT SemesterID, SemesterName FROM Semesters ORDER BY StartDate DESC", fetch="all")
                if semesters_df is None: st.error("Could not load semester data."); return
                with st.form("register_form", border=False):
                    name = st.text_input("Full Name", placeholder="Vanya Sharma")
                    reg_email = st.text_input("Email Address", placeholder="vanya.sharma@example.com")
                    role = st.selectbox("I am a...", ["Student", "Admin"])
                    semester_id = None
                    if role == 'Student': semester_id = st.selectbox("Select Your Current Semester", options=semesters_df['SemesterID'], format_func=lambda x: semesters_df.loc[semesters_df['SemesterID'] == x, 'SemesterName'].iloc[0])
                    reg_password = st.text_input("Choose a Password", type="password", placeholder="Choose a password")
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                    if st.form_submit_button("Create Account", use_container_width=True):
                        if reg_password != confirm_password: st.error("Passwords do not match.")
                        else: handle_registration(name, reg_email, reg_password, role, semester_id)

def handle_login(email, password):
    if not email or not password: st.error("Email and password cannot be empty."); return
    
    # *** CHANGED: Query now selects 'Password' column instead of 'PasswordHash' ***
    query = "SELECT UserID, Name, Password, Role FROM Users WHERE Email = %s"
    user_data = execute_query(query, (email,), fetch="one")

    if user_data:
        user_id, user_name, stored_password, user_role = user_data
        
        # The verify_password function now just does a simple string comparison
        if verify_password(password, stored_password):
            st.session_state['logged_in'], st.session_state['user_id'], st.session_state['user_name'], st.session_state['user_role'] = True, user_id, user_name, user_role
            st.rerun()
        else:
            st.error("Invalid email or password.")
    else:
        st.error("Invalid email or password.")

def handle_registration(name, email, password, role, semester_id):
    if not name or not email or not password: st.error("Name, email, and password fields are required."); return
    if execute_query("SELECT UserID FROM Users WHERE Email = %s", (email,), fetch="one"): st.error("An account with this email already exists."); return
    
    # The 'hash_password' function now just returns the plain password
    plain_password_to_store = hash_password(password)

    # The stored procedure now accepts the plain password
    args = (name, email, plain_password_to_store, role, semester_id, 0)
    result = call_procedure('sp_RegisterUserWithSemester', args)
    
    if result and result[5] > 0: st.success("Registration successful! You can now log in.")
    else: st.error("Registration failed. Please try again.")