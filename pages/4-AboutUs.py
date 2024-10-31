import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="About us", page_icon="👥")

st.title('About us')

st.header('The team')

st.write("""We are a team of four individuals—Lars, Jinne, Floor, and Bram—who came together for a school project. Lars serves as our chairman, guiding our discussions and ensuring we stay on track with our goals.
We are a team committed to delivering the best results possible. Currently, we are working on a project called PlanningChecker, which we will elaborate on in the following section.""")

st.header('Project PlanningChecker')
st.write("""PlanningChecker will check if your given bus planning is complete and correct.
        Whether you're new to this type of software or an experienced user, this tool will help you check and improve your planning. 
        With the transition to electric busses, bus scheduling has gotten more requirements. PlanningChecker makes sure that every bus schedule meets these new requirements.
        The tool checks if all of the given routes will be driven, if the charging time of a bus is more than 15 minutes and if the bus has an SOC-value (State of Charge-value) below the minimal value. 
        If the given bus planning and timetable don't meet the conditions, PlanningChecker will let you know where the conditions aren't met. This makes it easier for planners to quickly identify and correct potential issues and minimizing errors in the scheduling process.
""")
st.header("Meet the team")

col1, col2, col3, col4= st.columns(4)
with col1:
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div style="background-color: #6e6e6e; padding: 10px; border-style:solid; border-width:2px; border-color:#404040; border-radius:5px;text-align:center;">
            <h5 style="color: white;">Bram Bleumink</h5>
            <i class="fa fa-github" style="font-size:30px; color: black;"></i><br>
            <a href='https://github.com/Brimma' style="text-decoration:none; color: #003cff;"">See Github</a>
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
            <a href='https://github.com/Jinne123' style="text-decoration:none; color: #003cff;"">See Github</a>
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
            <a href='https://github.com/LarsdeKok' style="text-decoration:none; color: #003cff;"">See Github</a>
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
            <a href='https://github.com/FloorVanDerVenne' style="text-decoration:none; color: #003cff;">See Github</a>
        </div>
        """, 
        unsafe_allow_html=True
    )