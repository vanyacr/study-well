import streamlit as st
from db_connection import execute_query


def show():
    """Displays the admin dashboard for managing campus resources."""
    st.title("Admin Dashboard")
    st.subheader("Manage Campus Resources")
    
    # --- Display Resources ---
    resources_df = execute_query("SELECT ResourceID, ResourceName, ResourceType, ContactInfo FROM CampusResources", fetch="all")
    if resources_df is None:
        st.error("Error fetching resources.")
        return
    st.dataframe(resources_df, use_container_width=True)

    st.markdown("---")

    # --- Add/Edit/Delete Forms ---
    tab1, tab2, tab3 = st.tabs(["Add Resource", "Edit Resource", "Delete Resource"])

    with tab1:
        with st.form("add_resource_form"):
            name = st.text_input("Resource Name")
            res_type = st.selectbox("Resource Type", ["Academic", "Wellness", "Financial", "Career"])
            contact = st.text_input("Contact Info (Email, Phone, or URL)")
            submitted = st.form_submit_button("Add Resource")
            
            if submitted:
                query = "INSERT INTO CampusResources (ResourceName, ResourceType, ContactInfo) VALUES (%s, %s, %s)"
                execute_query(query, (name, res_type, contact))
                st.success("Resource added successfully!")
                st.rerun()
                
    with tab2:
        if resources_df is not None and not resources_df.empty:
            resource_to_edit_id = st.selectbox(
                "Select Resource to Edit",
                options=resources_df['ResourceID'],
                format_func=lambda x: resources_df.loc[resources_df['ResourceID'] == x, 'ResourceName'].iloc[0]
            )
            selected_resource = resources_df[resources_df['ResourceID'] == resource_to_edit_id].iloc[0]

            with st.form("edit_resource_form"):
                new_name = st.text_input("Resource Name", value=selected_resource['ResourceName'])
                new_type = st.selectbox("Resource Type", ["Academic", "Wellness", "Financial", "Career"], index=["Academic", "Wellness", "Financial", "Career"].index(selected_resource['ResourceType']))
                new_contact = st.text_input("Contact Info", value=selected_resource['ContactInfo'])
                
                submitted = st.form_submit_button("Update Resource")
                if submitted:
                    query = "UPDATE CampusResources SET ResourceName = %s, ResourceType = %s, ContactInfo = %s WHERE ResourceID = %s"
                    execute_query(query, (new_name, new_type, new_contact, resource_to_edit_id))
                    st.success("Resource updated successfully!")
                    st.rerun()
        else:
            st.info("No resources to edit.")
            
    with tab3:
        if resources_df is not None and not resources_df.empty:
            resource_to_delete_id = st.selectbox(
                "Select Resource to Delete",
                options=resources_df['ResourceID'],
                format_func=lambda x: resources_df.loc[resources_df['ResourceID'] == x, 'ResourceName'].iloc[0],
                key="delete_select"
            )
            if st.button("Delete Selected Resource", type="primary"):
                execute_query("DELETE FROM CampusResources WHERE ResourceID = %s", (resource_to_delete_id,))
                st.warning("Resource deleted.")
                st.rerun()
        else:
            st.info("No resources to delete.")
