import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer
import scipy.stats as stats
import pingouin as pg


## Basic encodoing functions
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
    try:
        feature_type_df.columns = ["Index", "Numeric", "Categorical/Ordinal"]
    except:
        feature_type_df.columns = ["Numeric", "Categorical/Ordinal"]
    feature_type_df.fillna(np.nan, inplace=True)

    return feature_type_df.fillna(np.nan)


def categorical_column_encoding(df, categorical_columns=[], encoding_type="ordinal"):
    """This function takes the dataframe and a column of categorical data and returns the df with the encoded column."""

    if encoding_type == "ordinal":
        enc = OrdinalEncoder()
        enc.fit(df.loc[:, categorical_columns])
        df[categorical_columns] = enc.transform(df.loc[:, categorical_columns])

        return df

    if encoding_type == "one-hot":
        df = pd.get_dummies(
            df, columns=categorical_columns, prefix=categorical_columns, drop_first=True
        )

        return df
    else:

        return df


## Data download
# @st.cache_data
def csv_download_button(
    df, text="Enter the name of the dataframe to be saved as: ", col=None
):

    if col:
        file_name = col.text_input(text, "dataframe", key=f"{col}-text-input")
        col.download_button(
            data=df.to_csv(),
            label="Download the dataframe as a CSV file",
            file_name=file_name + ".csv",
            key=f"{col}-download-button",
        )

    else:
        file_name = st.text_input(text, "dataframe")
        st.download_button(
            data=df.to_csv(),
            label="Download the dataframe as a CSV file",
            file_name=file_name + ".csv",
        )


### Imputation functions
def imputation(
    df,
    imputation_type="mean",
    columns=[],
    knn_k=5,
    initial_strategy="mean",
    n_nearest_features=None,
    imp_order="ascending",
):
    """This function takes the dataframe and a column of categorical data and returns the df with the encoded column."""

    if imputation_type in ["mean", "median", "most frequent"]:
        if imputation_type == "most frequent":
            imputation_type = "most_frequent"
        imputer = SimpleImputer(strategy=imputation_type)
        imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
        df.loc[:, columns] = imputed.loc[:, columns]

        return df

    if imputation_type == "knn":
        imputer = KNNImputer(n_neighbors=knn_k)
        df.loc[:, columns] = imputer.fit_transform(df.loc[:, columns])

        return df

    if imputation_type == "iter":
        iter_imp = IterativeImputer(
            initial_strategy=initial_strategy,
            n_nearest_features=n_nearest_features,
            random_state=42,
            imputation_order=imp_order,
        )
        imputed = iter_imp.fit_transform(df)
        df = pd.DataFrame(imputed, columns=df.columns).set_index(df.index)

        return df
    else:

        return df


### Scaling functions
def scaling(df, sclaing_type="min-max", columns=[], range=(0, 1)):
    """This function takes the dataframe and a column of categorical data and returns the df with the encoded column."""

    if columns == []:
        columns = df.columns

    if sclaing_type == "min-max":  ## min-max scaling with flexible range
        df_std = (df.loc[:, columns] - df.loc[:, columns].min(axis=0)) / (
            df.loc[:, columns].max(axis=0) - df.loc[:, columns].min(axis=0)
        )
        df_scaled = df_std * (range[1] - range[0]) + range[0]
        df.loc[:, columns] = df_scaled

        return df

    if sclaing_type == "z-score":  ## z-score normalization
        df.loc[:, columns] = (df.loc[:, columns] - df.loc[:, columns].mean()) / df.loc[
            :, columns
        ].std()

        return df

    if sclaing_type == "max-abs":  ## max-abs scaling
        df.loc[:, columns] = df.loc[:, columns] / df.loc[:, columns].abs().max()

        return df

    if sclaing_type == "robust":  ## robust scaling using IQR
        df.loc[:, columns] = (df.loc[:, columns] - df.loc[:, columns].median()) / (
            df.loc[:, columns].quantile(0.75) - df.loc[:, columns].quantile(0.25)
        )

        return df

    else:
        return df


### Outlier detection functions


