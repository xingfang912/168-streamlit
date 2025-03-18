# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

import streamlit as st

def syntax():
    import streamlit as st
    
    
    st.write("# Overview of Java Syntax")
    st.sidebar.success("Java Syntax Page")
    
    st.markdown("""
Java syntax defines the rules for writing Java programs. Below is a general overview covering key aspects like naming conventions, Java statements, code blocks, the main class, and comments.

---

## **1. Naming Conventions in Java**
Java follows specific naming conventions to ensure code readability and consistency:  
- **Classes:** Start with an uppercase letter and use camel case. Example: `MyClass`
- **Methods & Variables:** Start with a lowercase letter and use camel case. Example: `calculateSum()`, `totalAmount`
- **Constants:** Use uppercase letters with underscores. Example: `PI_VALUE`
- **Packages:** Use all lowercase letters. Example: `com.example.project`

### **Example:**
```java
public class NamingConventionExample {
    static final double PI_VALUE = 3.14159; // Constant
    private int totalAmount; // Variable
    
    public void calculateSum(int num1, int num2) { // Method
        int sum = num1 + num2;
        System.out.println("Sum: " + sum);
    }
}
```

---

## **2. Java Statements**
A **statement** in Java is a complete unit of execution and ends with a semicolon (`;`).

### **Examples of Statements:**
```java
int x = 10;       // Variable declaration and initialization
System.out.println(x);  // Method call statement
x += 5;           // Assignment statement
```

---

## **3. Blocks of Code**
A **block of code** is a group of statements enclosed within `{}`. Blocks define the body of methods, loops, and conditional statements.

### **Example:**
```java
public class BlockExample {
    public static void main(String[] args) {
        int number = 5;
        
        if (number > 0) {  // Block inside if statement
            System.out.println("Positive number");
        }
    }
}
```

---

## **4. The Main Class and `main` Method**
Every Java application must have a **main class** with a `main` method, which serves as the entry point for execution.

### **Example:**
```java
public class MainClassExample {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
```

---

## **5. Comments in Java**
Comments help document the code and are ignored by the compiler.

### **Types of Comments:**
- **Single-line comment (`//`)**
- **Multi-line comment (`/* ... */`)**
- **Javadoc comment (`/** ... */`)**

### **Example:**
```java
public class CommentExample {
    public static void main(String[] args) {
        // This is a single-line comment
        System.out.println("Single-line comment example");

        /* 
         * This is a multi-line comment.
         * It can span multiple lines.
         */
        System.out.println("Multi-line comment example");

        /**
         * This is a Javadoc comment.
         * It is used for generating documentation.
         */
        System.out.println("Javadoc comment example");
    }
}
```

---

""")
    # st.write("\n\n#### Choose your pratice:")            
    # genre = st.radio(
    #         "",
    #         ["arithmetic precedence", "basic caculations"],
    #         index=None,
    #       )
    
    # cwd = "./arithmetic/"
    # if genre == "arithmetic precedence":
    #     arithmetic_general(cwd+"precedence/")
    # elif genre == "basic caculations":
    #     arithmetic_general(cwd+"calculation/")
        

# def arithmetic_general(cwd):
#     from openai import OpenAI

#     client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
#     # step 0. Creating a Vector Store
#     vector_store = client.beta.vector_stores.create(name="KnowledgeBase")
    
#     # step 1. put each string question into a word file.
    
#     # step 2. Prepare the files to upload to the vector store
#     import os
    
#     # @st.cache_data
#     def find_files(root_dir):
#         """
#         Walks through a directory and its subdirectories to find all file names.
    
#         Args:
#             root_dir (str): The path to the root directory to start searching from.
    
#         Returns:
#             list: A list of file names.
#         """
#         matching_files = []
#         for dirpath, dirnames, filenames in os.walk(root_dir):
#             for filename in filenames:
#                 matching_files.append(filename)
#         return matching_files
    
    
    
#     files = find_files(cwd)
    
