import streamlit as st
import pandas as pd
import io

def analyze_submittal_log(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)

        # Add mock columns or flags for testing logic
        df['Flag'] = "Pending Review"

        return {
            'delayed_approvals': df.head(2),
            'pending_or_rejected': df.head(2),
            'missing_links': df.head(2),
            'long_open_pending': df.head(2),
            'full_log': df
        }
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return None

# App UI
st.set_page_config(page_title="NAVA AI - Submittal Review", layout="wide")
st.title("📄 Submittal Review Analytics")

uploaded_file = st.file_uploader("Upload Submittal Log (.xlsx)", type=["xlsx"], key="uploader_1")

if uploaded_file:
    with st.spinner("Analyzing file..."):
        results = analyze_submittal_log(uploaded_file)

    if results:
        st.success("Analysis Complete ✅")

        st.subheader("⏱ Delayed Approvals")
        st.dataframe(results['delayed_approvals'])

        st.subheader("⏳ Pending or Rejected")
        st.dataframe(results['pending_or_rejected'])

        st.subheader("❌ Missing Activity Links")
        st.dataframe(results['missing_links'])

        st.subheader("🔍 Long Open Pending Submittals")
        st.dataframe(results['long_open_pending'])

        st.subheader("🧾 Full Annotated Log")
        st.dataframe(results['full_log'])

        # Export to Excel
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                results['full_log'].to_excel(writer, sheet_name='Full Log', index=False)
                writer.save()
            st.download_button(
                label="📥 Download Full Annotated Log",
                data=output.getvalue(),
                file_name="full_annotated_log.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error during export: {e}")