def apply_func_checking_IQR_threshold(row, threshold=3, IQR_dict={}):
    """This is a helper function for pandas apply function to check if the value is an outlier."""

    if IQR_dict == {}:
        raise ValueError("No columns provided")

    outlier_col_count = 0
    for key in IQR_dict.keys():
        if row[key] < IQR_dict[key][0] or row[key] > IQR_dict[key][1]:
            outlier_col_count += 1

        if outlier_col_count >= threshold:
            row["Outlier"] = 1
            return row

    return row


def apply_func_checking_Z_threshold(row, threshold=1, z_score_threshold=3):
    """This is a helper function for pandas apply function to check if the value is an outlier."""

    outlier_counter = 0
    for i in row.index:
        if row[i] >= z_score_threshold or row[i] <= -z_score_threshold:
            outlier_counter += 1

    if outlier_counter >= threshold:
        row["Outlier"] = 1
        return row
    return row


##Threshold is the number of columns that need to be outliers for the row to be considered an outlier
def basic_outlier_detection(
    df,
    columns=[],
    method="Z-Score",
    iqr_threshold=1.5,
    z_score_threshold=3,
    threshold=1,
    quantile_range=(0.25, 0.75),
):
    """This function aims to detect outliers in the dataframe and returns both a dataframe with the outliers removed and a dataframe with the outliers only."""

    if columns == []:
        columns = list(df.columns)

    if method == "IQR":

        df["Outlier"] = 0
        IQR_dict = {}

        for col in columns:
            IQR = df[col].quantile(quantile_range[1]) - df[col].quantile(
                quantile_range[0]
            )
            lower_bound = df[col].quantile(quantile_range[0]) - (iqr_threshold * IQR)
            upper_bound = df[col].quantile(quantile_range[1]) + (iqr_threshold * IQR)
            IQR_dict[col] = (lower_bound, upper_bound)

        df = df.apply(
            apply_func_checking_IQR_threshold, axis=1, args=(threshold, IQR_dict)
        )
        df_outliers = df.loc[df["Outlier"] == 1]
        df_no_outliers = df.loc[df["Outlier"] == 0]

        df_outliers.drop(columns=["Outlier"], inplace=True)
        df_no_outliers.drop(columns=["Outlier"], inplace=True)

        return df_no_outliers, df_outliers

    if method == "Z-Score":

        df["Outlier"] = 0

        for col in columns:
            df[col] = (df[col] - df[col].mean()) / df[col].std()

        df = df.apply(
            apply_func_checking_Z_threshold, axis=1, args=(threshold, z_score_threshold)
        )

        df_outliers = df.loc[df["Outlier"] == 1]
        df_no_outliers = df.loc[df["Outlier"] == 0]

        df_outliers.drop(columns=["Outlier"], inplace=True)
        df_no_outliers.drop(columns=["Outlier"], inplace=True)

        return df_no_outliers, df_outliers

    else:
        return df


### Statistical tests functions


def t_tests(
    test_df,
    paired=False,
    alpha=0.05,
    alternative="two-sided",
    correction=False,
    pairwise=False,
):
    """Function to be used for t-tests. If pairwise is set to True, then the function will perform pairwise t-tests for all columns in the dataframe."""
    if pairwise == False:
        t_test_results = pg.ttest(
            test_df.iloc[:, 0],
            test_df.iloc[:, 1],
            paired=paired,
            correction=correction,
            alternative=alternative,
        )
        return t_test_results

    if pairwise == True:

        t_test_results = pg.ptests(
            test_df, paired=paired, decimals=3, stars=False, padjust="bonf"
        )
        return t_test_results


def non_parametric_tests(test_df, alternative="two-sided", test="Mann-Whitney"):
    """Function to be used for non-parametric tests. Currently supports Mann-Whitney and Wilcoxon tests."""
    
    if test == "Mann-Whitney":
        test_results = pg.mwu(
            test_df.iloc[:, 0], test_df.iloc[:, 1], alternative=alternative
        )
        return test_results

    if test == "Wilcoxon":
        test_results = pg.wilcoxon(
            test_df.iloc[:, 0], test_df.iloc[:, 1], alternative=alternative
        )
        return test_results
