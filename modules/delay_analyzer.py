
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📊 Delay Analyzer", layout="wide")
st.title("📊 Delay Analyzer")
st.markdown("Compare two project schedules (Baseline vs Updated) to detect and quantify delays.")

col1, col2 = st.columns(2)

with col1:
    baseline_file = st.file_uploader("Upload Baseline Schedule (Excel)", type=["xlsx"], key="baseline")

with col2:
    updated_file = st.file_uploader("Upload Updated Schedule (Excel)", type=["xlsx"], key="updated")

if baseline_file and updated_file:
    baseline_df = pd.read_excel(baseline_file)
    updated_df = pd.read_excel(updated_file)

    # Normalize column names
    baseline_df.columns = [col.strip() for col in baseline_df.columns]
    updated_df.columns = [col.strip() for col in updated_df.columns]

    required_columns = ["Activity ID", "Start Date", "Finish Date"]
    if not all(col in baseline_df.columns for col in required_columns) or not all(col in updated_df.columns for col in required_columns):
        st.error(f"Both files must contain the following columns: {', '.join(required_columns)}")
    else:
        st.subheader("📋 Baseline Schedule Sample")
        st.dataframe(baseline_df.head())

        st.subheader("📋 Updated Schedule Sample")
        st.dataframe(updated_df.head())

        # Merge and compute delay
        merged = pd.merge(
            baseline_df,
            updated_df,
            on="Activity ID",
            suffixes=("_Baseline", "_Updated")
        )

        merged["Start Delay (days)"] = (merged["Start Date_Updated"] - merged["Start Date_Baseline"]).dt.days
        merged["Finish Delay (days)"] = (merged["Finish Date_Updated"] - merged["Finish Date_Baseline"]).dt.days
        merged["Has Delay"] = (merged["Start Delay (days)"] != 0) | (merged["Finish Delay (days)"] != 0)

        delay_log = merged[merged["Has Delay"]].copy()

        st.subheader("🔍 Detected Delays")
        st.dataframe(delay_log)

        # Export options
        buffer_xlsx = io.BytesIO()
        with pd.ExcelWriter(buffer_xlsx, engine='xlsxwriter') as writer:
            delay_log.to_excel(writer, index=False, sheet_name="DelayLog")
        st.download_button("📄 Download Delay Log (Excel)", buffer_xlsx.getvalue(), file_name="delay_log.xlsx")

        buffer_csv = io.StringIO()
        delay_log.to_csv(buffer_csv, index=False)
        st.download_button("📁 Download Delay Log (CSV)", buffer_csv.getvalue(), file_name="delay_log.csv")
else:
    st.info("Upload both baseline and updated schedule files to begin.")
