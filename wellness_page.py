import streamlit as st
from db_connection import execute_query

def show():
    st.title("🧘 Wellness Tracker")
    st.markdown("Log your daily wellness metrics to keep track of your mental health.")
    user_id = st.session_state['user_id']
    
    col1, col2 = st.columns([1, 1])

    with col1:
        with st.container(border=True):
            st.subheader("📝 Log Today's Wellness")
            with st.form("wellness_log_form"):
                log_date = st.date_input("Date")
                stress_level = st.slider("Stress Level (1-Low, 10-High)", 1, 10, 5)
                mood = st.selectbox("Overall Mood", ["😊 Happy", "🙂 Neutral", "😟 Sad", "😠 Angry", "😩 Stressed"])
                sleep_hours = st.number_input("Hours of Sleep", min_value=0.0, max_value=24.0, step=0.5, value=7.5)
                
                if st.form_submit_button("Log My Wellness", use_container_width=True):
                    result = execute_query("INSERT INTO WellnessLogs (UserID, LogDate, StressLevel, Mood, SleepHours) VALUES (%s, %s, %s, %s, %s)", (user_id, log_date, stress_level, mood.split(" ")[1], sleep_hours))
                    if result is not None:
                        st.success("Your wellness data has been logged!")
                        notifications_df = execute_query("SELECT Message FROM Notifications WHERE UserID = %s AND DATE(CreatedAt) = CURDATE()", (user_id,), fetch="all")
                        if not notifications_df.empty:
                            for _, row in notifications_df.iterrows():
                                st.warning(f"**System Alert:** {row['Message']}")
                    else:
                        st.error("Failed to log wellness data. You may have already logged for this date.")

    with col2:
        with st.container(border=True):
            st.subheader("🗓️ Recent Wellness Logs")
            recent_logs_df = execute_query("SELECT LogDate, StressLevel, Mood, SleepHours FROM WellnessLogs WHERE UserID = %s ORDER BY LogDate DESC LIMIT 7", (user_id,), fetch="all")
            st.dataframe(recent_logs_df, use_container_width=True)