# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

import streamlit as st

def arrays_and_file():
    import streamlit as st
    
    
    st.write("# Arrays and File I/O")
    st.sidebar.success("Arrays and File I/O Page")
    
    st.markdown("""
### **1. Arrays in Java**  
An **array** is a data structure used to store multiple values of the same type in a contiguous memory location. Java supports both **one-dimensional** and **multi-dimensional** arrays.

#### **Declaring and Initializing Arrays**  
```java
// Declare and initialize an integer array
int[] numbers = {1, 2, 3, 4, 5};

// Declare an array and allocate memory
String[] names = new String[3]; // Array of size 3
names[0] = "Alice";
names[1] = "Bob";
names[2] = "Charlie";
```

#### **Accessing Elements**  
```java
System.out.println(numbers[2]); // Output: 3
```

#### **Iterating Through Arrays Using Loops**  
```java
for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}
```
Using an enhanced for-loop:
```java
for (int num : numbers) {
    System.out.println(num);
}
```

#### **Multi-Dimensional Arrays**  
```java
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Accessing elements
System.out.println(matrix[1][2]); // Output: 6
```

---

### **2. File I/O in Java**  
Java provides classes in the `java.io` package to read from and write to files.

#### **Writing to a File** (`FileWriter` and `PrintWriter`)  
```java
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class FileWriteExample {
    public static void main(String[] args) {
        try {
            FileWriter fileWriter = new FileWriter("output.txt"); 
            PrintWriter printWriter = new PrintWriter(fileWriter);
            printWriter.println("Hello, this is a test file.");
            printWriter.println("Writing to a file in Java!");
            printWriter.close();
            System.out.println("File written successfully.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}
```
*Creates a file `output.txt` and writes text into it.*

#### **Reading from a File** (`Scanner` and `BufferedReader`)  
```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FileReadExample {
    public static void main(String[] args) {
        try {
            File file = new File("output.txt");
            Scanner scanner = new Scanner(file);
            
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                System.out.println(line);
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found.");
            e.printStackTrace();
        }
    }
}
```
*Opens `output.txt`, reads its content line by line, and prints it to the console.*

---

### **Summary**
| **Topic**             | **Example Used** |
|----------------------|-----------------|
| Declaring & Initializing Arrays | `int[] numbers = {1, 2, 3, 4, 5};` |
| Accessing Elements | `System.out.println(numbers[2]);` |
| Iterating Arrays | `for (int num : numbers) {}` |
| Multi-Dimensional Arrays | `int[][] matrix = {{1,2,3}, {4,5,6}};` |
| Writing to a File | `FileWriter` & `PrintWriter` |
| Reading from a File | `Scanner` & `File` |



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
        user_query = "Write a new problem that is similar to the example found in the file of {selected_file}\n\nPlease directly show the problem sentences without any foreword.\n\nThe new problem:\n'"
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