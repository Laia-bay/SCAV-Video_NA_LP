import streamlit as st
import os
import requests

IMAGES_PATH = "images"
def display():
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Image processing and encoding</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


    ## Display images in images folder
    col1,col2 = st.columns(2)

    if 'counter' not in st.session_state: 
        st.session_state.counter = 0

    def showPhoto(photo):
        col2.image(photo,caption=photo)
        col1.write(f"Index as a session_state attribute: {st.session_state.counter}")
        
        ## Increments the counter to get next photo
        st.session_state.counter += 1
        if st.session_state.counter >= len(images_list):
            st.session_state.counter = 0

    # Get list of images in folder
    images_list = [os.path.join(IMAGES_PATH,f) for f in os.listdir(IMAGES_PATH)]

    col1.subheader("List of images in folder")
    col1.write(images_list)

    # Select photo a send it to button
    photo = images_list[st.session_state.counter]
    show_btn = col1.button("Show next pic ⏭",on_click=showPhoto,args=([photo]))


    input_image = st.file_uploader("Upload an image:","jpg")

    processing_options = ["---","Read image in Serpentine pattern", "Convert image to grayscale"]
    st.selectbox("Select the processing that you want to do",processing_options, 0)

