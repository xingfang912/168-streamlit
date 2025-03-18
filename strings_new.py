# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

def strings():
    import streamlit as st

    # st.title("String Practice")
    model = "ChatGPT"
    key_word = "string"
    cwd = "./"+key_word+"/"
    
    st.write("# Strings in Java")
    st.markdown(
        """
In Java, a **string** is a sequence of characters and is represented by the `String` class, which is part of the `java.lang` package. Unlike primitive data types, strings in Java are **objects**.

#### **1. String Creation**
Strings can be created in two main ways:  
- **Using string literals:**  
  ```java
  String str1 = "Hello";
  ```
  Strings created this way are stored in the **string pool** for memory optimization.
  
- **Using the `new` keyword:**  
  ```java
  String str2 = new String("Hello");
  ```
  This forces the creation of a new object in the heap memory.

#### **2. String Immutability**
Strings in Java are **immutable**, meaning once a string object is created, it cannot be modified. Any modification (concatenation, replacement, etc.) creates a new string object.

#### **3. Common String Operations**
Java provides many built-in methods to manipulate strings:

- **Concatenation:**
  ```java
  String fullName = "John" + " Doe";  // Using + operator
  String fullName2 = "John".concat(" Doe");  // Using concat()
  ```

- **Finding Length:**
  ```java
  int len = "Hello".length();
  ```

- **Accessing Characters:**
  ```java
  char ch = "Hello".charAt(1); // 'e'
  ```

- **Substring Extraction:**
  ```java
  String sub = "Hello".substring(1, 4); // "ell"
  ```

- **Comparison:**
  ```java
  boolean isEqual = "hello".equals("Hello"); // false
  boolean isEqualIgnoreCase = "hello".equalsIgnoreCase("Hello"); // true
  ```

- **Searching for a Character or Substring:**
  ```java
  int index = "Hello".indexOf('e');  // 1
  ```


- **Splitting a String:**
  ```java
  String[] words = "Java,Python,C++".split(",");
  ```

- **Converting to Upper or Lower Case:**
  ```java
  String upper = "hello".toUpperCase(); // "HELLO"
  String lower = "HELLO".toLowerCase(); // "hello"
  ```

  ```

#### **4. String Formatting**
Java provides the `String.format()` method for formatted output.
```java
String formatted = String.format("Name: %s, Age: %d", "Alice", 25);
```


 """
    )
    st.write("\n\n#### Choose your pratice:")
    genre = st.radio(
            "",
            ["string methods", "output formatting"],
            index=None,
          )
    # if genre == "arithmetic precedence":
    #     arithmetic_precedence()
    
    
    if model == "ChatGPT" and genre is not None:
        from openai import OpenAI

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # step 0. Creating a Vector Store
        vector_store = client.beta.vector_stores.create(name="KnowledgeBase")
        
        # step 1. put each string question into a word file.
        
        # step 2. Prepare the files to upload to the vector store
        import os
        
        # @st.cache_data
        def find_files(root_dir):
            """
            Walks through a directory and its subdirectories to find all file names.
        
            Args:
                root_dir (str): The path to the root directory to start searching from.
        
            Returns:
                list: A list of file names.
            """
            matching_files = []
            for dirpath, dirnames, filenames in os.walk(root_dir):
                for filename in filenames:
                    matching_files.append(filename)
            return matching_files
        
        if genre == "string methods":
            cwd += "methods/"
        elif genre == "output formatting":
            cwd += "formatting/"
        
        files = find_files(cwd)
        
        # step 3. Randomly select a file to practice
        @st.cache_data
        def sampling_file():
            import random
            return random.sample(files,1)[0]
        selected_file = sampling_file()
        
        file_streams = [open(cwd+selected_file,"rb") for file_name in files]
        
        # step 4. Uploading the files to vector store
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )
                
        
        #debugging
        st.write(selected_file)
        
        # step 5. Creating an assistant
        assistant = client.beta.assistants.create(
            name="Java programming instructor",
            model="gpt-4o",
            tools=[
                {"type": "code_interpreter"},
                {"type": "file_search"},
            ],
            # strict instructions to limit the assistant to answer only from the content of files not outside it
            instructions="""You are an assistant that MUST ONLY answer questions based on the content of the attached files.
        If the answer cannot be found in the attached files, respond with: 'I cannot answer this question as the information is not present in the provided files.'
        
        When handling code-related queries:
        1. NEVER share or reveal the actual Java implementation code from the files
        2. Instead, you may:
            - Provide high-level explanations of how the code works
            - Share pseudocode that demonstrates the logic
            - Describe the algorithm or approach using plain English
            - Explain the design patterns or architectural concepts used
            - Break down the solution into logical steps
            - Discuss the input/output behavior without revealing implementation details
        
        You can use the code interpreter to perform calculations, create visualizations, or analyze data when requested.
        Do not use any external knowledge or make assumptions beyond what is explicitly stated in the files.
        Always base your responses solely on the content found in the attached documents.""",
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
        
        # Now that the assistant is created and file is uploaded go to the next step
        # step 6. Creating a thread and attaching the uploaded file to thread
        thread = client.beta.threads.create()
        
        @st.cache_data
        def get_question():
        
            # step 7. Add the user query to the exisiting thread, file is already attached
            user_query = "Write a new problem that is similar to the example found in the file of {selected_file}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nThe new problem:\n'"
            client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_query
            )
        
        
            # step 8. run the query inside the thread using create and poll
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=assistant.id
            )
        
            # step 9. get the latest response from the thread
            response = client.beta.threads.messages.list(thread_id=thread.id)
        
        
            # prompt = ""
            # question = response.data[0].content[0].text.value.split("【")[0].strip()
            question = response.data[0].content[0].text.value
            
            return question
        
        question = get_question()
        st.write(question)
        
        
        with st.form("my_form"):
            answer = st.text_area("Your answer here:")
            submit_button = st.form_submit_button(label='Submit')
        
            
            
        if submit_button:
            st.write("Submit successful!")
            
            prompt = f"""
                Your task is to solve the problem.
                
                Use the following format:
                Question:
                ```
                question here
                ```
                Student's solution:
                ```
                student's solution here
                ```
                Actual solution:
                ```
                steps to work out the solution and your solution here
                ```
                Question:
                ```
                {question}
                ``` 
                Student's solution:
                ```
                {answer}
                ```
                Actual solution:
                """
            # st.write(prompt)
            completion = client.chat.completions.create(
              model="gpt-4o",
              messages=[
                # {"role": "system", "content": "You are an experienced Java programmer."},
                {"role": "user", "content": prompt}
              ]
            )
            final_answer = completion.choices[0].message.content    
            st.write(final_answer)
            st.cache_data.clear()