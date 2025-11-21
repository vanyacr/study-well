import streamlit as st
from db_connection import execute_query


def show():
    """Displays the page for viewing notifications."""
    st.title("Notifications")
    st.write("All system-generated alerts and notifications appear here.")
    user_id = st.session_state['user_id']
    
    # Fetch notifications
    notifications_df = execute_query(
        "SELECT NotificationID, Message, CreatedAt FROM Notifications WHERE UserID = %s ORDER BY CreatedAt DESC",
        (user_id,),
        fetch="all"
    )

    if notifications_df is not None and not notifications_df.empty:
        # Action buttons
        col1, col2 = st.columns(2)
        with col2:
            if st.button("Clear All Notifications", type="primary"):
                execute_query("DELETE FROM Notifications WHERE UserID = %s", (user_id,))
                st.success("All notifications have been cleared.")
                st.rerun()

        # Display notifications
        for index, row in notifications_df.iterrows():
            # st.container(border=True) is not a streamlit API param; show container with simple layout
            with st.container():
                c1, c2 = st.columns([4, 1])
                try:
                    ts = row['CreatedAt']
                    formatted = ts.strftime('%Y-%m-%d %H:%M') if hasattr(ts, 'strftime') else str(ts)
                except Exception:
                    formatted = str(row['CreatedAt'])
                c1.write(f"**{row['Message']}**")
                c1.caption(f"Received on: {formatted}")
                if c2.button("Delete", key=f"del_{row['NotificationID']}"):
                    execute_query("DELETE FROM Notifications WHERE NotificationID = %s", (row['NotificationID'],))
                    st.rerun()
    else:
        st.info("You have no notifications.")
