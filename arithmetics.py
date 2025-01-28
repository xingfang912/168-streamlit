# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:55:57 2024

@author: xfang13
"""

import streamlit as st

def arithmetics():
    import streamlit as st
    st.write("# Welcome to Streamlit! 👋")
    genre = st.radio(
            "Choose your practice",
            ["arithmetic precedence", "varible caculations"],
            index=None,
          )
    if genre == "arithmetic precedence":
        arithmetic_precedence()


def arithmetic_precedence():
    from openai import OpenAI

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    @st.cache_data
    def get_question2():
        completion = client.chat.completions.create(
              # model="gpt-3.5-turbo",
              model="gpt-4o",
              messages=[
                {"role": "system", "content": "You are an experienced Java programming instructor."},
                {"role": "user", "content": 
                f'Give me a question on java arithmetic precedence. The calculation may involve multiple variables together with layers of parathesis. But do not show me the answer.'}
              ]
            )
        question = completion.choices[0].message.content
        if question[:4].lower() == "sure":
            question = question[question.find("\n")+1:]
        return question    
    
    
    prompt = ""
    question = get_question2()
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
          model="gpt-3.5-turbo",
          messages=[
            # {"role": "system", "content": "You are an experienced Java programmer."},
            {"role": "user", "content": prompt}
          ]
        )
        final_answer = completion.choices[0].message.content    
        st.write(final_answer)
        st.cache_data.clear()
    



def variable_calculations():
    import streamlit as st

    st.title("Variable Calculations")
    model = None
    model = st.radio(
    "Choose your AI assistance model",
    ["ChatGPT", "Llama3.2"],
    index=None)
    
    key_word = "arithmetic"
    
    @st.cache_data
    def load_data():
        import pandas as pd
        return pd.read_csv("data.csv")
    
    data = load_data()
    example = data[data["topic"] == key_word]['question'][1]
    
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
               f'Write a new problem that is similar to the following example:\nDo not include any Java code in your writing.\nExample: {example}\nThe new problem:\n'}
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
                     f'Write a new problem that is similar to the following example:\nExample: {example}\n\nDo not include the following advanced content: array, file i/o, loops, if-else.\n\nThe new problem:\n'}
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


# page_names_to_funcs = {
#     "—": arithmetics,
#     "Arthmetic precendence":arithmetic_precedence,
#     "Calculation with variables": variable_calculations,
    
# }

# demo_name = st.sidebar.selectbox("Choose a practice", page_names_to_funcs.keys())
# page_names_to_funcs[demo_name]()