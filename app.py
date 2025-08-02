import streamlit as st
from logic_analyzer import run_logic_analyzer
import pandas as pd

st.header("🧠 Schedule Logic Analyzer")

def extract_table(lines, table_name):
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == f"{table_name}%T")
        end = next((i for i in range(start + 1, len(lines)) if lines[i].strip().endswith('%T')), len(lines))
        headers = lines[start + 1].strip().split('\t')
        data = [line.strip().split('\t') for line in lines[start + 2:end]]
        df = pd.DataFrame(data, columns=headers)
        return df
    except Exception as e:
        st.error(f"Failed to extract table {table_name}: {e}")
        return pd.DataFrame()

# ---- Upload and Process XER ----
uploaded_file = st.file_uploader("Upload a Primavera .xer file", type=["xer"])

if uploaded_file:
    lines = uploaded_file.read().decode("utf-8").splitlines()
    task_df = extract_table(lines, "TASK")
    taskpred_df = extract_table(lines, "TASKPRED")

    if task_df.empty or taskpred_df.empty:
        st.error("TASK or TASKPRED data missing in uploaded file.")
    else:
        run_logic_analyzer(task_df, taskpred_df)

    if not task_df.empty and not taskpred_df.empty:
        run_logic_analyzer(task_df, taskpred_df)
    else:
        st.warning("⚠️ TASK or TASKPRED data missing in uploaded file.")

