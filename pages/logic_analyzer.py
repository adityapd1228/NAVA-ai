import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="🔗 Logic Analyzer", layout="wide")
st.title("🔗 Schedule Logic Analyzer")
st.markdown("Analyze activity relationships and constraints from a Primavera `.xer` file.")

# Function to extract a specific table from XER content
def extract_table(lines, table_name):
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == f"{table_name}%T")
        end = next((i for i in range(start + 1, len(lines)) if lines[i].strip().endswith("%T")), len(lines))
        headers = lines[start + 1].strip().split('\t')
        data = [line.strip().split('\t') for line in lines[start + 2:end]]
        return pd.DataFrame(data, columns=headers)
    except StopIteration:
        return pd.DataFrame()

# Upload .xer file
uploaded_file = st.file_uploader("Upload a Primavera .xer file", type=["xer"])

if uploaded_file:
    xer_content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = xer_content.splitlines()

    # Extract tables
    task_df = extract_table(lines, "TASK")
    pred_df = extract_table(lines, "TASKPRED")

    if task_df.empty or pred_df.empty:
        st.error("❌ Required tables (TASK or TASKPRED) not found in uploaded XER.")
    else:
        st.success("✅ TASK and TASKPRED tables loaded successfully.")
        st.subheader("📄 TASK Table Sample")
        st.dataframe(task_df.head(10), use_container_width=True)

        st.subheader("📄 TASKPRED Table Sample")
        st.dataframe(pred_df.head(10), use_container_width=True)

        # Logic analysis
if not task_df.empty and not pred_df.empty:
    st.subheader("🔍 Logic Relationship Counts")
    rel_counts = pred_df["relationship_type"].value_counts().rename({
        "FS": "Finish-Start",
        "SS": "Start-Start",
        "FF": "Finish-Finish",
        "SF": "Start-Finish"
    })
    st.bar_chart(rel_counts)


        st.bar_chart(rel_counts)

        # Constraints
        st.subheader("📌 Activities with Constraints")
        if 'constraint_type' in task_df.columns:
            constrained_tasks = task_df[task_df['constraint_type'] != '0']
            st.write(f"Found {len(constrained_tasks)} constrained activities.")
            st.dataframe(constrained_tasks, use_container_width=True)
        else:
            st.info("No constraint_type column found in TASK table.")

        # Download results
        st.subheader("⬇️ Export")
        task_csv = task_df.to_csv(index=False).encode('utf-8')
        pred_csv = pred_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download TASK.csv", task_csv, file_name="TASK.csv", mime="text/csv")
        st.download_button("Download TASKPRED.csv", pred_csv, file_name="TASKPRED.csv", mime="text/csv")

