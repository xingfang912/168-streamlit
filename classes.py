# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

import streamlit as st

def classes():
    import streamlit as st
    
    
    st.write("# Java Classes (Public Non-Main Classes)")
    st.sidebar.success("Java Classes Page")
    
    st.markdown("""
In Java, a **class** is a blueprint for creating objects. A **public non-main class** does not contain the `main` method but can be used by other classes in the program. These classes typically define attributes (variables) and behaviors (methods) that describe objects.

---

## **1. Instance Variables**  
Instance variables belong to **individual objects** of a class. Each object has its own copy of these variables.

### **Example:**
```java
public class Car {
    String brand;  // Instance variable
    int speed;     // Instance variable

    public Car(String brand, int speed) {
        this.brand = brand;
        this.speed = speed;
    }

    public void display() {
        System.out.println("Brand: " + brand + ", Speed: " + speed);
    }
}
```
Here, `brand` and `speed` are **instance variables**. Every object of `Car` has a separate `brand` and `speed`.

---

## **2. Class Constants (`final` variables)**  
Constants are declared using `final` and **cannot be changed** once assigned.

### **Example:**
```java
public class MathConstants {
    public static final double PI = 3.14159; // Class constant

    public void displayPI() {
        System.out.println("Value of PI: " + PI);
    }
}
```
- `PI` is a **class constant** because it is declared `final` and `static`.
- Constants should be written in **UPPERCASE**.

---

## **3. Static Variables (Class Variables)**  
A **static variable** is shared by all instances of a class. It belongs to the **class itself** rather than any specific object.

### **Example:**
```java
public class Employee {
    private static int employeeCount = 0; // Static variable

    public Employee() {
        employeeCount++; // Increment count when an object is created
    }

    public static int getEmployeeCount() {
        return employeeCount; // Static method accessing a static variable
    }
}
```
- `employeeCount` is a **static variable** because it is shared across all objects of `Employee`.
- `getEmployeeCount()` is a **static method** that returns the value of `employeeCount`.

---

## **4. Public Methods**  
Public methods allow **external access** to perform operations or get object details.

### **Example:**
```java
public class Person {
    private String name; // Private instance variable

    public Person(String name) {
        this.name = name;
    }

    public void greet() {  // Public method
        System.out.println("Hello, my name is " + name);
    }
}
```
- `greet()` is a **public method**, meaning other classes can call it.

---

## **5. Encapsulation (Using Getters and Setters)**  
Encapsulation means **hiding data** and allowing controlled access through **getter and setter** methods.

### **Example:**
```java
public class BankAccount {
    private double balance; // Private variable (cannot be accessed directly)

    public BankAccount(double balance) {
        this.balance = balance;
    }

    // Getter method
    public double getBalance() {
        return balance;
    }

    // Setter method
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
}
```
- `balance` is **private**, meaning it **cannot be accessed directly**.
- `getBalance()` is a **getter** method that retrieves the balance.
- `deposit()` is a **setter** method that allows **controlled modification** of `balance`.

---

## **Summary Table**
| Feature | Description | Example Variable/Method |
|---------|------------|------------------------|
| **Instance Variable** | Belongs to an object | `String brand` |
| **Class Constant** | `final` value that does not change | `public static final double PI` |
| **Static Variable** | Shared across all instances | `private static int employeeCount` |
| **Public Method** | Accessible from outside the class | `public void greet()` |
| **Encapsulation** | Restricts direct access to variables | `getBalance()`, `deposit(amount)` |

---

## **Conclusion**  
Java classes define object behavior using **instance variables, class constants, static variables, and public methods**. **Encapsulation** helps maintain data integrity by restricting direct access. Mastering these concepts is crucial for writing well-structured Java programs!

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