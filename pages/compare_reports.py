import streamlit as st
import pandas as pd
from utils.data_manager import get_user_reports
from utils.comparison import compare_reports

def compare_ui():

    st.title("🔍 Compare Reports")

    user = st.session_state.user["username"]
    reports = get_user_reports(user)

    if len(reports) < 2:
        st.warning("Upload at least 2 reports to compare ❗")
        return

    options = [f"{r['filename']}" for r in reports]

    r1_index = st.selectbox(
        "Select Report 1",
        range(len(options)),
        format_func=lambda x: options[x],
        key="compare_r1"
    )

    r2_index = st.selectbox(
        "Select Report 2",
        range(len(options)),
        format_func=lambda x: options[x],
        key="compare_r2"
    )

    if st.button("Compare Now", key="compare_btn"):

        r1 = reports[r1_index]["data"]
        r2 = reports[r2_index]["data"]

        result = compare_reports(r1, r2)

        df = pd.DataFrame(result, columns=[
            "Parameter",
            "Report 1",
            "Report 2",
            "Change"
        ])

        st.dataframe(df, use_container_width=True)