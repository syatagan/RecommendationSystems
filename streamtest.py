import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Rules Based Classificiation on Customers Dataset",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)

image = Image.open('yetenekler.png')

st.image(image, width=200)

st.title('ARL RECOMMENDATION PROJECT')

st.markdown(
    """
    This app is to create new level-based customer definitions using some features of a game company's customers. 
    It creates segments according to these new customer definitions and estimates how much the new customers can earn according to these segments.

    After entering the Country, OS, Gender and Age information in the new customer information section on the left, you can perform estimation and segmentation operations by pressing the "Save" button.

    * **Pyton libraries:** pandas, streamlit, PIL, matplotlib, plotly.express
    * **Data source:** persona.csv

    ***
    """
)