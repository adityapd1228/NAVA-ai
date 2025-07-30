
import streamlit as st
import pandas as pd


st.set_page_config(page_title="NAVA AI - Submittal Review", layout="wide")
st.title("📑 Submittal Review Analytics")

uploaded_file = st.file_uploader("Upload Submittal Log (.xlsx)", type=["xlsx"])

if uploaded_file:
    with st.spinner("Analyzing file..."):
        try:
            results = analyze_submittal_log(uploaded_file)

            st.success("Analysis Complete ✅")
            st.subheader("🕐 Delayed Approvals")
            st.dataframe(results['delayed_approvals'])

            st.subheader("⏳ Pending or Rejected")
            st.dataframe(results['pending_or_rejected'])

            st.subheader("❌ Missing Activity Links")
            st.dataframe(results['missing_links'])

            st.subheader("🔎 Long Open Pending Submittals")
            st.dataframe(results['long_open_pending'])

            st.subheader("📋 Full Annotated Log")
            st.dataframe(results['full_log'])

            # Optional download
            st.download_button(
                label="📥 Download Full Log as Excel",
                data=results['full_log'].to_excel(index=False, engine='openpyxl'),
                file_name="annotated_submittal_log.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")
else:
    st.info("Please upload a submittal log Excel file to begin analysis.")
