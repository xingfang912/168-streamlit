# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

def strings():
    import streamlit as st

    st.title("Variable Practice")
    model = None
    model = st.radio(
    "Choose your AI assistance model",
    ["ChatGPT", "Llama3.2"],
    index=None)
    
    key_word = "string"
    
    @st.cache_data
    def load_data():
        import pandas as pd
        return pd.read_csv("data.csv")
    
    data = load_data()
    example = list(data[data["topic"] == key_word]['question'])[0]
    
    if model == "Llama3.2":
        from ollama import Client
        client = Client(
          host='http://localhost:11434',
          headers={'x-some-header': 'some-value'}
        )
        
        
        @st.cache_data
        def get_question(example):
            response = client.chat(model='llama3.2', messages=[
              {'role':'system','content':"You are an experienced Java programming instructor."},
              {'role': 'user','content': 
               f'Write a new problem, which practices on Java string methods, that is similar to the following example:\nDo not include any Java code in your writing.\nExample: {example}\nThe new problem:\n'}
            ])
            question = response['message']['content']
            return question    
        
        
        
        # if st.checkbox('Variable Declaration'):
            
        prompt = ""
        question = get_question(example)
        st.write(question)
        
        
        with st.form("my_form"):
            answer = st.text_area("Your answer here:")
            submit_button = st.form_submit_button(label='Submit')
        
            
            
        if submit_button:
            st.write("Submit successful!")
            
            prompt = f"""
                Your task is to determine if the student's solution \
                is correct or not.
                To solve the problem do the following:
                - First, work out your own solution to the problem including the final total. 
                - Then compare your solution to the student's solution \ 
                and evaluate if the student's solution is correct or not. 
                Don't decide if the student's solution is correct until 
                you have done the problem yourself.

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
                Is the student's solution the same as actual solution \
                just calculated:
                ```
                yes or no
                ```
                Student grade:
                ```
                correct or incorrect
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
            
            response = client.chat(model='llama3.2', messages=[
              {'role': 'user','content': prompt}
            ])
            
            
            final_answer = response['message']['content']    
            st.write(final_answer)
            st.cache_data.clear()
                    
    elif model == "ChatGPT":
        from openai import OpenAI

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        @st.cache_data
        def get_question2(example):
            completion = client.chat.completions.create(
                  model="gpt-3.5-turbo",
                  messages=[
                    {"role": "system", "content": "You are an experienced Java programming instructor."},
                    {"role": "user", "content": 
                     f'Write a new problem, which practices on Java string methods, that is similar to the following example:\nExample: {example}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nThe new problem:\n'}
                  ]
                )
            question = completion.choices[0].message.content
            if question[:4].lower() == "sure":
                question = question[question.find("\n")+1:]
            return question    
        
        
        prompt = ""
        question = get_question2(example)
        st.write(question)
        
        
        with st.form("my_form"):
            answer = st.text_area("Your answer here:")
            submit_button = st.form_submit_button(label='Submit')
        
            
            
        if submit_button:
            st.write("Submit successful!")
            
            prompt = f"""
                Your task is to determine if the student's solution \
                is correct or not.
                To solve the problem do the following:
                - First, work out your own solution to the problem including the final total. 
                - Second, do not include the following advanced content: array, file i/o, loops, if-else in your solution.
                - Then compare your solution to the student's solution \ 
                and evaluate if the student's solution is correct or not. 
                Don't decide if the student's solution is correct until 
                you have done the problem yourself.

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
                Is the student's solution the same as actual solution \
                just calculated:
                ```
                yes or no
                ```
                Student grade:
                ```
                correct or incorrect
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
              model="gpt-3.5-turbo",
              messages=[
                # {"role": "system", "content": "You are an experienced Java programmer."},
                {"role": "user", "content": prompt}
              ]
            )
            final_answer = completion.choices[0].message.content    
            st.write(final_answer)
            st.cache_data.clear()