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
    st.write("In this video processing & encoding page most transformations will be done on the Big Buck Bunny (BBB) video." \
    "However, we recommend that for converting the video and doing the encoder ladder you select another video that has less duration. " \
    "Otherwise, the processing will take very long.")
    col1,col2 = st.columns(2)
    info_options = ["---", "5 points of information", "Inspect mp4 tracks", "YUV histogram"]
    information = col1.selectbox("Select the information of the video that you want", info_options)
    
    
    if (col1.button("Show information")):
        if information == "---":
            st.warning("Please select the information that you want to know")
            return
        elif information == "5 points of information":
            endpoint = "/video_info"
        elif information == "Inspect mp4 tracks":
            endpoint = "/inspect_mp4_tracks"
        elif information == "YUV histogram":
            endpoint = "/yuv_histogram"
        else:
            st.warning("Please select an existing information that you want to know")
            return
        

    col2.image(BBB, "Big Buck Bunny movie video")



    processing_options = ["---", "Resize video", "Create BBB container", "Macroblocks Motion Vectors", ""]

