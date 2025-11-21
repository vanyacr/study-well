import streamlit as st
from db_connection import execute_query

def show():
    st.title("📚 My Courses")
    user_id = st.session_state['user_id']
    st.header("Your Enrolled Courses")
    courses_df = execute_query("SELECT CourseID, CourseName, CourseCode FROM Courses WHERE UserID = %s ORDER BY CourseName", (user_id,), fetch="all")
    st.dataframe(courses_df, use_container_width=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("➕ Add a New Course")
            with st.form("add_course_form", border=False):
                course_name = st.text_input("Course Name", placeholder="e.g., Advanced Python")
                course_code = st.text_input("Course Code", placeholder="e.g., CS-502")
                if st.form_submit_button("Add Course", use_container_width=True):
                    if course_name:
                        execute_query("INSERT INTO Courses (UserID, CourseName, CourseCode) VALUES (%s, %s, %s)", (user_id, course_name, course_code))
                        # --- MESSAGE CHANGE: Using st.toast for a persistent message ---
                        st.toast(f"Course '{course_name}' added successfully!", icon="🎉")
                        st.rerun() # Clears the form
                    else:
                        st.toast("Course name cannot be empty.", icon="❗")

    with col2:
        with st.container(border=True):
            st.subheader("🗑️ Delete a Course")
            if not courses_df.empty:
                course_to_delete = st.selectbox("Select a course to delete", options=courses_df['CourseID'], format_func=lambda x: f"{courses_df.loc[courses_df['CourseID'] == x, 'CourseName'].iloc[0]}")
                if st.button("Delete Selected Course", use_container_width=True):
                    execute_query("DELETE FROM Courses WHERE CourseID = %s", (course_to_delete,))
                    # --- MESSAGE CHANGE: Using st.toast for a persistent message ---
                    st.toast("Course has been deleted.", icon="🗑️")
                    st.rerun() # Refreshes the list
            else:
                st.info("No courses to delete.")