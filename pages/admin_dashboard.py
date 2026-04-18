import streamlit as st
from utils.data_manager import add_user, load_users, delete_user


def show_admin(menu):

    if menu == "Dashboard":

        st.title("🛡️ Admin Dashboard")

        st.markdown("### 👥 User Management")

        col1, col2 = st.columns(2)

        # ➕ ADD USER
        with col1:
            st.markdown("#### ➕ Add New User")

            username = st.text_input("Username")
            password = st.text_input("Password")

            if st.button("Add User"):
                if username and password:
                    add_user(username, password)
                    st.success("User Added Successfully ✅")
                else:
                    st.error("Please fill all fields")

        # 👀 VIEW USERS
        with col2:
            st.markdown("#### 👀 Existing Users")

            users = load_users()

            for u in users:
                if u["role"] != "admin":
                    c1, c2 = st.columns([3,1])

                    c1.write(f"👤 {u['username']}")

                    if c2.button("❌ Delete", key=u["username"]):
                        delete_user(u["username"])
                        st.warning("User Deleted")
                        st.rerun()

