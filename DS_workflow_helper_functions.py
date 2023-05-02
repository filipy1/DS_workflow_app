import streamlit as st
import pandas as pd
import numpy as np


def feature_type_extraction(df, index_columns=[0], categorical_columns=[]):
    """This function takes the uploaded file and returns a dictionary with the feature type as the key and the list of column names as the value."""

    # Get the list of column names for each feature type

    indexes = pd.DataFrame(index_columns)
    numer = pd.DataFrame(list(df.select_dtypes(include=["float64", "int64"]).columns))
    numer.replace(index_columns + categorical_columns, np.nan, inplace=True)
    cate = pd.DataFrame(list(df.select_dtypes(include=["object"]).columns) + categorical_columns)

    feature_type_df = pd.concat((indexes, numer, cate), axis=1, ignore_index=True)
    feature_type_df.columns = ["Index", "Numeric", "Categorical"]
    feature_type_df.fillna(np.nan, inplace=True)

    return feature_type_df


def download_button(df):
    file_name = st.text_input('Enter the name of the dataframe to be saved as: ', 'dataframe')
    if st.button("Download the datafream as a CSV file"):
        df.to_csv(file_name + '.csv')
        st.success('Dataframe saved as a CSV file.')