from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.chat_engine.types import BaseChatEngine

class DocChatter:

    def __init__(self, data_path: str) -> None:
        documents = SimpleDirectoryReader(data_path).load_data()
        index: VectorStoreIndex = VectorStoreIndex.from_documents(documents)
        self.__chat_engine: BaseChatEngine = index.as_chat_engine()

    def chat(self, usr_input: str) -> str:
        return self.__chat_engine.chat(usr_input)
