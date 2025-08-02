import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df, taskpred_df):
    st.subheader("🔍 Logic Analyzer Results")

    # Check if required columns exist before renaming or dropping
    if 'task_name' in task_df.columns:
        task_df = task_df.rename(columns={'task_name': 'Predecessor Name'})

    if 'task_id' in task_df.columns:
        task_df = task_df.drop(columns='task_id')

    # Check if 'task_id' exists in taskpred_df before proceeding
    if 'task_id' not in taskpred_df.columns or 'pred_task_id' not in taskpred_df.columns:
        st.error("Required columns 'task_id' or 'pred_task_id' not found in task predecessor table.")
        return

    try:
        # Merge the two dataframes on task_id
        merged_df = pd.merge(
            task_df,
            taskpred_df,
            how='left',
            left_on='task_id' if 'task_id' in task_df.columns else task_df.columns[0],
            right_on='task_id'
        )

        # Logic Issue Check: Find tasks with missing predecessors
        no_pred_df = merged_df[merged_df['pred_task_id'].isnull()]

        st.markdown("### 🔗 Tasks Without Predecessors")
        if not no_pred_df.empty:
            st.dataframe(no_pred_df)
        else:
            st.success("✅ All tasks have defined predecessor logic.")

    except Exception as e:
        st.error(f"❌ Logic analysis failed: {e}")
