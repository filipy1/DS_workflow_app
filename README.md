# Basic data preprocessing app
### The aim of this application is to quicken the basic preprocessing of data before using it for ML/analysis purposes
Supported features - 
1. Categorical data encoding
2. Data imputation
3. Data scaling
4. Presents results at every step
5. Download-able CSV


#### Plans for the future
1. Outlier-detection using basic techniques
2. Basic visual analysis
3. Automatic linear regression between continueos variables
4. Automatic student's T-test between categories



### Explanation of streamlit 
Explanation of Streamlit multipage app usage
For this project I utilized the power of the [multi-page streamlit](https://docs.streamlit.io/library/get-started/multipage-apps) feature. The project is built such that there are 2 copies of each "streamlit app". One set of copies is in the "test_script" folder so you are able to run each app individually and change it as you see fit, the second set of copies is under the "pages" (specifically titled like this) folder and is meant to be the final product to be used in the multi-page app. Another thing to note is the "Welcome.py" file which is the landing page of the app.
