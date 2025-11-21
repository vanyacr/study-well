import streamlit as st
from db_connection import execute_query, call_function
import plotly.express as px

def show():
    # Use the name from the session state for a personalized welcome
    user_name = st.session_state.get('user_name', 'Student').split(" ")[0]
    st.title(f"📊 Welcome to Your Dashboard, {user_name}!")
    st.markdown("Here's your academic and wellness summary at a glance.")
    user_id = st.session_state['user_id']

    # --- Top Metrics in a Styled Container ---
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_stress = call_function('fn_GetAverageStress', (user_id, 7))
            st.metric(label="Weekly Stress Average", value=f"{avg_stress:.1f}/10" if avg_stress is not None else "N/A")
        with col2:
            tasks_completed = execute_query("SELECT count(*) FROM Tasks t JOIN Courses c ON t.CourseID = c.CourseID WHERE c.UserID = %s AND t.Status = 'Completed'", (user_id,), fetch='one')
            st.metric("Total Tasks Completed", value=tasks_completed[0] if tasks_completed else 0)
        with col3:
            study_hours = execute_query("SELECT SUM(DurationMinutes)/60 FROM StudySessions WHERE UserID = %s AND SessionDate >= CURDATE() - INTERVAL 7 DAY", (user_id,), fetch='one')
            st.metric("Study Hours This Week", value=f"{study_hours[0]:.1f}" if study_hours and study_hours[0] else "0")

    # --- Charts in separate columns/cards ---
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("🧠 Stress Trend")
            stress_df = execute_query("SELECT LogDate, StressLevel FROM WellnessLogs WHERE UserID = %s AND LogDate >= CURDATE() - INTERVAL 30 DAY ORDER BY LogDate", (user_id,), fetch="all")
            
            # Robust check for DataFrame
            if stress_df is not None and not stress_df.empty:
                fig_stress = px.area(stress_df, x='LogDate', y='StressLevel', labels={'LogDate': 'Date', 'StressLevel': 'Level'}, height=300, template="plotly_dark")
                fig_stress.update_layout(margin=dict(l=20, r=20, t=40, b=20), yaxis_title=None, xaxis_title=None)
                st.plotly_chart(fig_stress, use_container_width=True)
            else:
                st.info("Log your wellness data to see your stress trend here.")

    with col2:
        with st.container(border=True):
            st.subheader("📚 Hours by Course")
            
            # --- !!! SQL QUERY FIX !!! ---
            # Added the 'INTERVAL' keyword before '7 DAY'
            study_query = """
                SELECT c.CourseName, SUM(s.DurationMinutes)/60.0 AS Hours 
                FROM StudySessions s 
                JOIN Courses c ON s.CourseID=c.CourseID 
                WHERE s.UserID=%s AND s.SessionDate >= CURDATE() - INTERVAL 7 DAY 
                GROUP BY c.CourseName
            """
            study_df = execute_query(study_query, (user_id,), fetch="all")

            # --- !!! PYTHON ERROR FIX !!! ---
            # Added 'study_df is not None' to prevent crash if query fails
            if study_df is not None and not study_df.empty:
                fig_study = px.bar(study_df, x='Hours', y='CourseName', orientation='h', labels={'CourseName': '', 'Hours': 'Hours Studied'}, height=300, template="plotly_dark")
                fig_study.update_layout(margin=dict(l=20, r=20, t=40, b=20), yaxis_title=None)
                st.plotly_chart(fig_study, use_container_width=True)
            else:
                st.info("Log study sessions to see your weekly effort here.")