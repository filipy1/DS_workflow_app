import streamlit as st
import pandas as pd
import DS_workflow_helper_functions as hf




# st.header("""
#         Upload your data for a Normalization process that includes - \n
#         1. Dropping rows based on number of non-NA values
#         2. Dropping columns of your choosing
#         3. Several Simple imputation methods
#         4. KNN imputation
#         5. The scikit-learn experimental IterativeImputer
#         6. Summary statistics of the dataframe after the process
#         7. Download the modified dataframe as a CSV file that can be used in the next pages""") 



st.subheader('Upload your data')

uploaded_file = st.file_uploader("Upload your input CSV/XLSX file", type=["csv", "xlsx"])

if uploaded_file is not None: ## If the user has uploaded a file
    
    ## We read the file and create a dataframe based on the file type
    if '.csv' in uploaded_file.name:
        df = pd.read_csv(uploaded_file)
    
    if '.xlsx' in uploaded_file.name:
        df = pd.read_excel(uploaded_file)

    try:
        idx_cols = st.multiselect('Select the index columns', df.columns)
        df.set_index(idx_cols, inplace=True, drop=True)
        ## present the dataframe
        st.subheader("""Presenting top 5 rows and summary statistics of the dataframe""")
        col1, col2 = st.columns(2)
        col1.write(df.head())
        col2.write(df.describe(include='all'))

        ## Outlier detection/removal methods
        

        

    ## We catch the errors and present them to the user
    except ValueError as v:
        st.error(v)
    
    
    try:
        ## We download the dataframe as a CSV file 
        hf.csv_download_button(df)
    except NameError as e:
        st.error(e)

