import streamlit as st
import pandas as pd
import plotly.express as px
import DS_workflow_helper_functions as hf


t_test_results = pd.DataFrame()


st.header(
    """
        Upload your data to perform a non-parametric test  \n
        1. Wilcoxon test for paired data
        2. Mann-Whitney test for unpaired data
        
        Assumptions of the tests: \n
        * The distributions of the 2 groups are similar \n
        
        """
)


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
        if idx_cols == []:
            idx_cols = pd.Series(df.index, name="index")
        df.set_index(idx_cols, inplace=True, drop=True)
        ## present the dataframe
        st.subheader(
            """Presenting top 5 rows and summary statistics of the dataframe"""
        )
        col1, col2 = st.columns(2)
        col1.write(df.head())
        col2.write(df.describe(include="all"))

        ## Outlier detection/removal methods
        st.subheader("Non-parametric tests")

        col3, col4 = st.columns(2)
        col3.write("Test selection")

        pairwise = col3.radio("Pairwise test on whole data-frame?", ["Yes", "No"]) ## Pairwise means 

        if pairwise == "No":

            t_type = col3.radio("Select the type of test", ["Mann-Whitney", "Wilcoxon"])

            test_cols = col4.multiselect(
                "Select 2 columns to be compared", df.columns, max_selections=2
            )
            test_df = df.loc[:, test_cols]
            if len(test_cols) < 2:
                st.error(f"{t_type} test can only be performed on 2 columns")

            try:
                t_test_results = hf.non_parametric_tests(test_df, test=t_type)
                st.subheader("Test results")
                st.write(t_test_results)

                col_1_hist = px.histogram(data_frame=df, x=test_cols[0], height=250)
                col_2_hist = px.histogram(data_frame=df, x=test_cols[1], height=250)

                st.subheader("Histograms of the 2 columns")
                st.plotly_chart(
                    col_1_hist,
                    use_container_width=True,
                )
                st.plotly_chart(col_2_hist)
            except IndexError as e:
                pass

        if pairwise == "Yes":

            st.error("Sorry but pairwise test not implemented yet")

    ## We catch the errors and present them to the user
    except ValueError as v:
        st.error(v)

    try:
        ## We download the dataframe as a CSV file
        hf.csv_download_button(
            t_test_results, "Download the test results as a CSV file"
        )
    except NameError as e:
        st.error(e)
