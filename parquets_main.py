# parquets_main.py

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

with ParquetHandler(parquet_path=[parquets_directory + file for file in parquet_files]) as parquet_handler:
    tools = [
        FunctionTool.from_defaults(
            fn=parquet_handler.get_data,
            name="get_parquet_data",
            description="""
                Use this function to query the parquet files containing telemetry data organized by sensor sources 
                (Inlet, Outlet, Return, Supply, Floor, Ambient). Also it contains calculated data for variables like: 
                RCI high, RCI low and Power IT. As well as it contains information about the entities of the 
                datacenter's structure with this hierachy schema: Datacenter -> Room -> Row -> Rack -> Sensor. 
                You can ask for temperature, humidity, pressure, rssi and their averages, minimums, and maximums. 
                The data is stored in a table named 'parquets'. Use SQL to query the data.
            """
        )
    ]

    agent = OpenAIAgent.from_tools(tools, verbose=True)

    # agent.chat_repl()
    # Chat loop
    while True:
        usr_input: str = input()
        final_input: str = f"""
        Take a look at this database schema: {parquet_handler.get_schema()}
        Now look at the user input: {usr_input}.
        Solve it!
        """
        response = agent.chat(final_input)
        print(f'Assistant: {response}')
