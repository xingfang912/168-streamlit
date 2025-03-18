# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:48:04 2025

@author: xfang13
"""

def debugging_function():
    
    import streamlit as st
    
    
    st.write("# Welcome to the Debugging sesssion!")

    st.markdown(
        """
        Introducing Meena 👩‍🎓, our AI debugger!
        
        👩‍🎓 will help you clean up all the bugs you have in your program.
        
        👀Important: Please upload the file to the cwd.
        
        **👇 Upload your assignment file and click on the button to proceed!**

        
    """
    )
    
    left, middle, right = st.columns(3)
    
    if middle.button("Proceed!", use_container_width=True):
        
        import os
        # search the directory for files
        def find_files(root_dir, file_extension):
            """
            Walks through a directory and its subdirectories to find files with a specific extension.
        
            Args:
                root_dir (str): The path to the root directory to start searching from.
                file_extension (str): The file extension to search for (e.g., ".txt", ".pdf").
        
            Returns:
                list: A list of file paths that match the specified extension.
            """
            matching_files = []
            for dirpath, dirnames, filenames in os.walk(root_dir):
                for filename in filenames:
                    if filename.lower().endswith(file_extension.lower()):
                        matching_files.append(filename)
            return matching_files
        
        
        file_extension = "txt"# this should be java: assert file_extension == "java"
        file_list = find_files("./debugging_files/",file_extension=file_extension)
        
        file_name = st.radio("Select the file:",file_list,index=None)

        st.write("You selected:", file_name)

        #use Akhil's code below