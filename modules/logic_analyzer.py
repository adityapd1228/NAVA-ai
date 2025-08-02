import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df: pd.DataFrame, taskpred_df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("🔍 Logic Analyzer Results")

    # Defensive renaming
    if 'task_name' in task_df.columns:
        task_df = task_df.rename(columns={'task_name': 'Predecessor Name'})
    else:
        st.warning("⚠️ Column 'task_name' not found in task_df. Skipping rename.")
    
    # Defensive drop
    if 'task_id' in task_df.columns:
        task_df = task_df.drop(columns='task_id')
    else:
        st.warning("⚠️ Column 'task_id' not found in task_df. Skipping drop.")

    # Merge with taskpred_df
    merge_cols = ['task_code', 'project_id']
    missing_merge_cols = [col for col in merge_cols if col not in task_df.columns or col not in taskpred_df.columns]
    if missing_merge_cols:
        st.error(f"❌ Cannot merge: Missing columns {missing_merge_cols} in task_df or taskpred_df.")
        return pd.DataFrame()

    merged_df = pd.merge(task_df, taskpred_df, on=merge_cols, how='inner')

    # Sort and reset index
    if 'task_code' in merged_df.columns:
        merged_df = merged_df.sort_values(by='task_code').reset_index(drop=True)
    else:
        st.warning("⚠️ Column 'task_code' not found in merged_df. Skipping sort.")

    # Display output
    st.dataframe(merged_df)

    return merged_df

