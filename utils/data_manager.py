import json
from datetime import datetime

USER_FILE = "users.json"
REPORT_FILE = "report_history.json"


# =========================
# 👤 USER FUNCTIONS
# =========================

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def add_user(username, password):
    users = load_users()

    # 🚫 Prevent duplicate users
    for u in users:
        if u["username"] == username:
            return False

    users.append({
        "username": username,
        "password": password,
        "role": "user"
    })

    save_users(users)
    return True


def delete_user(username):
    users = load_users()
    users = [u for u in users if u["username"] != username]
    save_users(users)


# =========================
# 📊 REPORT FUNCTIONS
# =========================

def load_reports():
    try:
        with open(REPORT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_reports(reports):
    with open(REPORT_FILE, "w") as f:
        json.dump(reports, f, indent=4)


def add_report(username, data, filename):
    reports = load_reports()

    reports.append({
        "username": username,
        "data": data,
        "filename": filename,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_reports(reports)


def get_user_reports(username):
    reports = load_reports()
    return [r for r in reports if r["username"] == username]


def delete_report(username, index):
    reports = load_reports()

    # ✅ Get actual index in original list
    user_reports = [(i, r) for i, r in enumerate(reports) if r["username"] == username]

    if 0 <= index < len(user_reports):
        actual_index = user_reports[index][0]
        reports.pop(actual_index)

    save_reports(reports)