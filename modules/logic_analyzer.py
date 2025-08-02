import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df, taskpred_df):
    # ---------------- Check Columns ----------------
    required_task_cols = ['task_id', 'task_name']
    required_taskpred_cols = ['task_id', 'pred_task_id', 'lag', 'relationship_type']

    missing_task = [col for col in required_task_cols if col not in task_df.columns]
    missing_taskpred = [col for col in required_taskpred_cols if col not in taskpred_df.columns]

    if missing_task:
        st.error(f"Missing columns in TASK table: {missing_task}")
        return
    if missing_taskpred:
        st.error(f"Missing columns in TASKPRED table: {missing_taskpred}")
        return

    # ---------------- Rename Columns for Readability ----------------
    task_df = task_df.rename(columns={'task_name': 'Activity Name'})
    
    # ---------------- Merge ----------------
    merged_df = taskpred_df.merge(
        task_df[['task_id', 'Activity Name']],
        on='task_id', how='left'
    ).merge(
        task_df[['task_id', 'Activity Name']],
        left_on='pred_task_id',
        right_on='task_id',
        suffixes=('_Successor', '_Predecessor'),
        how='left'
    )

    # ---------------- Clean Columns ----------------
    merged_df = merged_df.drop(columns=[col for col in ['task_id_Successor', 'task_id_Predecessor'] if col in merged_df.columns])

    # ---------------- Display ----------------
    st.subheader("📊 Logic Analyzer Results")
    st.dataframe(merged_df)

    # ---------------- Logic Checks ----------------
    invalid_lags = merged_df[merged_df['lag'] > 0]
    if not invalid_lags.empty:
        st.warning(f"⚠️ {len(invalid_lags)} relationships have positive lag.")
        st.dataframe(invalid_lags)

    non_fs = merged_df[merged_df['relationship_type'] != 'FS']
    if not non_fs.empty:
        st.warning(f"⚠️ {len(non_fs)} relationships are not Finish-to-Start (FS).")
        st.dataframe(non_fs)

    st.success("✅ Logic analysis completed.")



