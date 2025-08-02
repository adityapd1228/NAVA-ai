
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📝 Markup Translator", layout="wide")
st.title("📝 Markup Translator")
st.markdown("Upload a marked-up Excel file with activity updates. This module will extract changes and generate a P6-import-ready file.")

uploaded_file = st.file_uploader("Upload Marked-up Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normalize column names
    df.columns = [col.strip() for col in df.columns]

    required_columns = ["Activity ID", "Activity Name", "Original Start", "Original Finish", "New Start Date", "New Finish Date"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
    else:
        st.subheader("📋 Raw Marked-up Data")
        st.dataframe(df.head())

        # Calculate delays
        df["Start Delay (days)"] = (df["New Start Date"] - df["Original Start"]).dt.days
        df["Finish Delay (days)"] = (df["New Finish Date"] - df["Original Finish"]).dt.days
        df["Has Changes"] = (df["Start Delay (days)"] != 0) | (df["Finish Delay (days)"] != 0)

        # Show change log
        st.subheader("🔍 Extracted Change Log")
        change_log = df[df["Has Changes"]].copy()
        st.dataframe(change_log)

        # Download change log
        buffer_xlsx = io.BytesIO()
        with pd.ExcelWriter(buffer_xlsx, engine='xlsxwriter') as writer:
            change_log.to_excel(writer, index=False, sheet_name="ChangeLog")
        st.download_button("📄 Download Change Log (Excel)", buffer_xlsx.getvalue(), file_name="change_log.xlsx")

        # Create and download P6-ready CSV
        p6_import = change_log[["Activity ID", "New Start Date", "New Finish Date"]].copy()
        p6_import.columns = ["Activity ID", "Start Date", "Finish Date"]
        buffer_csv = io.StringIO()
        p6_import.to_csv(buffer_csv, index=False)
        st.download_button("📁 Download P6 Import File (CSV)", buffer_csv.getvalue(), file_name="p6_import_ready.csv")
else:
    st.info("Upload an Excel file to begin.")
