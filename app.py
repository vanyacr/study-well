import streamlit as st
from utils import initialize_session_state, logout, is_admin, is_student
import auth, student_dashboard, courses_page, tasks_page, study_sessions_page, wellness_page, notifications_page, admin_dashboard

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_final_corrected_theme():
    """
    Injects the professional dark theme with the user-provided, robust fix for the sidebar toggle.
    This is the safest and most reliable version.
    """
    st.markdown("""
        <style>
            /* --- Base & Font (Dark Mode) --- */
            html, body, [class*="st-"], [class*="css-"] {
                color: #EAEAEB;
                background-color: #121212;
            }
            .st-emotion-cache-1jicfl2 { background-color: #121212; }

            /* --- Sidebar Styling (Dark Mode) --- */
            [data-testid="stSidebar"] {
                background-color: #1E1E1E;
                border-right: 1px solid #2E2E2E;
            }
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj {
                color: #EAEAEB;
            }
            [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj:hover {
                background-color: #2C2C2C;
                color: #8A3FFC;
            }

            /* --- Main Content Cards (Dark Mode) --- */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: #1E1E1E;
                border-radius: 12px;
                border: 1px solid #2E2E2E;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }
            
            /* --- Button Styling (Dark Mode) --- */
            [data-testid="stButton"] > button {
                border-radius: 8px;
                border: 1px solid #8A3FFC;
                background-color: transparent;
                color: #8A3FFC;
                font-weight: 600;
            }
            [data-testid="stButton"] > button:hover {
                background-color: #8A3FFC;
                color: #FFFFFF;
            }

            /* --- Tab Styling (Dark Mode) --- */
            [data-testid="stTabs"] button { color: #A8A8A8; }
            [data-testid="stTabs"] button[aria-selected="true"] {
                color: #8A3FFC;
                border-bottom: 2px solid #8A3FFC;
            }
            
            /* --- Text Input Styling (Dark Mode) --- */
            [data-testid="stTextInput"] input, [data-testid="stDateInput"] input {
                background-color: #2C2C2C;
                border: 1px solid #3E3E3E;
                color: #EAEAEB;
            }
            
            /* --- Typography (Dark Mode) --- */
            h1, h2, h3 { color: #FFFFFF; }
            .st-emotion-cache-zt5igj { color: #A8A8A8; }

            /* --- !!! FINAL SIDEBAR FIX (USER-PROVIDED SAFER ALTERNATIVE) !!! --- */
            /* Hide "Made with Streamlit" footer only */
            footer { visibility: hidden; }

            /* Hide the 'Deploy' or 'View app in new tab' button icon */
            button[title="View app in new tab"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

initialize_session_state()

def main():
    apply_final_corrected_theme()
    if not st.session_state['logged_in']:
        auth.show_auth_page()
    else:
        student_pages = {"📈 Dashboard": student_dashboard, "📚 Courses": courses_page, "🎯 Tasks": tasks_page, "⏱️ Study Sessions": study_sessions_page, "🧘 Wellness": wellness_page, "🔔 Notifications": notifications_page}
        admin_pages = {"🛠️ Admin Panel": admin_dashboard}
        
        st.sidebar.title(f"✨ Welcome, {st.session_state['user_name']}!")
        st.sidebar.markdown(f"**Role:** {st.session_state['user_role']}")
        st.sidebar.markdown("---")
        
        if is_student():
            page_selection = st.sidebar.radio("Navigation", list(student_pages.keys()), label_visibility="collapsed")
            student_pages[page_selection].show()
        if is_admin():
            st.sidebar.markdown("---"); st.sidebar.header("Admin Tools")
            admin_page_selection = st.sidebar.radio("Management", list(admin_pages.keys()), label_visibility="collapsed")
            admin_pages[admin_page_selection].show()

        st.sidebar.markdown("---")
        if st.sidebar.button("Logout", use_container_width=True): logout()

if __name__ == "__main__":
    main()