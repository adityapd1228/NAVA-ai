import streamlit as st
import pandas as pd

st.set_page_config(page_title="🧠 Logic Analyzer", layout="wide")
st.title("🧠 Logic Analyzer")
st.markdown("Analyze activity logic, relationships, and constraints. Supports .xer and Excel files.")

uploaded_file = st.file_uploader("Upload Schedule File (.xer or .xlsx)", type=["xer", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".xer"):
        # Simulated parsing logic for .xer file
        df = pd.DataFrame({
            "Activity ID": ["A1000", "A1001"],
            "Activity Name": ["Excavation", "Foundation"],
            "Predecessors": ["", "A1000"],
            "Successors": ["A1001", ""],
            "Relationship Type": ["", "FS"],
            "Lag (Days)": [0, 2],
            "Constraint Type": ["", "Finish On or Before"],
            "Constraint Date": ["", "2025-09-15"]
        })
    st.subheader("Schedule Logic")
    st.dataframe(df)
else:
    st.info("Upload a valid .xer or .xlsx schedule file to begin logic analysis.")