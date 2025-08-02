import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df, taskpred_df):
    # Check required columns
    required_task_cols = ['task_name', 'task_id']
    required_taskpred_cols = ['task_id', 'pred_task_id', 'lag', 'relationship_type']

    # Validate task_df
    missing_task_cols = [col for col in required_task_cols if col not in task_df.columns]
    if missing_task_cols:
        st.error(f"Missing column(s) in TASK table: {missing_task_cols}")
        return

    # Validate taskpred_df
    missing_taskpred_cols = [col for col in required_taskpred_cols if col not in taskpred_df.columns]
    if missing_taskpred_cols:
        st.error(f"Missing column(s) in TASKPRED table: {missing_taskpred_cols}")
        return

    # Prepare data
    task_df = task_df.rename(columns={'task_name': 'Activity Name'})  # Rename for clarity
    merged_df = taskpred_df.merge(
        task_df[['task_id', 'Activity Name']],
        how='left',
        left_on='task_id',
        right_on='task_id'
    ).merge(
        task_df[['task_id', 'Activity Name']],
        how='left',
        left_on='pred_task_id',
        right_on='task_id',
        suffixes=('_Successor', '_Predecessor')
    )

    # Drop ID columns if needed
    merged_df = merged_df.drop(columns=['task_id_Successor', 'task_id_Predecessor'], errors='ignore')

    # Show results
    st.subheader("🔍 Logic Analysis Summary")
    st.write(merged_df.head())

    # Optional: Logic checks (e.g., lag, invalid relationships, etc.)
    invalid_lags = merged_df[merged_df['lag'] > 0]
    if not invalid_lags.empty:
        st.warning(f"⚠️ {len(invalid_lags)} activities have positive lag.")
        st.dataframe(invalid_lags)

    fs_relationships = merged_df[merged_df['relationship_type'] != 'FS']
    if not fs_relationships.empty:
        st.warning(f"⚠️ {len(fs_relationships)} activities have non-FS relationships.")
        st.dataframe(fs_relationships)

    st.success("✅ Logic analysis completed.")


