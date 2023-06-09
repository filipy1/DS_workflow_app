import streamlit as st
import pandas as pd
import DS_workflow_helper_functions as hf


st.header(
    """
        Initial Data Processing Application  \n
        Features - \n
        1. Choosing index column\s
        2. Categorical column encoding
        3. Feature type extraction and presentation
        4. Top 5 rows of the dataframe
        5. Summary statistics of the dataframe
        6. Download the modified dataframe as a CSV file that can be used in the next pages"""
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
        ## We create a dataframe with the feature type and old vs new name, also we renamed the columns for consistency later on.
        idx_cols = st.multiselect("Select the index columns", df.columns)
        if idx_cols == []:
            idx_col = pd.Series(df.index, name="index")
            df.set_index(idx_col, inplace=True)
            df.reset_index(inplace=True)
        else:
            df.set_index(idx_cols, inplace=True, drop=True)
        
        ## We encode the categorical columns
        cat_lst = st.multiselect(
            "Select the categorical columns",
            df.columns,
            default=list(df.select_dtypes(include=["object", "datetime", "timedelta"])),
        )

        feature_type_df = hf.feature_type_extraction(
            df, index_columns=idx_cols, categorical_columns=cat_lst
        )
        st.write(feature_type_df)

        col1, col2 = st.columns(2)
        int_enc_lst = col1.multiselect(
            "Select the categorical columns to be integer-encoded", cat_lst
        )
        one_h_lst = col2.multiselect(
            "Select the categorical columns to be one-hot-encoded", cat_lst
        )
        try:
            index_cols = feature_type_df["Index"].dropna().tolist()
        except:
            pass 
        
        numeric_cols = feature_type_df["Numeric"].dropna().tolist()
        categorical_cols = feature_type_df["Categorical/Ordinal"].dropna().tolist()

        try:
            ## We encode the categorical columns and present the dataframe
            df = hf.categorical_column_encoding(
                df, categorical_columns=int_enc_lst, encoding_type="ordinal"
            )
            df = hf.categorical_column_encoding(
                df, categorical_columns=one_h_lst, encoding_type="one-hot"
            )
            st.write(df.head())
            st.write(df.describe(include="all"))

        except BaseException as e:
            st.write(df.head())
            st.write(df.describe(include="all"))

    ## We catch the errors and present them to the user
    except ValueError as v:
        v
        st.error(v)

    try:
        ## We download the dataframe as a CSV file
        hf.csv_download_button(df)
    except NameError as e:
        st.error(e)
