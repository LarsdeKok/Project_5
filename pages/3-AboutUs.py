import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="About us", page_icon="👥")

st.title('About us')

st.header('Project planning checker')
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

st.header("Our team")

col1, col2, col3, col4= st.columns(4)
with col1:
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div style="background-color: #6e6e6e; padding: 10px; border-style:solid; border-width:2px; border-color:#404040; border-radius:5px;text-align:center;">
            <h5 style="color: white;">Bram Bleumink</h5>
            <i class="fa fa-github" style="font-size:30px; color: black;"></i><br>
            <a href='https://github.com/Brimma' style="text-decoration:none; color: #003cff;"">Brimma</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div style="background-color: #6e6e6e; padding: 10px; border-style:solid; border-width:2px; border-color:#404040; border-radius:5px;text-align:center;">
            <h5 style="color: white;">Jinne Haan<br></h5>
            <i class="fa fa-github" style="font-size:30px; color: black;"></i><br>
            <a href='https://github.com/Jinne123' style="text-decoration:none; color: #003cff;"">Jinne123</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div style="background-color: #6e6e6e; padding: 10px; border-style:solid; border-width:2px; border-color:#404040; border-radius:5px;text-align:center;">
            <h5 style="color: white;">Lars de Kok<br></h5>
            <i class="fa fa-github" style="font-size:30px; color: black;"></i><br>
            <a href='https://github.com/LarsdeKok' style="text-decoration:none; color: #003cff;"">LarsdeKok</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div style="background-color: #6e6e6e; padding: 10px; border-style:solid; border-width:2px; border-color:#404040; border-radius:5px;text-align:center;">
            <h5 style="color: white;">Floor van der Venne</h5>
            <i class="fa fa-github" style="font-size:30px; color: black;"></i><br>
            <a href='https://github.com/FloorVanDerVenne' style="text-decoration:none; color: #003cff;">FloorVanDerVenne</a>
        </div>
        """, 
        unsafe_allow_html=True
    )