#     # step 3. Randomly select a file to practice
#     @st.cache_data
#     def sampling_file():
#         import random
#         return random.sample(files,1)[0]
#     selected_file = sampling_file()
    
#     file_streams = [open(cwd+selected_file,"rb") for file_name in files]
    
#     # step 4. Uploading the files to vector store
#     # Use the upload and poll SDK helper to upload the files, add them to the vector store,
#     # and poll the status of the file batch for completion.
#     file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#         vector_store_id=vector_store.id, files=file_streams
#     )
                
#     #debugging
#     st.write(selected_file)
    
#     # step 5. Creating an assistant
#     assistant = client.beta.assistants.create(
#         name="Java programming instructor",
#         model="gpt-4o",
#         tools=[
#             {"type": "file_search"},
#         ],
#         # strict instructions to limit the assistant to answer only from the content of files not outside it
#         instructions="""You are an assistant that MUST ONLY answer questions based on the content of the attached files.
#     If the answer cannot be found in the attached files, respond with: 'I cannot answer this question as the information is not present in the provided files.'
    
#     When handling code-related queries:
#     1. NEVER share or reveal the actual Java implementation code from the files
#     2. Instead, you may:
#         - Provide high-level explanations of how the code works
#         - Share pseudocode that demonstrates the logic
#         - Describe the algorithm or approach using plain English
#         - Explain the design patterns or architectural concepts used
#         - Break down the solution into logical steps
#         - Discuss the input/output behavior without revealing implementation details
    
#     You can use the code interpreter to perform calculations, create visualizations, or analyze data when requested.
#     Do not use any external knowledge or make assumptions beyond what is explicitly stated in the files.
#     Always base your responses solely on the content found in the attached documents.""",
#         tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
#     )
    
#     # Now that the assistant is created and file is uploaded go to the next step
#     # step 6. Creating a thread and attaching the uploaded file to thread
#     thread = client.beta.threads.create()
    
#     @st.cache_data
#     def get_question():
    
#         # step 7. Add the user query to the exisiting thread, file is already attached
#         user_query = "Write a new problem that is similar to the example found in the file of {selected_file}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nPlease directly show the problem sentences without any foreword.\n\nThe new problem:\n'"
#         client.beta.threads.messages.create(
#         thread_id=thread.id, role="user", content=user_query
#         )
    
    
#         # step 8. run the query inside the thread using create and poll
#         run = client.beta.threads.runs.create_and_poll(
#             thread_id=thread.id, assistant_id=assistant.id
#         )
    
#         # step 9. get the latest response from the thread
#         response = client.beta.threads.messages.list(thread_id=thread.id)
    
    
#         # prompt = ""
#         # question = response.data[0].content[0].text.value.split("【")[0].strip()
#         text = response.data[0].content[0].text.value
#         if "blem:" in text:
#             text = response.data[0].content[0].text.value.split("blem:")[1]
#         if "【" in text:
#             text = response.data[0].content[0].text.value.split("【")[0].strip()
#         question = text
        
#         return question
    
#     question = get_question()
#     st.write(question)
    
    
#     with st.form("my_form"):
#         answer = st.text_area("Your answer here:")
#         submit_button = st.form_submit_button(label='Submit')
    
        
        
#     if submit_button:
#         st.write("Submit successful!")
        
#         prompt = f"""
#             Your task is to solve the problem.
            
#             Use the following format:
#             Question:
#             ```
#             question here
#             ```
#             Student's solution:
#             ```
#             student's solution here
#             ```
#             Actual solution:
#             ```
#             steps to work out the solution and your solution here
#             ```
#             Question:
#             ```
#             {question}
#             ``` 
#             Student's solution:
#             ```
#             {answer}
#             ```
#             Actual solution:
#             """
#         # st.write(prompt)
#         completion = client.chat.completions.create(
#           model="gpt-4o",
#           messages=[
#             # {"role": "system", "content": "You are an experienced Java programmer."},
#             {"role": "user", "content": prompt}
#           ]
#         )
#         final_answer = completion.choices[0].message.content    
#         st.write(final_answer)
#         st.cache_data.clear()