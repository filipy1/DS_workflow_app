import streamlit as st
import pandas as pd
import DS_workflow_helper_functions as hf


st.set_page_config(page_title="Welcome")

st.title('Welcome to the Data Science Workflow App :+1:')
st.markdown(f"""
        This app is designed with the intention of learning the basic data preprocessing workflow. \n
        Different pages on the app will perform different basic tasks in the data preprocessing workflow,
        keep in mind there are many ways to do the same things,
        we aim to introduce you to some basic approaches to each problem
        
        The app follows an easy to use interface, where every page is an app that produces a downloadable output that can be used in the other pages.""")

