# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

import streamlit as st

def arithmetics():
    import streamlit as st
    
    
    st.write("# Arithmetic Basics in Java")
    st.sidebar.success("Java Arithmetic Page")
    
    st.markdown("""
In Java, arithmetic operations are performed using **operators** on **primitive data types**. Below is a general overview of how arithmetic works in Java.

---

## **1. Primitive Data Types in Java**  
Java provides several primitive data types for storing numeric values:

| Data Type | Size | Range | Example |
|-----------|------|-------------|---------|
| `byte`    | 1 byte  | -128 to 127  | `byte a = 10;`  |
| `short`   | 2 bytes | -32,768 to 32,767 | `short b = 1000;` |
| `int`     | 4 bytes | -2³¹ to 2³¹-1  | `int c = 100000;` |
| `long`    | 8 bytes | -2⁶³ to 2⁶³-1  | `long d = 100000L;` |
| `float`   | 4 bytes | ~7 decimal digits  | `float e = 10.5f;` |
| `double`  | 8 bytes | ~15 decimal digits | `double f = 10.56789;` |

### **Syntax for Declaring and Initializing Variables**  
```java
int num1 = 10;   // Integer
double num2 = 5.5;  // Floating-point number
float num3 = 3.14f; // 'f' suffix is required for float
long num4 = 100000L; // 'L' suffix is required for long
```

---

## **2. Arithmetic Operators in Java**  
Java provides basic arithmetic operators:

| Operator | Meaning | Example |
|----------|---------|---------|
| `+`  | Addition | `10 + 5` → `15` |
| `-`  | Subtraction | `10 - 5` → `5` |
| `*`  | Multiplication | `10 * 5` → `50` |
| `/`  | Division | `10 / 5` → `2` |
| `%`  | Modulus (Remainder) | `10 % 3` → `1` |

### **Example: Arithmetic Operations**
```java
public class ArithmeticExample {
    public static void main(String[] args) {
        int a = 10, b = 5;
        System.out.println("Addition: " + (a + b));        // 15
        System.out.println("Subtraction: " + (a - b));     // 5
        System.out.println("Multiplication: " + (a * b));  // 50
        System.out.println("Division: " + (a / b));        // 2
        System.out.println("Modulus: " + (a % b));         // 0
    }
}
```

---

## **3. Arithmetic Precedence and Associativity**  
Operators follow a specific **precedence order**, similar to standard mathematical rules.

### **Precedence Table (Highest to Lowest)**
| Precedence | Operators |
|------------|-----------|
| 1 (Highest) | `()` (Parentheses) |
| 2 | `*`, `/`, `%` (Multiplication, Division, Modulus) |
| 3 | `+`, `-` (Addition, Subtraction) |

- **Operators** with the same precedence follow **left-to-right associativity**.  
- **Parentheses `()`** can be used to **override** precedence.

### **Example: Arithmetic Precedence**
```java
public class PrecedenceExample {
    public static void main(String[] args) {
        int result1 = 10 + 5 * 2;  // Multiplication first, then addition
        int result2 = (10 + 5) * 2; // Parentheses change order

        System.out.println("Without parentheses: " + result1); // 20
        System.out.println("With parentheses: " + result2); // 30
    }
}
```

### **Example: Left-to-Right Associativity**
```java
public class AssociativityExample {
    public static void main(String[] args) {
        int result = 20 / 5 * 2; // (20 / 5) * 2 → 4 * 2 → 8
        System.out.println("Left-to-right associativity: " + result);
    }
}
```

---

### **4. Integer Division and Floating-Point Arithmetic**  
- When **both operands** are integers, **integer division** occurs.
- To get a **decimal result**, at least one operand must be a `double` or `float`.

```java
public class DivisionExample {
    public static void main(String[] args) {
        int intDiv = 10 / 3;       // Integer division: 3
        double doubleDiv = 10.0 / 3; // Floating-point division: 3.3333

        System.out.println("Integer Division: " + intDiv);
        System.out.println("Floating-Point Division: " + doubleDiv);
    }
}
```

---

### **5. Increment (`++`) and Decrement (`--`) Operators**
These operators increase or decrease a value by **1**.

- **Postfix (`x++`, `x--`)**: Returns the value **before** increment/decrement.
- **Prefix (`++x`, `--x`)**: Returns the value **after** increment/decrement.

```java
public class IncrementExample {
    public static void main(String[] args) {
        int x = 5;
        System.out.println(x++); // Prints 5, then x becomes 6
        System.out.println(++x); // Increments first, then prints 7
    }
}
```

---


                """)
    st.write("\n\n#### Choose your pratice:")            
    genre = st.radio(
            "",
            ["arithmetic precedence", "basic caculations"],
            index=None,
          )
    
    cwd = "./arithmetic/"
    if genre == "arithmetic precedence":
        arithmetic_general(cwd+"precedence/")
    elif genre == "basic caculations":
        arithmetic_general(cwd+"calculation/")
        

def arithmetic_general(cwd):
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
        user_query = "Write a new problem that is similar to the example found in the file of {selected_file}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nPlease directly show the problem sentences without any foreword.\n\nThe new problem:\n'"
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
        text = response.data[0].content[0].text.value
        if "blem:" in text:
            text = response.data[0].content[0].text.value.split("blem:")[1]
        if "【" in text:
            text = response.data[0].content[0].text.value.split("【")[0].strip()
        question = text
        
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

# def arithmetic_precedence():
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
    
#     cwd = "./arithmetic/precedence/"
    
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
#         user_query = "Write a new problem that is similar to the example found in the file of {selected_file}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nThe new problem:\n'"
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
    



