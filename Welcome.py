import streamlit as st
import pandas as pd
import DS_workflow_helper_functions as hf


st.set_page_config(page_title="Welcome")

uploaded_file = st.file_uploader("Upload your input CSV/XLSX file", type=["csv", "xlsx"])
if uploaded_file is not None:
    
    if '.csv' in uploaded_file.name:
        df = pd.read_csv(uploaded_file)
    
    if '.xlsx' in uploaded_file.name:
        df = pd.read_excel(uploaded_file)

    try:
        ## We create a dataframe with the feature type and old vs new name, also we renamed the columns for consistency later on.
        idx_cols = st.multiselect('Select the index columns', df.columns)
        #manual_cate_cols = st.multiselect('Select the categorical columns', df.columns)
        df.set_index(idx_cols, inplace=True, drop=True)

        ## We encode the categorical columns
        int_enc_lst = st.multiselect('Select the categorical columns to be integer-encoded', df.columns)
        one_h_lst = st.multiselect('Select the categorical columns to be one-hot-encoded', df.columns)

        feature_type_df = hf.feature_type_extraction(df, index_columns=idx_cols, categorical_columns=int_enc_lst+one_h_lst) 
        st.write(feature_type_df)
        index_cols = feature_type_df['Index'].dropna().tolist()
        numeric_cols = feature_type_df['Numeric'].dropna().tolist()
        categorical_cols = feature_type_df['Categorical/Ordinal'].dropna().tolist()

        
        try:
            df = hf.categorical_column_encoding(df, categorical_columns=int_enc_lst, encoding_type='ordinal')
            df = hf.categorical_column_encoding(df, categorical_columns=one_h_lst, encoding_type='one-hot')
            st.write(df.head())

        except BaseException as e:
            st.error(e)

        # old_cols = df.columns.tolist()
        # st.write('Renaming the columns for consistency -')
        # df.columns = ['N' + str(i) if df.columns[i] in numeric_cols else 'C' + str(i) for i in range(0, len(df.columns))]

        # st.write(pd.DataFrame({'Old column names: ': old_cols, 'New column names: ': df.columns, 'Column types: ': df.dtypes.tolist()}))

        # st.write(df.describe(include='all'))

        # st.write(df.head())


        
    except ValueError as v:
        st.error(v)

    try:
        hf.download_button(df)
    except NameError as e:
        st.error(e)


