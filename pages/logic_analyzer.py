
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import io

st.set_page_config(page_title="Logic Analyzer", layout="wide")
st.title("🔗 Logic Analyzer")
st.markdown("Analyze logical relationships between activities, leads, lags, float, and constraints from uploaded schedule data.")

uploaded_file = st.file_uploader("Upload Schedule File (XLSX)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = [col.lower() for col in df.columns]

    st.subheader("📋 Raw Schedule Data")
    st.dataframe(df)

    # Display logic types distribution
    if "logic type" in df.columns:
        st.subheader("🧠 Logic Type Distribution")
        fig_logic = px.histogram(df, x="logic type", title="Logic Type Frequency")
        st.plotly_chart(fig_logic, use_container_width=True)

    # Leads and Lags
    if "lag" in df.columns:
        st.subheader("⏱ Lead/Lag Analysis")
        fig_lag = px.histogram(df, x="lag", title="Lag Distribution (Positive = Lag, Negative = Lead)")
        st.plotly_chart(fig_lag, use_container_width=True)

    # Float Analysis
    if "total float" in df.columns:
        st.subheader("📉 Float Analysis")
        fig_float = px.histogram(df, x="total float", title="Total Float Distribution")
        st.plotly_chart(fig_float, use_container_width=True)

    # Constraint Summary
    if "constraint type" in df.columns:
        st.subheader("🔐 Constraint Types")
        fig_constraints = px.histogram(df, x="constraint type", title="Constraint Type Frequency")
        st.plotly_chart(fig_constraints, use_container_width=True)

    # Export analyzed data
    st.subheader("📤 Export Logic Analysis Report")
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    st.markdown(f"[⬇️ Download Logic Report (Excel)](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64})", unsafe_allow_html=True)
