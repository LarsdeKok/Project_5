import streamlit as st
import pandas as pd
import numpy as np

from ToolLars import aantal_bussen


# pages = {
#     "Planning checker": [
#         st.Page("Ui.py", title="Planning checker"),
#         st.Page("tool.py", title="Manage your account"),
#     ],
#     "Resources": [
#         st.Page("tool.py", title="Learn about us"),
#         st.Page("tool.py", title="Try it out"),
#     ],
# }

# pg = st.navigation(pages)
# pg.run()


st.title('test2')

st.write('test')



dienstregeling = st.file_uploader('Dienstregeling', type=['xlsx'],accept_multiple_files=False)
omloop = st.file_uploader('Omloopplanning', type=['xlsx'],accept_multiple_files=False)

df1 = None
inputfields = []

def filesUploaded():
    df1=pd.read_excel(omloop)
    st.write(df1)
    aantallen = aantal_bussen(df1)
   
    st.write(aantallen)
    generate_values(aantallen)

def generate_values(aantallen):
    for i in aantallen:
        inputfields.append(st.number_input(f"Insert the SOH for bus {i}."))

if st.button("Submit"):
    if dienstregeling is not None and omloop is not None:
        st.write("Why hello there")
        filesUploaded()
    else:
        st.write("Please add the files first.")



# for i in aantallen:
#     inputfields.append(st.number_input(f"Insert the SOH for bus {i}."))
