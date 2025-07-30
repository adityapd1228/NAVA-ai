
import streamlit as st
import pandas as pd
import io

def analyze_submittal_log(uploaded_file):
    df = pd.read_excel(uploaded_file)

    # Add dummy flags for testing display
    df["Flag"] = "Pending Review"

    return {
        "delayed_approvals": df.head(2),
        "pending_or_rejected": df.head(2),
        "missing_links": df.head(2),
        "long_open_pending": df.head(2),
        "full_log": df
    }

def get_excel_download(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer

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

            st.subheader("🗂️ Full Annotated Log")
            st.dataframe(results['full_log'])

            st.download_button("📥 Download Annotated Log",
                               data=get_excel_download(results["full_log"]),
                               file_name="annotated_log.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"Error during analysis: {e}")
import streamlit as st
import pandas as pd
def analyze_submittal_log(uploaded_file):
    import pandas as pd
    df = pd.read_excel(uploaded_file)

    # Dummy data for now
    return {
        "delayed_approvals": df.head(2),
        "pending_or_rejected": df.head(2),
        "missing_links": df.head(2),
        "long_open_pending": df.head(2),
        "full_log": df  # 
    }

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
