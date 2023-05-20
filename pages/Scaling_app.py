import streamlit as st
import pandas as pd
import DS_workflow_helper_functions as hf


st.header(
    """
        Data Scaling Application \n
        Features - \n
        1. Min-Max
        2. Z-Score
        3. Max-Abs
        4. Robust
        5. Leaving the option for not scaling some columns"""
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
        df.set_index(idx_cols, inplace=True, drop=True)
        ## present the dataframe
        st.subheader(
            """Presenting top 5 rows and summary statistics of the dataframe"""
        )
        col1, col2 = st.columns(2)
        col1.write(df.head())
        col2.write(df.describe(include="all"))

        ## Sclaing the data frame
        st.subheader("""Scaling the dataframe""")
        col1, col2 = st.columns(2)
        scaling_type = col1.selectbox(
            "Select the scaling type", ["Min-Max", "Z-Score", "Max-Abs", "Robust"]
        )

        col2.write(
            "Leaving the option for not scaling some columns, this is unrecommended in most cases"
        )
        columns_to_scale = col2.multiselect(
            "Select the columns to scale", df.columns
        )  ## We get the columns to scale

        if scaling_type.lower() == "min-max":
            range_low = col1.slider(
                "Select the range for the scaled values",
                min_value=0,
                max_value=100,
                key="min-max_slider_1",
            )
            range_high = col1.slider(
                "Select the range for the scaled values",
                min_value=0,
                max_value=100,
                key="min-max_slider_2",
            )
            scaled_df = hf.scaling(
                df,
                scaling_type.lower(),
                columns_to_scale,
                range=(range_low, range_high),
            )
            st.write(scaled_df.head())

        elif columns_to_scale == []:
            scaled_df = hf.scaling(df, scaling_type.lower())
            st.write(scaled_df.head())

        else:
            scaled_df = hf.scaling(df, scaling_type.lower(), columns_to_scale)
            st.write(scaled_df.head())

    ## We catch the errors and present them to the user
    except ValueError as v:
        st.error(v)

    try:
        ## We download the dataframe as a CSV file
        hf.csv_download_button(df)
    except NameError as e:
        st.error(e)
