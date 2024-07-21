import os
from dotenv import dotenv_values
from docchatter import DocChatter

# Pulling secrets from .env file
secrets: dict = dotenv_values(".env")

# Overriding OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]

# Creating DocChatter instance
print("Processing documents..")
aiDocChatter: DocChatter = DocChatter(data_path="data")
print("Digested documents\nReady to chat!\n\n")

# Chat loop
while True:
    usr_input: str = input()
    response = aiDocChatter.chat(usr_input)
    print(f'Assistant: {response}')
