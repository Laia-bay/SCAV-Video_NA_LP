import streamlit as st
import os
import requests
import io
from PIL import Image

API_URL = "http://localhost:8000"
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

    # Get list of images in folder
    images_list = [os.path.join(IMAGES_PATH,f) for f in os.listdir(IMAGES_PATH)]

    col1.subheader("List of images in folder")
    col1.write(images_list)

    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = images_list[st.session_state.counter]
    
    def showPhoto():
        st.session_state.selected_image = images_list[st.session_state.counter]
        col2.image(st.session_state.selected_image,caption=st.session_state.selected_image)
        col1.write(f"Index: {st.session_state.counter}")
        
        ## Increments the counter to get next photo
        st.session_state.counter += 1
        if st.session_state.counter >= len(images_list):
            st.session_state.counter = 0

 
    next_button = col1.button("Show next pic ⏭",on_click=showPhoto)


    input_image = st.file_uploader("Upload an image:","jpg")
    
    ## 2 different ways of uploading images (in case the user wants another image)
    if input_image:
        image_name = input_image.name
        image_bytes = input_image.read()
    else:
        image_name = os.path.basename(st.session_state.selected_image)
        with open(st.session_state.selected_image, "rb") as f:
            image_bytes = f.read()
    
    
    processing_options = ["---","Read image in Serpentine pattern", "Convert image to grayscale", "Chroma Subsampling"]
    transformation = st.selectbox("Select the processing that you want to do",processing_options, 0)

    if transformation == "Chroma Subsampling":
        CS_options = ["---", "4:4:4","4:2:2", "4:1:1", "4:2:0"]
        string_vals = str(000)
        values = st.selectbox("Select the chroma subsampling that you want to apply:", CS_options)
        if values == "4:4:4":
            string_vals = str(444)
        elif values == "4:2:2":
            string_vals = str(422)
        elif values == "4:1:1":
            string_vals = str(411)
        elif values == "4:2:0":
            string_vals == str(420)
        else:
            string_vals = str(000)
        

    if(st.button("Process image")):
            
        if transformation == "---":
            st.warning("Please select a processing operation")
            return
        elif transformation == "Read image in Serpentine pattern":
            endpoint = "/serpentine"
        elif transformation == "Convert image to grayscale":
            endpoint = "/B&W"
        elif transformation == "Chroma Subsampling":
            if string_vals == "000":
                st.warning("Please select a correct chroma subsampling option")
                return
            else:
                endpoint = "/chroma_subsampling"
        else: 
            st.warning("Processing option not available. Please select one of the showed options.")
            return
        
        with st.spinner("Processing..."):
            files = {"file": (image_name, image_bytes, "image/jpg")}
            if transformation == "Chroma Subsampling":
                data = {"subsampling":  string_vals}
                response = requests.post(API_URL + endpoint, files=files, data=data)
            else:
                response = requests.post(API_URL + endpoint, files=files)

        if response.status_code != 200:
            st.error("Error processing image.")
            st.text(response.text)
            return
        
        img = Image.open(io.BytesIO(response.content))
        col2.image(img, caption=f"Processed result: {transformation}")
        st.write("Image saved in 'image_results' folder.")

