import streamlit as st
# bcrypt is no longer needed in this file
# import bcrypt

# *** CHANGED: This function no longer hashes, it just returns the password as-is. ***
def hash_password(password):
    """
    (DEMO-ONLY) This function now returns the password in plain text.
    In a real app, this MUST be a hashing function.
    """
    return password

# *** CHANGED: This function now does a simple string comparison. ***
def verify_password(plain_password, stored_password):
    """
    (DEMO-ONLY) This function compares the plain text password to the one from the DB.
    """
    return plain_password == stored_password

# (The rest of the file is the same)
def initialize_session_state():
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state: st.session_state['user_id'] = None
    if 'user_name' not in st.session_state: st.session_state['user_name'] = None
    if 'user_role' not in st.session_state: st.session_state['user_role'] = None

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['user_name'] = None
    st.session_state['user_role'] = None
    st.success("You have been logged out successfully.")
    st.rerun()

def is_admin():
    return st.session_state.get('user_role') == 'Admin'

def is_student():
    return st.session_state.get('user_role') == 'Student'