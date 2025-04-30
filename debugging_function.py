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

    from openai import OpenAI

    client = OpenAI()

    # Step 1: Create an Assistant
    my_assistant = client.beta.assistants.create(
        model="gpt-4o",  # gpt-3.5-turbo-1106
        instructions="""
        You are Meena, an expert Java programming debugger.
        
        When provided with a Java file, analyze it for:
        1. Syntax errors
        2. Logic errors
        3. Runtime errors
        4. Design flaws
        5. Code style issues
        
        For each issue you find:
        - Clearly identify the line number or code block with the issue
        - Explain what the problem is in a clear, concise way
        - Explain why it's a problem (what errors or unexpected behavior it might cause)
        - Provide a specific solution to fix the issue
        - Explain why your solution works
        
        Present your findings in a structured, easy-to-follow format. Be thorough in your analysis but focus on the most significant issues first.
        
        If the code has multiple bugs, prioritize them in this order:
        1. Critical errors that prevent compilation
        2. Runtime errors that would crash the program
        3. Logic errors that would cause incorrect behavior
        4. Performance issues
        5. Style and best practice violations
        """,
        name="Java programming debugger",
        tools=[{"type": "file_search"}],
    )

    # Step 2: Create a Thread
    my_thread = client.beta.threads.create()

    # Step 3 Upload a file
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

    if uploaded_files:
        results = []

        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as fh:
                fh.write(uploaded_file.getbuffer())  # Save the file temporarily

            # Upload file
            my_file = client.files.create(
                file=open(uploaded_file.name, "rb"), purpose="assistants"
            )

            # Step 4: Add a separate Message for each file
            my_thread_message = client.beta.threads.messages.create(
                thread_id=my_thread.id,
                role="user",
                content=f"I need help debugging this Java file: {uploaded_file.name}. Please identify all errors and issues in the code and provide specific fixes for each problem.",
                attachments=[
                    {"file_id": my_file.id, "tools": [{"type": "file_search"}]}
                ],
            )

            # Run the assistant for each file separately
            run = client.beta.threads.runs.create_and_poll(
                thread_id=my_thread.id, assistant_id=my_assistant.id
            )

            # Get the response for the current file
            all_messages = client.beta.threads.messages.list(thread_id=my_thread.id)
            response = all_messages.data[0].content[0].text.value

            # Store results
            results.append(f"### **File: {uploaded_file.name}**\n{response}")

        # Display results for all files
        for result in results:
            st.write(result)
