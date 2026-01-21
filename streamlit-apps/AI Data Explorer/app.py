import streamlit as st
from core.loader import load_file
from core.eda import basic_eda
from core.visualizer import plot_numeric_distributions
from core.insights import generate_insights
from core.schema import infer_schema
from core.eda import smart_eda
from core.insights import correlation_matrix, detect_anomalies

st.title("AI Data Explorer")
st.markdown("""
Welcome to the AI Data Explorer! This application allows you to upload your datasets and perform exploratory data
analysis (EDA), generate insights, and visualize data with ease.
""")

# initialize session state flags
if "run_eda" not in st.session_state:
    st.session_state["run_eda"] = False
if "show_correlation" not in st.session_state:
    st.session_state["show_correlation"] = False

def set_run_eda():
    st.session_state["run_eda"] = True

def toggle_show_correlation():
    st.session_state["show_correlation"] = True

st.sidebar.title("Data Uploader & Options")
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV, Excel, JSON)", type=["csv", "xlsx", "parquet", "json"])
eda_level = st.sidebar.selectbox("Select EDA Level", ["Basic", "Smart"])
st.sidebar.button("Run EDA", on_click=set_run_eda)
generate_data_insights = st.sidebar.button("Generate Insights")
visualize_data = st.sidebar.button("Visualize Data")

if uploaded_file:
    df = load_file(uploaded_file)
    st.subheader("Dataset Summary")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    st.write(df.head())

    # check if file is uploaded, then infer schema. Next, if basic EDA is selected, run it. and change the
    # session state flag to indicate EDA has been run
    # and if smart EDA is selected, run it
    if st.session_state["run_eda"]:
        #st.subheader("Schema Inference")
        schema = infer_schema(df)

        if eda_level == "Basic":
            st.subheader("Basic EDA Results")
            eda_results = basic_eda(df)
            st.json(eda_results, expanded=False)
            
        elif eda_level == "Smart":
            st.subheader("Smart EDA Results")
            eda_results = smart_eda(df, schema=schema)
            st.json(eda_results, expanded=False)

        # Insights requires EDA results
        if generate_data_insights:
            if eda_results:
                st.subheader("Data Insights")
                insights = generate_insights(eda_results)
                st.write(insights)
            else:
                st.warning("Run EDA first (click 'Run EDA' in the sidebar).")
        else:
            st.warning("Click 'Generate Insights' to see insights based on EDA results.")
        

    # Show correlation matrix if the flag is set
    if st.session_state["show_correlation"]:
        st.subheader("Correlation Matrix")
        corr_matrix = correlation_matrix(df)
        st.write(corr_matrix)
        st.session_state["show_correlation"] = False

    # Button to toggle correlation matrix display
    if st.sidebar.button("Show Correlation Matrix"):
        toggle_show_correlation()

    # Anomaly detection button
    if st.sidebar.button("Detect Anomalies"):
        st.subheader("Anomaly Detection")
        anomalies = detect_anomalies(df)
        if anomalies.empty:
            st.write("No anomalies detected.")
        else:
            st.write("Anomalies detected:")
            st.write(anomalies)

    # Visualizations require a loaded dataframe
    if visualize_data:
        st.subheader("Data Visualizations")
        plots = plot_numeric_distributions(df)
        for fig in plots:
            st.pyplot(fig)