# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:48:04 2025

@author: xfang13
"""

def tutoring_function():
    
    import streamlit as st
    
    
    st.write("# Welcome to the Tutoring sesssion!")

    st.markdown(
        """
        Introducing Leena 👩‍🎓, our AI tutor!
        
        👩‍🎓 will help you form up a step-by-step solution for your assignment.
        
        👀Important: 👩‍🎓 will not include any Java code in the solution.
        
        **👇 Upload your assignment file below and get started!**

        
    """
    )

    from openai import OpenAI
    
    client = OpenAI()
    
    # Step 1: Create an Assistant
    my_assistant = client.beta.assistants.create(
        model="gpt-4o", #gpt-3.5-turbo-1106
        instructions="You are a Java programming tutor. Your knowledge base is a homework assignment that students is having problems about.",
        name="Java programming tutor",
        tools=[{"type": "file_search"}]
    )
    
    # Step 2: Create a Thread
    my_thread = client.beta.threads.create()
    
    
    # Step 3 Upload a file
    
    # @st.cache_data
    # def file_upload():
    #     return st.file_uploader("Choose a file")
    uploaded_file = st.file_uploader("Choose a file")
    
    
    if uploaded_file is not None:
        # st.write(uploaded_file.name)
        # Step 4: Upload a File with an "assistants" purpose, the file contains the
        # homework assignment from a student
        my_file = client.files.create(
          file=open(uploaded_file.name,"rb"),
          purpose='assistants'
        )
        
        # Step 4: Add a Message to a Thread
        my_thread_message = client.beta.threads.messages.create(
          thread_id=my_thread.id,
          role="user",
          content="I am having issues in figuring out the step-by-step solution to the homework problem that I attached. Please show me the step-by-step solution without showing me any actual Java code.",
          attachments=[{"file_id":my_file.id, "tools":[{"type": "file_search"}]}]
        )
        
        
        run = client.beta.threads.runs.create_and_poll(
                thread_id=my_thread.id, assistant_id=my_assistant.id
        )
        
        all_messages = client.beta.threads.messages.list(
                    thread_id=my_thread.id
                )
        
        
        # st.write(f"User: {my_thread_message.content[0].text.value}")
        st.write(f"Assistant: {all_messages.data[0].content[0].text.value}")
    