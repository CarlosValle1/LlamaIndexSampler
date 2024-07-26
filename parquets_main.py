import os
from dotenv import dotenv_values
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from parquethandler import ParquetHandler

# Pulling secrets from .env file
secrets: dict = dotenv_values(".env")

# Overriding OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]

# Defining some constants
parquets_directory: str = 'data/as_parquet/'
parquet_files: list = ['20240601.parquet', '20240602.parquet']

with ParquetHandler(parquet_path=parquets_directory+parquet_files[0]) as parquet_handler:
    tool = FunctionTool.from_defaults(
        *parquet_handler.get_tools(),
    )

    agent = OpenAIAgent.from_tools([tool], verbose=True)

    agent.chat_repl()
