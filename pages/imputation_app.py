import streamlit as st
import pandas as pd
import numpy as np
import DS_workflow_helper_functions as hf
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import io


st.header(
    """
        Data Imputation Application \n
        Features - \n
        1. Dropping rows based on number of non-NA values
        2. Dropping columns of your choosing
        3. Several Simple imputation methods
        4. KNN imputation
        5. The scikit-learn experimental IterativeImputer
        6. Summary statistics of the dataframe after the process
        7. Download the modified dataframe as a CSV file that can be used in the next pages"""
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

        ## Index column selection
        idx_cols = st.multiselect("Select the index columns", df.columns)
        df.set_index(idx_cols, inplace=True, drop=True)
        ## present the dataframe
        st.subheader(
            """Presenting top 5 rows and summary statistics of the dataframe"""
        )
        col1, col2 = st.columns(2)
        col1.write(df.head())
        col2.write(df.describe(include="all"))

        row_drop, col_drop = st.columns(2)
        drop_thresh = row_drop.slider(
            "Select how many non-NA values required for a row to be kept",
            min_value=0,
            max_value=len(df.columns),
            value=0,
            step=1,
        )
        df.dropna(axis=0, thresh=drop_thresh, inplace=True)

        st.write(len(df.index))
        col_drop_lst = col_drop.multiselect(
            "Select the columns to be dropped", df.columns
        )
        df.drop(col_drop_lst, axis=1, inplace=True)

        col1, col2 = st.columns(2)
        simple_impute = col1.multiselect(
            "Select the columns to be simple-imputed",
            [col for col in df.columns if col not in col_drop_lst],
        )

        if len(simple_impute) > 0:
            imp_type = col2.radio(
                "Select the type of simple imputation",
                ["mean", "median", "most frequent"],
            )
            df = hf.imputation(df, imputation_type=imp_type, columns=simple_impute)

        col3, col4 = st.columns(2)
        knn_impute = col3.multiselect(
            "Select the columns to be knn imputed",
            [col for col in df.columns if col not in simple_impute + col_drop_lst],
        )

        if len(knn_impute) > 0:
            knn_k = col4.slider(
                "Select the number of nearest neighbors",
                min_value=1,
                max_value=len(df.index),
                value=int(np.sqrt(len(df.index))),
                step=1,
            )
            df = hf.imputation(
                df, imputation_type="knn", columns=knn_impute, knn_k=knn_k
            )

        ## Iterative imputer using bayesian ridge regression, note the implementation is exprimental in sklearn.`
        col5, col6, col7, col8 = st.columns(4)
        iter_impute = col5.radio("Iter impute rest of the columns?", ["No", "Yes"])

        if iter_impute == "Yes":
            # n_nearest = col6.slider('Select the number of nearest feautres to use for imputation', min_value=1, max_value=len(df.columns), value=int(np.sqrt(len(df.columns))), step=1)
            init_strategy = col7.radio(
                "Select the initial imputation strategy",
                ["mean", "median", "most_frequent"],
            )
            imp_order = col8.radio(
                "Select the order of imputation", ["ascending", "descending", "random"]
            )
            df = hf.imputation(
                df,
                imputation_type="iter",
                columns=iter_impute,
                initial_strategy=init_strategy,
                imp_order=imp_order,
            )

        ## We present the dataframe
        st.subheader(
            """Presenting top 5 rows and summary statistics of the dataframe"""
        )
        col1, col2, col3 = st.columns(3)
        col1.write(df.head())
        col2.write(df.describe(include="all"))

        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()

        col3.text(s)
    except BaseException as e:
        st.error(e)

    try:
        ## We download the dataframe as a CSV file
        hf.csv_download_button(df)
    except NameError as e:
        st.error(e)
