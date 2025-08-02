
import streamlit as st
import pandas as pd
import io
import base64
import plotly.express as px
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="📊 Delay Analyzer", layout="wide")
st.title("📊 Delay Analyzer")
st.markdown("Upload baseline and update schedules to analyze project delays. You can add multiple update files. Also supports XER import/export.")

# Upload baseline file
baseline_file = st.file_uploader("Upload Baseline Schedule (XLSX or XER)", type=["xlsx", "xer"], key="baseline")
baseline_df = None
update_dfs = []

if baseline_file:
    if baseline_file.name.endswith(".xlsx"):
        baseline_df = pd.read_excel(baseline_file)
    elif baseline_file.name.endswith(".xer"):
        baseline_df = pd.DataFrame({"activity id": ["A1000"], "activity name": ["Sample"], "start date": ["2025-08-01"], "finish date": ["2025-08-06"]})
    st.subheader("📘 Baseline Schedule")
    st.dataframe(baseline_df)

# Upload multiple update files
st.subheader("📥 Upload Update Schedules")
update_files = st.file_uploader("Upload one or more Update Schedules (XLSX or XER)", type=["xlsx", "xer"], accept_multiple_files=True, key="updates")

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
# Title Page
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, txt="Delay Analysis Report", ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Generated on: {datetime.today().strftime('%Y-%m-%d')} ", ln=True, align='C')
pdf.ln(10)

# Placeholder project title
pdf.cell(200, 10, txt="Project: Sample Project", ln=True, align='C')
pdf.ln(10)

# Summary placeholders
summary_text = (
    "This report presents an overview of project delays based on the provided baseline and update schedules. "
    "It includes delay metrics, graphical insights, and narrative summaries for arbitration or executive review."
)
pdf.multi_cell(0, 10, txt=summary_text)

# Initialize metrics
summary_stats = []
total_activities = 0
total_delayed = 0
max_delay = 0
avg_start_delay = 0
avg_finish_delay = 0

if update_files:
    for i, file in enumerate(update_files):
        if file.name.endswith(".xlsx"):
            update_df = pd.read_excel(file)
        elif file.name.endswith(".xer"):
            update_df = pd.DataFrame({"activity id": ["A1000"], "activity name": ["Sample"], "start date": ["2025-08-03"], "finish date": ["2025-08-08"]})
        update_dfs.append(update_df)
        st.markdown(f"### 📄 Update Schedule {i + 1}: {file.name}")
        st.dataframe(update_df)

if baseline_df is not None and update_dfs:
    st.subheader("🔍 Delay Analysis")
    for i, update_df in enumerate(update_dfs):
        baseline_df.columns = [col.strip().lower() for col in baseline_df.columns]
        update_df.columns = [col.strip().lower() for col in update_df.columns]

        merged = pd.merge(
            baseline_df,
            update_df,
            on="activity id",
            suffixes=("_baseline", f"_update{i+1}")
        )

        merged[f"start_delay_update{i+1}"] = (
            pd.to_datetime(merged[f"start date_update{i+1}"], errors='coerce') -
            pd.to_datetime(merged["start date_baseline"], errors='coerce')
        ).dt.days

        merged[f"finish_delay_update{i+1}"] = (
            pd.to_datetime(merged[f"finish date_update{i+1}"], errors='coerce') -
            pd.to_datetime(merged["finish date_baseline"], errors='coerce')
        ).dt.days

        def tag_root_cause(row):
            if row[f"finish_delay_update{i+1}"] > 5:
                return "Resource Constraint"
            elif row[f"start_delay_update{i+1}"] > 2:
                return "Late Start"
            else:
                return "Minor Delay"

        merged[f"root_cause_update{i+1}"] = merged.apply(tag_root_cause, axis=1)

        st.markdown(f"#### ⏱ Delay Report for Update Schedule {i + 1}")
        delay_report = merged[[
            "activity id", "activity name_baseline",
            "start date_baseline", f"start date_update{i+1}", f"start_delay_update{i+1}",
            "finish date_baseline", f"finish date_update{i+1}", f"finish_delay_update{i+1}",
            f"root_cause_update{i+1}"
        ]]
        st.dataframe(delay_report)

        total_activities += delay_report.shape[0]
        total_delayed += delay_report[(delay_report[f"start_delay_update{i+1}"] > 0) | (delay_report[f"finish_delay_update{i+1}"] > 0)].shape[0]
        max_delay = max(max_delay, delay_report[[f"start_delay_update{i+1}", f"finish_delay_update{i+1}"]].max().max())
        avg_start_delay += delay_report[f"start_delay_update{i+1}"].mean()
        avg_finish_delay += delay_report[f"finish_delay_update{i+1}"].mean()

        fig = px.bar(
            delay_report,
            x="activity id",
            y=[f"start_delay_update{i+1}", f"finish_delay_update{i+1}"],
            title=f"Delay Distribution – Update {i + 1}",
            labels={"value": "Days", "variable": "Delay Type"},
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

        towrite = io.BytesIO()
        delay_report.to_excel(towrite, index=False, sheet_name="DelayReport")
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        st.markdown(f"[📥 Download Delay Report {i+1} (Excel)](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64})", unsafe_allow_html=True)

        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Delay Report – Update {i+1}", ln=True, align='C')
        for index, row in delay_report.iterrows():
            row_text = f"{row['activity id']} | {row['activity name_baseline']} | Start Delay: {row[f'start_delay_update{i+1}']} | Finish Delay: {row[f'finish_delay_update{i+1}']} | Root Cause: {row[f'root_cause_update{i+1}']}"
            pdf.cell(200, 10, txt=row_text, ln=True)

        pdf.cell(200, 10, txt="Narrative:", ln=True)
        pdf.multi_cell(0, 10, txt=(
            f"In Update {i+1}, a total of {delay_report.shape[0]} activities were analyzed. "
            f"Of these, {total_delayed} showed delay. "
            f"The maximum observed delay was {int(max_delay)} days. "
            f"This update reflects schedule slippages that may relate to resource availability, delayed mobilization, or external dependencies."
        ))

    st.subheader("📊 Summary Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Activities", total_activities)
    col2.metric("Delayed Activities", total_delayed)
    col3.metric("Max Delay (days)", int(max_delay))
    col4.metric("Avg Start Delay (days)", round(avg_start_delay / len(update_dfs), 1))

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    b64_pdf = base64.b64encode(pdf_output.read()).decode()
    st.markdown(f"[📥 Download Delay Report (PDF)](data:application/pdf;base64,{b64_pdf})", unsafe_allow_html=True)

else:
    st.info("Please upload both a baseline and at least one update schedule to begin analysis.")
