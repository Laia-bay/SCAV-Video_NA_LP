import streamlit as st

def display():
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Welcome to the Home page</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

     # Info abt what the web is: 
    st.text("")            #to leave a space between welcome and info
    st.write(
    """

    #### **Image & Video Processing**

    This website has been done by Nahia Anaut and Laia Pertusa. 
    It has been done using Streamlit.
    
    #### *Features:*
    This application contains 2 essential features

    - **Image processing & encoding:** A tab dedicated to different image transformations that you can do to encode them. 

    - **Video processing & encoding:** A tab dedicated to different video transformations that you can do to encode them.
    

    #### *How does it work:*
    The effective running of this webpage works due to:
    - A github repository that contains all image examples and all the necessary files with the different image and video functions.

    - A docker container that ignores the innecesary files and runs on fastAPI and ffmpeg, which allow us to do most of the image and video transformations.

    
    #### *Authors' notes*
    Hello Javi, we hope that you find this website interesting, easy to use, and most of all, that works correctly. 
    We have done our best during all the practices, and we feel like we learnt a lot. 
    That is all, enjoy!
    """
    )