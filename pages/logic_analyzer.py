import streamlit as st
import pandas as pd

st.set_page_config(page_title="🔗 Schedule Logic Analyzer", layout="wide")
st.title("🔗 Schedule Logic Analyzer")
st.markdown("Analyze activity relationships and constraints from a Primavera `.xer` file.")

def extract_table(lines, table_name):
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == f"{table_name}%T")
        end = next((i for i in range(start + 1, len(lines)) if lines[i].strip().endswith('%T')), len(lines))
        headers = lines[start + 1].strip().split('\t')
        data = [line.strip().split('\t') for line in lines[start + 2:end]]
        df = pd.DataFrame(data, columns=headers)
        return df
    except StopIteration:
        return pd.DataFrame()

uploaded_file = st.file_uploader("Upload a Primavera .xer file", type=["xer"])

if uploaded_file:
    xer_content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = xer_content.splitlines()

    task_df = extract_table(lines, "TASK")
    pred_df = extract_table(lines, "TASKPRED")

    if not task_df.empty and not pred_df.empty:
        st.subheader("📑 TASK Table Sample")
        st.dataframe(task_df.head(), use_container_width=True)

        st.subheader("📑 TASKPRED Table Sample")
        st.dataframe(pred_df.head(), use_container_width=True)

        st.subheader("🔍 Logic Relationship Counts")
        rel_counts = pred_df["relationship_type"].value_counts().rename({
            "FS": "Finish-Start",
            "SS": "Start-Start",
            "FF": "Finish-Finish",
            "SF": "Start-Finish"
        })
        st.bar_chart(rel_counts)
    else:
        st.error("Required tables (TASK or TASKPRED) not found in uploaded XER.")


