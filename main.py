import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define the URL for the data source
URL = ''

# Set Streamlit page configuration
st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide"
)

st.title("Arts Faculty Data Analysis")
st.markdown("---")
