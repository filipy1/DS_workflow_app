import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import DS_workflow_helper_functions as hf


st.header("""
        Upload your data to perform a Student's T-test - \n
        1. Optional pairwise T-test on the whole dataframe
        2. Paired/Unpaired T-test on 2 columns
        3. Displaying results as a table \n
        
        Assumptions of the T-test: \n
        * The mean of the data is normally distributed \n
        * The data is approximately normally distributed \n
        * Equal sample sizes and variance between groups being compared  \n
        """)


t_test_results = pd.DataFrame()

st.subheader("Upload your data")

uploaded_file = st.file_uploader(
    "Upload your input CSV/XLSX file", type=["csv", "xlsx"]
)

if uploaded_file is not None:  ## If the user has uploaded a file

    ## We read the file and create a dataframe based on the file type
    if ".csv" in uploaded_file.name:
        df = pd.read_csv(uploaded_file)

    if ".xlsx" in uploaded_file.name:
        df = pd.read_excel(uploaded_file)

    try:
        idx_cols = st.multiselect("Select the index columns", df.columns)
        df.set_index(idx_cols, inplace=True, drop=True)
        ## present the dataframe
        st.subheader(
            """Presenting top 5 rows and summary statistics of the dataframe"""
        )
        col1, col2 = st.columns(2)
        col1.write(df.head())
        col2.write(df.describe(include="all"))

        ## Outlier detection/removal methods
        st.subheader("T-tests")
        
        col3, col4 = st.columns(2)
        col3.write("T-test selection")
        
        pairwise = col3.radio("Pairwise T-test on whole data-frame?", ["Yes", "No"])

        if pairwise == 'No': ## If the user wants to perform a T-test on the whole dataframe
            alpha = st.number_input("Select the significance level", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
            t_type = col3.radio("Select the type of T-test", ["Unpaired", "Paired"])

            if t_type == "Paired":
                paired = True
            else:
                paired = False

            test_cols = col4.multiselect("Select 2 columns to be compared", df.columns, max_selections=2)
            test_df = df.loc[:, test_cols]  
            if len(test_cols) < 2:
                st.error(f"{t_type} T-test can only be performed on 2 columns")

            try:
                t_test_results = hf.t_tests(test_df, paired=paired, pairwise=False, alpha=alpha)
                st.subheader("T-test results")
                st.write(t_test_results)

                col_1_hist = px.histogram(data_frame=df, x=test_cols[0], height=250)
                col_2_hist = px.histogram(data_frame=df, x=test_cols[1], height=250)


                st.subheader("Histograms of the 2 columns")
                st.plotly_chart(col_1_hist, use_container_width=True, )
                st.plotly_chart(col_2_hist)
            except IndexError as e:
                pass

        
        if pairwise == 'Yes': ## If the user wants to perform a pairwise T-test on the whole dataframe

            t_type = col3.radio("Select the type of T-test", ["Unpaired", "Paired"])

            if t_type == "Paired":
                paired = True
            else:
                paired = False

            test_cols = col4.multiselect("Select columns to be compared", df.columns)

            try:
                t_test_results = hf.t_tests(df.loc[:, test_cols], paired=paired, pairwise=True)
                st.subheader("T-test results")
                st.write("The top triangle is the P values, the bottom triangle is the T values for each pair of columns")
                st.write(t_test_results)
            except ValueError as e:
                st.error("Please select at least 2 columns to be compared")

    ## We catch the errors and present them to the user
    except ValueError as v:
        st.error(v)

    try:
        ## We download the dataframe as a CSV file
        hf.csv_download_button(t_test_results, "Download the T-test results as a CSV file")
    except NameError as e:  
        st.error(e)
