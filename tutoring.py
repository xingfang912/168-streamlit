# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:48:04 2025

@author: xfang13
"""

from openai import OpenAI

client = OpenAI()

# Step 1: Upload a File with an "assistants" purpose
my_file = client.files.create(
  file=open("prog3F24.docx", "rb"),
  purpose='assistants'
)
print(f"This is the file object: {my_file} \n")

# Step 2: Create an Assistant
my_assistant = client.beta.assistants.create(
    model="gpt-4o", #gpt-3.5-turbo-1106
    instructions="You are a Java programming tutor. Your knowledge base is a homework assignment that students is having problems about.",
    name="Java",
    tools=[{"type": "file_search"}]
)

# Step 3: Create a Thread
my_thread = client.beta.threads.create()

# Step 4: Add a Message to a Thread
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role="user",
  content="I am having issues in figuring out the step-by-step solution to the homework problem that I attached. Please show me the step-by-step solution without showing me any actual Java code.",
  attachments=[{"file_id":my_file.id, "tools":[{"type": "file_search"}]}]
)

# Step 5: Run the Assistant
my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=my_assistant.id,
  instructions="Please address the user as Xing Fang."
)

# Step 6: Periodically retrieve the Run to check on its status to see if it has moved to completed
while my_run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")

        # Step 7: Retrieve the Messages added by the Assistant to the Thread
        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )

        print("------------------------------------------------------------ \n")

        print(f"User: {my_thread_message.content[0].text.value}")
        print(f"Assistant: {all_messages.data[0].content[0].text.value}")

        break
    elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        pass
    else:
        print(f"Run status: {keep_retrieving_run.status}")
        break