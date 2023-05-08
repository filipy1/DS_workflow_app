import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import io 

def feature_type_extraction(df, index_columns=[0], categorical_columns=[]):
    """This function takes the uploaded file and returns a dictionary with the feature type as the key and the list of column names as the value."""

    # Get the list of column names for each feature type
    
    indexes = pd.DataFrame(index_columns)
    numer = pd.DataFrame(list(df.select_dtypes(include=["float64", "int64"]).columns))
    numer.replace(index_columns + categorical_columns, np.nan, inplace=True)
    cate = pd.DataFrame(categorical_columns).drop_duplicates()
    if len(categorical_columns) == 0:
        cate = pd.DataFrame([np.nan for i in range(len(numer))])

    feature_type_df = pd.concat((indexes, numer, cate), axis=1, ignore_index=True)
    feature_type_df.columns = ["Index", "Numeric", "Categorical/Ordinal"]
    feature_type_df.fillna(np.nan, inplace=True)

    return feature_type_df

#@st.cache_data
def csv_download_button(df):
    file_name = st.text_input('Enter the name of the dataframe to be saved as: ', 'dataframe')
    st.download_button(data=df.to_csv(), label='Download the dataframe as a CSV file', file_name=file_name + '.csv')


def categorical_column_encoding(df, categorical_columns=[], encoding_type='ordinal'):
    """This function takes the dataframe and a column of categorical data and returns the df with the encoded column."""

    if encoding_type == 'ordinal':
        enc = OrdinalEncoder()
        enc.fit(df.loc[:, categorical_columns])
        df[categorical_columns] = enc.transform(df.loc[:, categorical_columns])

        return df
    
    if encoding_type == 'one-hot':
        df = pd.get_dummies(df, columns=categorical_columns, prefix=categorical_columns, drop_first=True)

        return df
    else:

        return df
    

def imputation(df, imputation_type='mean', columns=[], knn_k=5, initial_strategy='mean', n_nearest_features=None, imp_order='ascending'):
    """This function takes the dataframe and a column of categorical data and returns the df with the encoded column."""

    if imputation_type == 'mean':
        df.loc[:, columns] = df.loc[:, columns].fillna(df[columns].mean())

        return df
    
    if imputation_type == 'median':
        df.loc[:, columns] = df.loc[:, columns].fillna(df[columns].median())

        return df
    
    if imputation_type == 'mode':
        df.loc[:, columns] = df.loc[:, columns].fillna(list(df[columns].mode())[0])

        return df
    
    if imputation_type == 'knn':
        imputer = KNNImputer(n_neighbors=knn_k)
        df.loc[:, columns] = imputer.fit_transform(df.loc[:, columns])

        return df

    if imputation_type == 'iter':
        iter_imp = IterativeImputer(initial_strategy=initial_strategy, n_nearest_features=n_nearest_features, random_state=42, imputation_order=imp_order)
        imputed = iter_imp.fit_transform(df)
        df = pd.DataFrame(imputed, columns=df.columns)

        return df
    else:

        return df