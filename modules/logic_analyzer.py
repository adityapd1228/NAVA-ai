import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df, taskpred_df):
    st.subheader("🧠 Logic Analyzer Results")

    # Check if essential columns exist
    required_task_cols = ['task_id', 'task_name']
    required_taskpred_cols = ['task_id', 'pred_task_id', 'lag', 'relationship_type']

    missing_task = [col for col in required_task_cols if col not in task_df.columns]
    missing_taskpred = [col for col in required_taskpred_cols if col not in taskpred_df.columns]

    if missing_task:
        st.error(f"❌ Missing column(s) in TASK table: {missing_task}")
        st.write("Available columns:", task_df.columns.tolist())
        return

    if missing_taskpred:
        st.error(f"❌ Missing column(s) in TASKPRED table: {missing_taskpred}")
        st.write("Available columns:", taskpred_df.columns.tolist())
        return

    # Rename for clarity
    task_df = task_df.rename(columns={'task_name': 'Activity Name'})

    # Merge task predecessor logic with task names
    merged_df = taskpred_df.merge(
        task_df[['task_id', 'Activity Name']],
        on='task_id', how='left'
    ).merge(
        task_df[['task_id', 'Activity Name']],
        left_on='pred_task_id', right_on='task_id',
        suffixes=('_Successor', '_Predecessor'),
        how='left'
    )

    # Drop duplicate task_id columns if they exist
    cols_to_drop = [col for col in ['task_id_x', 'task_id_y'] if col in merged_df.columns]
    merged_df.drop(columns=cols_to_drop, inplace=True)

    # Display table
    st.write("📋 Full Predecessor Relationship Table")
    st.dataframe(merged_df)

    # Check for logic issues
    invalid_lags = merged_df[merged_df['lag'] > 0]
    if not invalid_lags.empty:
        st.warning(f"⚠️ {len(invalid_lags)} logic links have positive lag.")
        st.dataframe(invalid_lags)

    non_fs = merged_df[merged_df['relationship_type'] != 'FS']
    if not non_fs.empty:
        st.warning(f"⚠️ {len(non_fs)} relationships are not FS (Finish-Start).")
        st.dataframe(non_fs)

    st.success("✅ Logic analysis complete.")
