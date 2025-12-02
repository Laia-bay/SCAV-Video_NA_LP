import streamlit as st
import os
import requests

BBB = "images/BBB.jpg"
def display():
    st.markdown(
        """
        <div style="text-align: center;">
            <h3>Video processing and encoding</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    st.write("In this video processing & encoding page all transformations will be done on the Big Buck Bunny (BBB) video.")
    col1,col2 = st.columns(2)
    info_options = ["---", "5 points of information", "Inspect mp4 tracks", "YUV histogram"]
    col1.selectbox("Select the information of the video that you want", info_options)
    col2.image(BBB, "Big Buck Bunny movie video")

    processing_options = ["---", "Resize video", "Create BBB container", "Macroblocks Motion Vectors"]

