import streamlit as st
import os
import requests

def display():
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Video processing and encoding</h2>
        </div>
        """,
        unsafe_allow_html=True
    )