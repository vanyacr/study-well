import streamlit as st
from db_connection import execute_query

def show():
    st.title("⏱️ Study Sessions Log"); user_id = st.session_state['user_id']
    tab1, tab2 = st.tabs(["➕ Log New Session", "🗓️ View Past Sessions"])
    
    with tab1:
        with st.container(border=True):
            st.subheader("Log a New Study Session")
            courses_df = execute_query("SELECT CourseID, CourseName FROM Courses WHERE UserID = %s", (user_id,), fetch="all")
            tasks_df = execute_query("SELECT TaskID, TaskName FROM Tasks t JOIN Courses c ON t.CourseID = c.CourseID WHERE c.UserID = %s AND t.Status != 'Completed'", (user_id,), fetch="all")
            
            if courses_df.empty:
                st.warning("Please add a course first before logging a session.")
            else:
                with st.form("log_session_form", border=False):
                    course_id = st.selectbox("Select Course", options=courses_df['CourseID'], format_func=lambda x: courses_df.loc[courses_df['CourseID'] == x, 'CourseName'].iloc[0])
                    task_id = st.selectbox("Related Task (optional)", options=[None] + tasks_df['TaskID'].tolist(), format_func=lambda x: "None" if x is None else tasks_df.loc[tasks_df['TaskID'] == x, 'TaskName'].iloc[0])
                    session_date = st.date_input("Session Date")
                    duration = st.number_input("Duration (in minutes)", min_value=15, step=15)
                    
                    if st.form_submit_button("Log Session", use_container_width=True):
                        execute_query("INSERT INTO StudySessions (UserID, CourseID, TaskID, SessionDate, DurationMinutes) VALUES (%s, %s, %s, %s, %s)", (user_id, course_id, task_id, session_date, duration))
                        # --- MESSAGE CHANGE: Using st.toast for a persistent message ---
                        st.toast(f"Logged a {duration}-minute session! Keep it up! 💪", icon="✅")
                        st.rerun() # This clears the form fields by re-rendering the page
    
    with tab2:
        st.header("Your Study History")
        
        # --- !!! SORTING FIX: Added ORDER BY SessionDate DESC and SessionID DESC !!! ---
        # This ensures the newest entries always appear at the top.
        sessions_query = """
            SELECT s.SessionID, c.CourseName, COALESCE(t.TaskName, 'General Study') AS TaskName, s.SessionDate, s.DurationMinutes
            FROM StudySessions s
            JOIN Courses c ON s.CourseID = c.CourseID
            LEFT JOIN Tasks t ON s.TaskID = t.TaskID
            WHERE s.UserID = %s
            ORDER BY s.SessionDate DESC, s.SessionID DESC
        """
        sessions_df = execute_query(sessions_query, (user_id,), fetch="all")
        
        st.dataframe(sessions_df, use_container_width=True)