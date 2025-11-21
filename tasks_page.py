import streamlit as st
from db_connection import execute_query, call_procedure, call_function

def show():
    st.title("🎯 My Tasks")
    st.markdown("Manage your academic to-do list, complete with dependencies.")
    user_id = st.session_state['user_id']

    with st.expander("➕ Add a New Task"):
        with st.form("add_task_form"):
            courses_df = execute_query("SELECT CourseID, CourseName FROM Courses WHERE UserID = %s", (user_id,), fetch="all")
            if courses_df.empty:
                st.warning("Please add a course first before adding tasks.")
            else:
                task_name = st.text_input("Task Name")
                due_date = st.date_input("Due Date")
                course_id = st.selectbox("Select Course", options=courses_df['CourseID'], format_func=lambda x: courses_df.loc[courses_df['CourseID'] == x, 'CourseName'].iloc[0])
                all_tasks_df = execute_query("SELECT TaskID, TaskName FROM Tasks t JOIN Courses c ON t.CourseID = c.CourseID WHERE c.UserID = %s", (user_id,), fetch="all")
                prerequisite_id = st.selectbox("Prerequisite Task (optional)", options=[None] + all_tasks_df['TaskID'].tolist(), format_func=lambda x: "None" if x is None else all_tasks_df.loc[all_tasks_df['TaskID'] == x, 'TaskName'].iloc[0])

                if st.form_submit_button("Add Task"):
                    if task_name:
                        execute_query("INSERT INTO Tasks (CourseID, TaskName, DueDate, Status, PrerequisiteTaskID) VALUES (%s, %s, %s, 'Pending', %s)", (course_id, task_name, due_date, prerequisite_id))
                        # --- MESSAGE CHANGE: Using st.toast for a persistent message ---
                        st.toast(f"Task '{task_name}' added!", icon="👍")
                        st.rerun() # Clears the form
                    else:
                        st.toast("Task name cannot be empty.", icon="❗")

    st.markdown("---")
    st.header("📋 Your Task List")
    
    tasks_df = execute_query("SELECT t.TaskID, c.CourseName, t.TaskName, t.DueDate, t.Status FROM Tasks t JOIN Courses c ON t.CourseID = c.CourseID WHERE c.UserID = %s ORDER BY t.DueDate", (user_id,), fetch="all")
    
    if tasks_df is not None and not tasks_df.empty:
        for _, row in tasks_df.iterrows():
            is_unlocked = call_function('fn_IsTaskUnlocked', (row['TaskID'],))
            status_icon = "✅" if row['Status'] == 'Completed' else ("⏳" if is_unlocked else "🔒")

            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{status_icon} {row['TaskName']}**")
                    st.caption(f"Course: {row['CourseName']} | Due: {row['DueDate'].strftime('%b %d, %Y')}")
                
                with col2:
                    if row['Status'] != 'Completed' and is_unlocked:
                        if st.button("Mark Complete", key=f"complete_{row['TaskID']}", use_container_width=True):
                            call_procedure('sp_CompleteTask', (user_id, row['TaskID']))
                            # --- MESSAGE CHANGE: Using st.toast for a persistent message ---
                            st.toast(f"Great job on completing '{row['TaskName']}'! 🎉")
                            st.rerun() # Refreshes the task list
    else:
        st.info("Your task list is empty. Add a new task above to get started!")