# def basic_calculations():
#     import streamlit as st

#     st.title("Variable Calculations")
#     model = None
#     model = st.radio(
#     "Choose your AI assistance model",
#     ["ChatGPT", "Llama3.2"],
#     index=None)
    
#     key_word = "arithmetic"
    
#     @st.cache_data
#     def load_data():
#         import pandas as pd
#         return pd.read_csv("data.csv")
    
#     data = load_data()
#     example = data[data["topic"] == key_word]['question'][1]
    
#     if model == "Llama3.2":
#         from ollama import Client
#         client = Client(
#           host='http://localhost:11434',
#           headers={'x-some-header': 'some-value'}
#         )
        
        
#         @st.cache_data
#         def get_question(example):
#             response = client.chat(model='llama3.2', messages=[
#               {'role':'system','content':"You are an experienced Java programming instructor. Please directly show the problem sentences without any foreword."},
#               {'role': 'user','content': 
#                f'Write a new problem that is similar to the following example:\nDo not include any Java code in your writing.\nExample: {example}\nThe new problem:\n'}
#             ])
#             question = response['message']['content']
#             return question    
        
        
        
#         # if st.checkbox('Variable Declaration'):
            
#         prompt = ""
#         question = get_question(example)
#         st.write(question)
        
        
#         with st.form("my_form"):
#             answer = st.text_area("Your answer here:")
#             submit_button = st.form_submit_button(label='Submit')
        
            
            
#         if submit_button:
#             st.write("Submit successful!")
            
#             prompt = f"""
#                 Your task is to determine if the student's solution \
#                 is correct or not.
#                 To solve the problem do the following:
#                 - First, work out your own solution to the problem including the final total. 
#                 - Then compare your solution to the student's solution \ 
#                 and evaluate if the student's solution is correct or not. 
#                 Don't decide if the student's solution is correct until 
#                 you have done the problem yourself.

#                 Use the following format:
#                 Question:
#                 ```
#                 question here
#                 ```
#                 Student's solution:
#                 ```
#                 student's solution here
#                 ```
#                 Actual solution:
#                 ```
#                 steps to work out the solution and your solution here
#                 ```
#                 Is the student's solution the same as actual solution \
#                 just calculated:
#                 ```
#                 yes or no
#                 ```
#                 Student grade:
#                 ```
#                 correct or incorrect
#                 ```

#                 Question:
#                 ```
#                 {question}
#                 ``` 
#                 Student's solution:
#                 ```
#                 {answer}
#                 ```
#                 Actual solution:
#                 """
#             # st.write(prompt)
            
#             response = client.chat(model='llama3.2', messages=[
#               {'role': 'user','content': prompt}
#             ])
            
            
#             final_answer = response['message']['content']    
#             st.write(final_answer)
#             st.cache_data.clear()
                    
#     elif model == "ChatGPT":
#         from openai import OpenAI

#         client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
#         @st.cache_data
#         def get_question2(example):
#             completion = client.chat.completions.create(
#                   model="gpt-3.5-turbo",
#                   messages=[
#                     {"role": "system", "content": "You are an experienced Java programming instructor."},
#                     {"role": "user", "content": 
#                      f'Write a new problem that is similar to the following example:\nExample: {example}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nThe new problem:\n'}
#                   ]
#                 )
#             question = completion.choices[0].message.content
#             if question[:4].lower() == "sure":
#                 question = question[question.find("\n")+1:]
#             return question    
        
        
#         prompt = ""
#         question = get_question2(example)
#         st.write(question)
        
        
#         with st.form("my_form"):
#             answer = st.text_area("Your answer here:")
#             submit_button = st.form_submit_button(label='Submit')
        
            
            
#         if submit_button:
#             st.write("Submit successful!")
            
#             prompt = f"""
#                 Your task is to determine if the student's solution \
#                 is correct or not.
#                 To solve the problem do the following:
#                 - First, work out your own solution to the problem including the final total. 
#                 - Then compare your solution to the student's solution \ 
#                 and evaluate if the student's solution is correct or not. 
#                 Don't decide if the student's solution is correct until 
#                 you have done the problem yourself.

#                 Use the following format:
#                 Question:
#                 ```
#                 question here
#                 ```
#                 Student's solution:
#                 ```
#                 student's solution here
#                 ```
#                 Actual solution:
#                 ```
#                 steps to work out the solution and your solution here
#                 ```
#                 Is the student's solution the same as actual solution \
#                 just calculated:
#                 ```
#                 yes or no
#                 ```
#                 Student grade:
#                 ```
#                 correct or incorrect
#                 ```

#                 Question:
#                 ```
#                 {question}
#                 ``` 
#                 Student's solution:
#                 ```
#                 {answer}
#                 ```
#                 Actual solution:
#                 """
#             # st.write(prompt)
#             completion = client.chat.completions.create(
#               model="gpt-3.5-turbo",
#               messages=[
#                 # {"role": "system", "content": "You are an experienced Java programmer."},
#                 {"role": "user", "content": prompt}
#               ]
#             )
#             final_answer = completion.choices[0].message.content    
#             st.write(final_answer)
#             st.cache_data.clear()


# page_names_to_funcs = {
#     "—": arithmetics,
#     "Arthmetic precendence":arithmetic_precedence,
#     "Calculation with variables": variable_calculations,
    
# }

# demo_name = st.sidebar.selectbox("Choose a practice", page_names_to_funcs.keys())
# page_names_to_funcs[demo_name]()