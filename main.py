# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:51:30 2024

@author: xfang13
"""

import streamlit as st
from syntax import *
from arithmetics_new import *
from strings_new import *
from control_structures import *
from arrays_and_file import *
from classes import *
from tutoring_function import *
from debugging_function import *

def intro():
    import streamlit as st

    st.write("# IT 168 Learning Platform :female-student: :male-student: :pencil:")
    # st.sidebar.success("Select a topic above.")

    st.markdown(
        """
        This platform is an open-source app framework built specifically for
        facilitating learning processes of students taking IT 168.
        
        

        **👈 Select a topic from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )



                
        
     


page_names_to_funcs = {
    "—": intro,
    "Java Syntax": syntax,
    "Arithmetics": arithmetics,
    "Strings":strings,
    "Control Structures":control_structures,
    "Arrays and File I/O":arrays_and_file,
    "Classes":classes,
    "Tutoring":tutoring_function,
    "Debugging":debugging_function,
}

demo_name = st.sidebar.selectbox("Learning module", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()


# page_names_to_funcs2 = {
#     "—": intro,
#     "Tutoring":tutoring_function,
# }

# demo_name2 = st.sidebar.selectbox("Tutoring module", page_names_to_funcs2.keys())
# page_names_to_funcs2[demo_name2]()

# page_names_to_funcs3 = {
#     "—": intro,
#     "Debugging":debugging_function,
# }

# demo_name3 = st.sidebar.selectbox("Debugging module", page_names_to_funcs3.keys())
# page_names_to_funcs3[demo_name3]()
    





