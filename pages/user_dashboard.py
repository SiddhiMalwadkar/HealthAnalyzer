import streamlit as st
from utils.pdf_parser import extract_parameters_from_pdf
from utils.data_manager import add_report, get_user_reports, delete_report
from pages.compare_reports import compare_ui
import matplotlib.pyplot as plt
import requests


# 🔔 TELEGRAM FUNCTION
def send_telegram_message(message):

    BOT_TOKEN = "your both token"
    CHAT_ID = "your chat id"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=data)
    except:
        print("Telegram message failed")


def show_user(menu):

    user = st.session_state.user["username"]

    if "last_file" not in st.session_state:
        st.session_state.last_file = None

    # ================= DASHBOARD =================
    if menu == "Dashboard":

        st.title(f"👋 Welcome, {user}")

        st.markdown("### 📂 Upload Health Report")

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            key=f"upload_pdf_{user}"   # ✅ FIXED
        )

        if uploaded_file is not None:

            if st.button("⚙️ Process Report", key=f"process_{user}"):

                if st.session_state.last_file != uploaded_file.name:

                    uploaded_file.seek(0)

                    data = extract_parameters_from_pdf(uploaded_file)

                    add_report(user, data, uploaded_file.name)

                    st.session_state.last_file = uploaded_file.name

                    st.success("✅ Report uploaded and processed")
                    st.json(data)

                else:
                    st.warning("⚠️ This file is already processed")

        st.markdown("---")

        reports = get_user_reports(user)

        st.markdown("### 📊 Your Reports")
        st.write(f"Total Reports: {len(reports)}")

        st.markdown("---")

        st.markdown("### 🗂️ Manage Reports")

        if len(reports) == 0:
            st.info("No reports uploaded yet")

        else:
            for i, r in enumerate(reports):
                col1, col2 = st.columns([4, 1])

                col1.write(f"📄 {r.get('filename', 'Report')} — {r['date']}")

                if col2.button("❌ Delete", key=f"del_{user}_{i}"):
                    delete_report(user, i)
                    st.warning("Report deleted")
                    st.rerun()

    # ================= TRENDS =================
    elif menu == "Trends":

        st.title("📊 Parameter Trends")

        reports = get_user_reports(user)

        if len(reports) == 0:
            st.warning("No reports available")

        else:
            all_params = set()
            for r in reports:
                all_params.update(r["data"].keys())

            selected_param = st.selectbox(
                "Select Parameter",
                sorted(all_params),
                key=f"trend_param_{user}"   # ✅ FIXED
            )

            values = []
            dates = []

            for r in reports:
                val = r["data"].get(selected_param, "N/A")

                if isinstance(val, (int, float)):
                    values.append(val)
                    dates.append(r["date"])

            if values:
                plt.figure()
                plt.plot(dates, values, marker='o')
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("No numeric data")

    # ================= OVERALL =================
    elif menu == "Overall Trends":

        st.title("📊 Overall Health Trends")

        reports = get_user_reports(user)

        if len(reports) == 0:
            st.warning("No reports available")

        else:
            dates = []
            h, g, b = [], [], []

            for r in reports:
                dates.append(r["date"])
                h.append(r["data"].get("Hemoglobin"))
                g.append(r["data"].get("Glucose Fasting"))
                b.append(r["data"].get("Bilirubin Total"))

            plt.figure()

            plt.plot(dates, h, marker='o', label="Hemoglobin")
            plt.plot(dates, g, marker='o', label="Glucose")
            plt.plot(dates, b, marker='o', label="Bilirubin")

            plt.legend()
            plt.xticks(rotation=45)

            st.pyplot(plt)

    # ================= MONTHLY =================
    elif menu == "Monthly Summary":

        st.title("📅 Monthly Summary")

        reports = get_user_reports(user)

        from collections import defaultdict

        monthly = defaultdict(list)

        for r in reports:
            monthly[r["date"][:7]].append(r["data"])

        for m, data_list in monthly.items():

            st.subheader(m)

            combined = {}

            for d in data_list:
                for k, v in d.items():
                    if isinstance(v, (int, float)):
                        combined.setdefault(k, []).append(v)

            for k, v in combined.items():
                st.write(f"{k} → Avg:{round(sum(v)/len(v),2)} Min:{min(v)} Max:{max(v)}")

    # ================= REMINDERS =================
    elif menu == "Reminders":

        st.title("🔔 Reminder System")

        title = st.text_input("Reminder Title", key=f"rem_title_{user}")

        r_type = st.selectbox(
            "Type",
            ["Test", "Medicine", "Checkup"],
            key=f"rem_type_{user}"
        )

        date = st.date_input("Select Date", key=f"rem_date_{user}")

        if st.button("Set Reminder", key=f"rem_btn_{user}"):

            if title == "":
                st.error("Enter title")
            else:
                message = f"""
🔔 Reminder
Title: {title}
Type: {r_type}
Date: {date}
"""
                send_telegram_message(message)
                st.success("Reminder sent ✅")

    # ================= COMPARE =================
    elif menu == "Compare Reports":
        compare_ui()
