import streamlit as st
from utils.data_manager import load_users

st.set_page_config(page_title="Health Analyzer", layout="wide")

# 🎨 GLOBAL STYLE
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fb;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        border-radius: 12px;
        height: 45px;
        font-weight: 600;
        background-color: #4F46E5;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338CA;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🩺 Health Analyzer")

# Session
if "user" not in st.session_state:
    st.session_state.user = None


# 🔐 LOGIN
def login():
    st.image("assets/img.png", use_container_width=True)

    st.markdown("<h2 style='text-align:center;'>Welcome to Health Analyzer</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            users = load_users()

            for u in users:
                if u["username"] == username and u["password"] == password:
                    st.session_state.user = u
                    st.success("Login Successful ✅")
                    st.rerun()

            st.error("Invalid Credentials ❌")


# 🚀 MAIN ROUTING (FIXED - NO DUPLICATION)
def main():
    user = st.session_state.user

    st.sidebar.markdown(f"### 👤 {user['username']}")

    # ================= ADMIN =================
    if user["role"] == "admin":

        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Logout"]
        )

        if menu == "Logout":
            st.session_state.user = None
            st.rerun()

        from pages.admin_dashboard import show_admin
        show_admin(menu)

    # ================= USER =================
    else:

        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Trends", "Overall Trends", "Monthly Summary", "Reminders", "Compare Reports", "Logout"]
        )

        if menu == "Logout":
            st.session_state.user = None
            st.rerun()

        from pages.user_dashboard import show_user
        show_user(menu)


# RUN
if st.session_state.user:
    main()
else:
    login()