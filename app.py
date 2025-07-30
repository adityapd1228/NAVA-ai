import streamlit as st
import pandas as pd

def analyze_submittal_log(uploaded_file):
    df = pd.read_excel(uploaded_file)

    # Dummy filters for different sections
    delayed_approvals = df[df['Decision'].isna()]
    pending_or_rejected = df[df['Decision'].isin(['Pending', 'Rejected'])]
    missing_links = df[df['Comments'].isna()]
    long_open_pending = df[df['Status'] == 'Open']

    return {
        "delayed_approvals": delayed_approvals,
        "pending_or_rejected": pending_or_rejected,
        "missing_links": missing_links,
        "long_open_pending": long_open_pending,
        "full_log": df
    }

st.set_page_config(page_title="NAVA AI - Submittal Review", layout="wide")
st.title("📄 Submittal Review Analytics")

uploaded_file = st.file_uploader("Upload Submittal Log (.xlsx)", type=["xlsx"])

if uploaded_file:
    with st.spinner("Analyzing file..."):
        try:
            results = analyze_submittal_log(uploaded_file)
            st.success("Analysis Complete ✅")

            st.subheader("⏱️ Delayed Approvals")
            st.dataframe(results['delayed_approvals'])

            st.subheader("⏳ Pending or Rejected")
            st.dataframe(results['pending_or_rejected'])

            st.subheader("❌ Missing Activity Links")
            st.dataframe(results['missing_links'])

            st.subheader("🔍 Long Open Pending Submittals")
            st.dataframe(results['long_open_pending'])

            st.subheader("📋 Full Annotated Log")
            st.dataframe(results['full_log'])

        except Exception as e:
            st.error(f"Error during analysis: {e}")
