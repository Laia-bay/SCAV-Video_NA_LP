import streamlit as st
import os
import requests

BBB = "images/BBB.jpg"
VIDEO_RESULTS_PATH = "video_results"
API_URL = "http://localhost:8000"

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
    st.write("In this video processing & encoding page most transformations will be done on the Big Buck Bunny (BBB) video.")
    st.write("However, we recommend that for converting the video and doing the encoder ladder you select another video that has less duration." \
    "Otherwise, the processing will take very long.")
    st.write("")
    
    col1,col2 = st.columns(2)
    input_video = col1.file_uploader("Upload an image:","mp4")

    if input_video:
        video_name = input_video.name
        video_bytes = input_video.read()
    
    col2.image(BBB, "Big Buck Bunny movie video")
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
        
        with st.spinner("Loading..."):
            files = {"file": (video_name, video_bytes, "video/mp4")}
            response = requests.post(API_URL + endpoint, files=files)

        if response.status_code != 200:
            st.error("Error processing video.")
            st.text(response.text)
            return
       
        if information == "5 points of information" or information == "Inspect mp4 tracks":
            data = response.json()
            col1.write("Results")
            col1.json(data)
            
        elif information == "YUV histogram":
            col1.write("YUV histogram video has been saved on 'video_results' folder.")
        
        else:
            col1.write("Something went wrong. Try again")
        



    processing_options = ["---", "Resize video", "Create BBB container", "Macroblocks Motion Vectors", ""]

