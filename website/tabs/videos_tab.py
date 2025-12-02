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
    st.image(BBB, "Big Buck Bunny movie video")

    