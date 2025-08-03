
import streamlit as st
import pandas as pd
import io
import base64
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="🔍 Logic Analyzer", layout="wide")
st.title("🔍 Logic Analyzer")
st.markdown("Upload a Primavera P6 schedule in XER or Excel format to analyze logic, relationships, and constraints.")

file = st.file_uploader("Upload Schedule File (XER or XLSX)", type=["xer", "xlsx"])
df = None

if file:
    if file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    elif file.name.endswith(".xer"):
        # Fake parser for demonstration
        df = pd.DataFrame({
            "activity id": ["A1000", "A1001", "A1002"],
            "activity name": ["Start", "Foundation", "Walls"],
            "logic type": ["Start", "FS", "SS"],
            "predecessor": ["", "A1000", "A1001"],
            "successor": ["A1001", "A1002", ""],
            "lag": [0, 2, -1],
            "constraint": ["", "Start On or After 01-Aug-25", "Finish No Later Than 15-Aug-25"]
        })

    st.subheader("📋 Parsed Logic Table")
    st.dataframe(df)

    # Logic Insights
    st.subheader("🧠 Logic Insights")

    fs_count = df[df["logic type"] == "FS"].shape[0]
    ss_count = df[df["logic type"] == "SS"].shape[0]
    ff_count = df[df["logic type"] == "FF"].shape[0]
    sf_count = df[df["logic type"] == "SF"].shape[0]
    lead_count = df[df["lag"] < 0].shape[0]
    lag_count = df[df["lag"] > 0].shape[0]
    constraint_count = df[df["constraint"] != ""].shape[0]
    missing_preds = df[df["predecessor"] == ""].shape[0]
    missing_succs = df[df["successor"] == ""].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("FS Links", fs_count)
    col2.metric("SS Links", ss_count)
    col3.metric("FF Links", ff_count)

    col1, col2, col3 = st.columns(3)
    col1.metric("Leads (<0 Lag)", lead_count)
    col2.metric("Lags (>0 Lag)", lag_count)
    col3.metric("Constraints", constraint_count)

    col1, col2 = st.columns(2)
    col1.metric("Missing Predecessors", missing_preds)
    col2.metric("Missing Successors", missing_succs)

    # AI-based Summary
    st.subheader("🧾 Narrative Summary")
    summary = (
        f"The uploaded schedule has {fs_count} Finish-to-Start links, {ss_count} Start-to-Start links, and {ff_count} Finish-to-Finish links. "
        f"There are {lead_count} activities with leads (negative lag) and {lag_count} with positive lags. "
        f"{constraint_count} activities have constraints, which may impact float and logic transparency. "
        f"There are {missing_preds} activities missing predecessors and {missing_succs} missing successors, which can indicate logic gaps or broken sequences."
    )
    st.write(summary)

    # Download as Excel
    st.subheader("📤 Export Logic Report")
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, sheet_name="LogicReport")
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    st.markdown(f"[📥 Download Logic Report (Excel)](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64})", unsafe_allow_html=True)

    # Export as PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Logic Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.today().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=summary)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    b64_pdf = base64.b64encode(pdf_output.read()).decode()
    st.markdown(f"[📥 Download Logic Report (PDF)](data:application/pdf;base64,{b64_pdf})", unsafe_allow_html=True)

else:
    st.info("Please upload a valid XER or XLSX schedule file to begin logic analysis.")
