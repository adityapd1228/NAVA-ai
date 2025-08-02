import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df: pd.DataFrame, taskpred_df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("📊 Logic Analyzer Results")

    # Show columns before processing
    st.write("🧾 task_df columns:", task_df.columns.tolist())
    st.write("🧾 taskpred_df columns:", taskpred_df.columns.tolist())

    # Rename 'task_name' if present
    if 'task_name' in task_df.columns:
        task_df = task_df.rename(columns={'task_name': 'Predecessor Name'})
    else:
        st.warning("⚠️ Column 'task_name' not found in task_df — rename skipped.")

    # Drop 'task_id' only if it exists
    if 'task_id' in task_df.columns:
        task_df = task_df.drop(columns='task_id')
        st.info("✅ Dropped column 'task_id'.")
    else:
        st.info("ℹ️ Column 'task_id' not found — no drop needed.")

    # Check required columns before merge
    required_cols = {'task_code', 'project_id'}
    missing_task = required_cols - set(task_df.columns)
    missing_pred = required_cols - set(taskpred_df.columns)

    if missing_task:
        st.error(f"❌ Missing columns in task_df: {missing_task}")
        return pd.DataFrame()
    if missing_pred:
        st.error(f"❌ Missing columns in taskpred_df: {missing_pred}")
        return pd.DataFrame()

    # Merge dataframes
    merged_df = pd.merge(task_df, taskpred_df, on=['task_code', 'project_id'], how='inner')
    st.success("✅ Merge complete.")

    # Sort if task_code is present
    if 'task_code' in merged_df.columns:
        merged_df = merged_df.sort_values(by='task_code').reset_index(drop=True)
        st.success("✅ Sorted by 'task_code'.")

    # Output results
    st.dataframe(merged_df)
    return merged_df


