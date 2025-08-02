import streamlit as st
import pandas as pd

st.set_page_config(page_title="📄 XER File Parser", layout="wide")
st.title("📄 XER File Parser")
st.markdown("Upload a Primavera `.xer` file to parse `TASK` and `TASKPRED` tables.")

def read_xer_tables(uploaded_file):
    lines = uploaded_file.getvalue().decode("utf-8", errors="ignore").splitlines()

    tables = {}
    table_name = None
    headers = []
    data = []

    for line in lines:
        line = line.strip()
        if line == "%T":
            continue
        elif line.startswith("%T"):
            table_name = line[2:].strip()
            headers = []
            data = []
        elif line.startswith("%F"):
            headers = line[2:].split("\t")
        elif line.startswith("%R"):
            values = line[2:].split("\t")
            data.append(values)
        elif line.startswith("%E") and table_name:
            df = pd.DataFrame(data, columns=headers)
            tables[table_name] = df
            table_name = None

    return tables

uploaded_file = st.file_uploader("Upload a Primavera XER File", type=["xer"])

if uploaded_file:
    try:
        tables = read_xer_tables(uploaded_file)
        st.success("File parsed successfully.")

        if "TASK" in tables:
            st.subheader("📋 TASK Table")
            st.dataframe(tables["TASK"])
        else:
            st.warning("TASK table not found.")

        if "TASKPRED" in tables:
            st.subheader("🔗 TASKPRED Table")
            st.dataframe(tables["TASKPRED"])
        else:
            st.warning("TASKPRED table not found.")

        st.info(f"Tables found: {', '.join(tables.keys())}")

    except Exception as e:
        st.error(f"❌ Error parsing file: {str(e)}")
