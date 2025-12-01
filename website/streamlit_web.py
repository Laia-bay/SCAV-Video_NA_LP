import streamlit as st
import numpy as np
import os
from PIL import Image
import requests
from fastapi import HTTPException

from tabs import home_tab, images_tab, videos_tab

IMAGES_PATH = "images"
IMAGES_RESULTS_PATH = "image_results"


st.set_page_config(page_title="SCAV final project NA&LP", layout="wide")
st.title("SCAV final project NA&LP")

tab1, tab2, tab3 = st.tabs(["Home","Images","Videos"])

with tab1:
    home_tab.display()
    
with tab2: 
    images_tab.display()
    
with tab3:
    videos_tab.display()