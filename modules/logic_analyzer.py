import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df: pd.DataFrame, taskpred_df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("📊 Logic Analyzer Results")

    # Step 1: Rename safely
    if 'task_name' in task_df.columns:
        task_df = task_df.rename(columns={'task_name': 'Predecessor Name'})
    else:
        st.warning("⚠️ Column 'task_name' not found in task_df. Rename skipped.")

    # Step 2: Drop 'task_id' only if it exists
    if 'task_id' in task_df.columns:
        task_df = task_df.drop(columns='task_id')
    else:
        st.info("ℹ️ Column 'task_id' not found — skipping drop.")

    # Step 3: Validate columns before merging
    required_cols = {'task_code', 'project_id'}
    if not required_cols.issubset(task_df.columns) or not required_cols.issubset(taskpred_df.columns):
        st.error(f"❌ Cannot merge. Missing required columns: {required_cols}")
        return pd.DataFrame()

    # Step 4: Merge and sort
    merged_df = pd.merge(task_df, taskpred_df, on=['task_code', 'project_id'], how='inner')

    if 'task_code' in merged_df.columns:
        merged_df = merged_df.sort_values(by='task_code').reset_index(drop=True)

    # Step 5: Output
    st.success("✅ Logic analysis complete.")
    st.dataframe(merged_df)

    return merged_df

