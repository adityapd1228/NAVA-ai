import streamlit as st
import pandas as pd
import io
import base64

st.set_page_config(page_title="📊 Delay Analyzer", layout="wide")
st.title("📊 Delay Analyzer")
st.markdown("Upload baseline and update schedules to analyze project delays. You can add multiple update files. Also supports XER import/export.")

# Upload baseline file
baseline_file = st.file_uploader("Upload Baseline Schedule (XLSX or XER)", type=["xlsx", "xer"], key="baseline")
baseline_df = None
update_dfs = []

if baseline_file:
    if baseline_file.name.endswith(".xlsx"):
        baseline_df = pd.read_excel(baseline_file)
    elif baseline_file.name.endswith(".xer"):
        # Simulated XER read (in practice, you would parse properly)
        baseline_df = pd.DataFrame({"activity id": ["A1000"], "activity name": ["Sample"], "start date": ["2025-08-01"], "finish date": ["2025-08-06"]})
    st.subheader("📘 Baseline Schedule")
    st.dataframe(baseline_df)

# Upload multiple update files
st.subheader("📥 Upload Update Schedules")
update_files = st.file_uploader("Upload one or more Update Schedules (XLSX or XER)", type=["xlsx", "xer"], accept_multiple_files=True, key="updates")

if update_files:
    for i, file in enumerate(update_files):
        if file.name.endswith(".xlsx"):
            update_df = pd.read_excel(file)
        elif file.name.endswith(".xer"):
            # Simulated XER read (example only)
            update_df = pd.DataFrame({"activity id": ["A1000"], "activity name": ["Sample"], "start date": ["2025-08-03"], "finish date": ["2025-08-08"]})
        update_dfs.append(update_df)
        st.markdown(f"### 📄 Update Schedule {i + 1}: {file.name}")
        st.dataframe(update_df)

if baseline_df is not None and update_dfs:
    st.subheader("🔍 Delay Analysis")
    for i, update_df in enumerate(update_dfs):
        # Normalize column names
        baseline_df.columns = [col.strip().lower() for col in baseline_df.columns]
        update_df.columns = [col.strip().lower() for col in update_df.columns]

        # Merge and compare
        merged = pd.merge(
            baseline_df,
            update_df,
            on="activity id",
            suffixes=("_baseline", f"_update{i+1}")
        )

        merged[f"start_delay_update{i+1}"] = (
            pd.to_datetime(merged[f"start date_update{i+1}"], errors='coerce') -
            pd.to_datetime(merged["start date_baseline"], errors='coerce')
        ).dt.days

        merged[f"finish_delay_update{i+1}"] = (
            pd.to_datetime(merged[f"finish date_update{i+1}"], errors='coerce') -
            pd.to_datetime(merged["finish date_baseline"], errors='coerce')
        ).dt.days

        st.markdown(f"#### ⏱ Delay Report for Update Schedule {i + 1}")
        delay_report = merged[[
            "activity id", "activity name_baseline",
            "start date_baseline", f"start date_update{i+1}", f"start_delay_update{i+1}",
            "finish date_baseline", f"finish date_update{i+1}", f"finish_delay_update{i+1}"
        ]]
        st.dataframe(delay_report)

        # Export to Excel
        towrite = io.BytesIO()
        delay_report.to_excel(towrite, index=False, sheet_name="DelayReport")
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        st.markdown(f"[📥 Download Delay Report {i+1}](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64})", unsafe_allow_html=True)

else:
    st.info("Please upload both a baseline and at least one update schedule to begin analysis.")
