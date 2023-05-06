import streamlit as st
import pandas as pd
import numpy as np
import DS_workflow_helper_functions as hf




st.subheader('Upload your data')

uploaded_file = st.file_uploader("Upload your input CSV/XLSX file", type=["csv", "xlsx"])

if uploaded_file is not None: ## If the user has uploaded a file
    
    ## We read the file and create a dataframe based on the file type
    if '.csv' in uploaded_file.name:
        df = pd.read_csv(uploaded_file)
    
    if '.xlsx' in uploaded_file.name:
        df = pd.read_excel(uploaded_file)


    try:
        ## present the dataframe
        st.subheader("""Presenting top 5 rows and summary statistics of the dataframe""")
        col1, col2 = st.columns(2)
        col1.write(df.head())
        col2.write(df.describe(include='all'))

        col1, col2 = st.columns(2)
        simple_impute = col1.multiselect('Select the columns to be simple-imputed', df.columns)

        if len(simple_impute) > 0: 
            imp_type = col2.radio('Select the type of simple imputation', ['mean', 'median', 'mode'])
            df = hf.imputation(df, imputation_type=imp_type, columns=simple_impute)
            st.write(df.head())


        col3, col4 = st.columns(2)
        knn_impute = col3.multiselect('Select the columns to be knn imputed', [col for col in df.columns if col not in simple_impute])

        if len(knn_impute) > 0:
            knn_k = col4.slider('Select the number of nearest neighbors', min_value=1, max_value=len(df.index), value=int(np.sqrt(len(df.index))), step=1)
            df = hf.imputation(df, imputation_type='knn', columns=knn_impute, knn_k=knn_k)
            st.write(df.head())

    except BaseException as e:
        st.error(e)

    
    try:
        ## We download the dataframe as a CSV file 
        hf.csv_download_button(df)
    except NameError as e:
        st.error(e)