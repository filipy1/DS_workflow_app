import streamlit as st
import pandas as pd
import DS_workflow_helper_functions as hf


st.header(
    """
        Upload your data for an Outlier-Detection process - \n
        1. IQR Outlier detection
        2. Z-Score Outlier detection
        3. Threshold settings for each method
        4. KNN imputation
        5. The scikit-learn experimental IterativeImputer
        6. Summary statistics of the dataframe after the process
        7. Download the modified dataframe as a CSV file pages"""
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
        st.subheader("""Outlier detection/removal methods""")
        col1, col2 = st.columns(2)
        outlier_method = col1.selectbox(
            "Select the outlier detection/removal method", ["IQR", "Z-Score"]
        )

        columns_to_scale = col2.multiselect(
            "Remove outliers only by some columns. Taking into account which columns are compatible with which method",
            df.columns,
        )  ## We get the columns to scale

        if outlier_method == "IQR":

            range_low = col1.slider(
                "Select the lower bound of the range to consider outliers",
                min_value=0.0,
                max_value=1.0,
                value=0.25,
                key="IQR_slider_1",
            )
            range_high = col1.slider(
                "Select the upper bound of the range to consider outliers",
                min_value=0.0,
                max_value=1.0,
                value=0.75,
                key="IQR_slider_2",
            )

            threshold = col2.slider(
                "Select minimum number of columns required to be outliers",
                min_value=0,
                max_value=len(df.columns),
                key="IQR_slider_3",
            )

            df_no_outliers, outliers_df = hf.basic_outlier_detection(
                df,
                columns=list(columns_to_scale),
                method="IQR",
                quantile_range=(range_low, range_high),
                threshold=threshold,
            )

        if outlier_method == "Z-Score":

            z_score_threshold = col1.slider(
                "How many standard deviations away from the mean to consider outliers",
                min_value=1,
                max_value=10,
                value=3,
                key="Z_slider_1",
            )

            threshold = col2.slider(
                "Select minimum number of columns required to be outliers",
                min_value=1,
                max_value=len(df.columns),
                key="IQR_slider_3",
            )

            df_no_outliers, outliers_df = hf.basic_outlier_detection(
                df,
                columns=list(columns_to_scale),
                method="Z-Score",
                threshold=threshold,
                z_score_threshold=z_score_threshold,
            )

        col3, col4 = st.columns(2)

        col3.write("Datafarme after outlier removal")
        col3.write(df_no_outliers)
        col3.write(df_no_outliers.describe())

        col4.write("Outliers dataframe")
        col4.write(outliers_df)
        col4.write(outliers_df.describe())
    ## We catch the errors and present them to the user
    except BaseException as e:
        st.error("Error - file is unsuitable for the process")

    try:
        ## We download the dataframe as a CSV file
        col5, col6 = st.columns(2)
        hf.csv_download_button(
            df_no_outliers, "Download the dataframe after outlier removal", col5
        )
        hf.csv_download_button(outliers_df, "Download the outliers dataframe", col6)
    except NameError as e:
        st.error("Error - dataframe is unsuitable for the download")
