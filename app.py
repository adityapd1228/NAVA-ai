from modules.logic_analyzer import run_logic_analyzer

# ----------------- Logic Analyzer (.xer) -----------------
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
        st.error(f"Error parsing table {table_name}: {e}")
        return pd.DataFrame()

uploaded_xer = st.file_uploader("📂 Upload a Primavera .xer file", type="xer", key="uploader_2")

if uploaded_xer is not None:
    lines = uploaded_xer.read().decode('utf-8', errors='ignore').splitlines()
    task_df = extract_table(lines, "TASK")
    taskpred_df = extract_table(lines, "TASKPRED")

    if not task_df.empty and not taskpred_df.empty:
        st.success("✅ XER file loaded. Click below to analyze schedule logic.")
        if st.button("Run Logic Analyzer"):
            run_logic_analyzer(task_df, taskpred_df)
    else:
        st.warning("⚠️ TASK or TASKPRED data missing in uploaded file.")

import streamlit as st
import pandas as pd
import io

def analyze_submittal_log(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        df['Flag'] = "Pending Review"
        return {
            'delayed_approvals': df.head(2),
            'pending_or_rejected': df.head(2),
            'missing_links': df.head(2),
            'long_open_pending': df.head(2),
            'full_log': df
        }
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return None

st.set_page_config(page_title="NAVA AI - Submittal Review", layout="wide")
st.title("📄 Submittal Review Analytics")

uploaded_file = st.file_uploader("Upload Submittal Log (.xlsx)", type=["xlsx"], key="uploader_1")

if uploaded_file:
    with st.spinner("Analyzing file..."):
        results = analyze_submittal_log(uploaded_file)

    if results:
        st.success("Analysis Complete ✅")

        st.subheader("⏱ Delayed Approvals")
        st.dataframe(results['delayed_approvals'])

        st.subheader("⏳ Pending or Rejected")
        st.dataframe(results['pending_or_rejected'])

        st.subheader("❌ Missing Activity Links")
        st.dataframe(results['missing_links'])

        st.subheader("🔍 Long Open Pending Submittals")
        st.dataframe(results['long_open_pending'])

        st.subheader("🧾 Full Annotated Log")
        st.dataframe(results['full_log'])

        try:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                results['full_log'].to_excel(writer, sheet_name='Full Log', index=False)
            st.download_button(
                label="📥 Download Full Annotated Log",
                data=output.getvalue(),
                file_name="full_annotated_log.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error during export: {e}")
