import pandas as pd
import streamlit as st

def run_logic_analyzer(task_df, taskpred_df):
    st.subheader("📊 Logic Analyzer Results")

    # Merge logic info with task names
    logic_df = taskpred_df.merge(
        task_df[['task_id', 'task_name']],
        left_on='pred_task_id', right_on='task_id', how='left'
    ).rename(columns={'task_name': 'Predecessor Name'}).drop(columns='task_id')

    logic_df = logic_df.merge(
        task_df[['task_id', 'task_name']],
        left_on='task_id', right_on='task_id', how='left'
    ).rename(columns={'task_name': 'Successor Name'})

    # Map relationship types
    rel_map = {0: 'FS', 1: 'SS', 2: 'FF', 3: 'SF'}
    logic_df['Relationship Type'] = logic_df['relationship_type'].map(rel_map)
    logic_df['Lag (days)'] = logic_df['lag'] / 480  # Assuming 8hr = 480min

    # Flag high lags
    logic_df['Lag Warning'] = logic_df['Lag (days)'].apply(
        lambda x: '⚠️ High Lag' if abs(x) > 5 else '')

    # --- FLOAT & CONSTRAINTS ---
    st.markdown("### 🕒 Float & Constraint Analysis")

    task_df['Total Float (days)'] = task_df['total_float'] / 480
    task_df['Free Float (days)'] = task_df['free_float'] / 480

    constraint_map = {
        0: 'None', 1: 'Start On', 2: 'Finish On', 3: 'Start On or After',
        4: 'Start On or Before', 5: 'Finish On or After',
        6: 'Finish On or Before', 7: 'Mandatory Start', 8: 'Mandatory Finish'
    }
    task_df['Constraint Type'] = task_df['constraint_type'].map(constraint_map)

    # Flag risky float/constraint issues
    task_df['Float Warning'] = task_df['Total Float (days)'].apply(
        lambda x: '🟥 Negative Float' if x < 0 else ('🟨 Zero Float' if x == 0 else ''))

    task_df['Constraint Warning'] = task_df['Constraint Type'].apply(
        lambda x: '⚠️ Hard Constraint' if x in ['Mandatory Start', 'Mandatory Finish'] else '')

    st.dataframe(task_df[['task_id', 'task_name', 'Total Float (days)', 'Free Float (days)',
                          'Float Warning', 'Constraint Type', 'Constraint Warning']])

    # --- Missing Logic Check ---
    st.markdown("### ❌ Missing Logic")
    missing_pred = task_df[~task_df['task_id'].isin(taskpred_df['task_id'])]
    missing_succ = task_df[~task_df['task_id'].isin(taskpred_df['pred_task_id'])]

    st.write("**Activities without Predecessors:**")
    st.dataframe(missing_pred[['task_id', 'task_name']])

    st.write("**Activities without Successors:**")
    st.dataframe(missing_succ[['task_id', 'task_name']])

    # --- Export Combined Report ---
    combined_export = task_df[['task_id', 'task_name', 'Total Float (days)', 'Free Float (days)',
                               'Float Warning', 'Constraint Type', 'Constraint Warning']]

    st.download_button("⬇️ Download Float/Constraint Report (Excel)",
                       data=combined_export.to_excel(index=False),
                       file_name="float_constraint_report.xlsx")

    return logic_df
