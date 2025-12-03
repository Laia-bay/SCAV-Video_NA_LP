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
    input_video = col1.file_uploader("Upload a video to get its information:","mp4")

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
            st.warning("Information not available. Please select one of the showed options.")
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
        
    st.subheader("Processing & encoding section")
    st.write("")
    st.write("This is the processing & encoding section")

    input_video2 = st.file_uploader("Upload a video to process it:","mp4")

    if input_video2:
        video_name2 = input_video2.name
        video_bytes2 = input_video2.read()
    
    processing_options = ["---", "Resize video", "Create BBB container", "Macroblocks Motion Vectors", "Convert video format"]
    processing = st.selectbox("Select the processing transformation that you want to apply:", processing_options)

    if processing == ("Resize video"):
        width = st.number_input("Select the desired width:", 1, 1279)
        height = st.number_input("Select the desired height:", 1, 719)

    elif processing == ("Create BBB container"):
        audios = []
        AAC = st.checkbox("AAC audio:")
        MP3 = st.checkbox("MP3 audio:")
        AC3 = st.checkbox("AC3 audio:")
    
    elif processing == ("Convert video format"):
        videos = []
        VP8 = st.checkbox("VP8 video:")
        VP9 = st.checkbox("VP9 video:")
        h265 = st.checkbox("h265 video:")
        AV1 = st.checkbox("AV1 video:")



    if (st.button("Process video")):
        if (processing == "---"):
            st.warning("Please select a processing option.")
            return
        elif (processing == "Resize video"):
            if width != 0 and height != 0:
                endpoint2 = "/resize_video"
            else: 
                st.warning("Please write the desired width and height.")
                return
            
        elif (processing == "Create BBB container"):
            endpoint2 = "/create_BBB_container"
        elif (processing == "Macroblocks Motion Vectors"):
            endpoint2 = "/macroblocks_motion_vectors"
        elif (processing == "Convert video format"):
            endpoint2 = "/convert_video_format"
        else:
            st.warning("Processing option not available. Please select one of the showed options.")
            return
        
        with st.spinner("Processing..."):
            files = {"file": (video_name2, video_bytes2, "video/mp4")}
            
            if processing == "Resize video":
                data = {"width":  width, "height": height}
                response = requests.post(API_URL + endpoint2, files=files, data=data)
            elif processing == "Create BBB container":
                data = {"AAC_audio": AAC, "MP3_audio": MP3, "AC3_audio": AC3}
                response = requests.post(API_URL + endpoint2, files=files, data=data)
            elif processing == "Convert video format":
                data = {"VP8": VP8, "VP9": VP9, "h265": h265, "AV1": AV1}
                response = requests.post(API_URL + endpoint2, files=files, data=data)
            
            else:
                response = requests.post(API_URL + endpoint2, files=files)

        if processing == "Resize video":
            st.write("Resized video has been saved on 'video_results' folder.")
        if processing == "Create BBB container":
            if AAC == True:
                audios.append("AAC")
            if MP3 == True:
                audios.append("MP3")
            if AC3 == True:
                audios.append("AC3")
            st.write(f"BBB video with audios {audios} has been saved on 'video_results' folder.")
        if processing == "Convert video format":
            if VP8 == True:
                videos.append("VP8")
            if VP9 == True:
                videos.append("VP9")
            if h265 == True:
                videos.append("h265")
            if AV1 == True:
                videos.append("AV1")
            st.write(f"Video with codecs {videos} has been saved on 'video_results' folder.")
        if processing == "Macroblocks Motion Vectors":
            st.write("Video with macroblocks motion vectors has been saved on 'video_results' folder.")

        if response.status_code != 200:
            st.error("Error processing video.")
            st.text(response.text)
            return

