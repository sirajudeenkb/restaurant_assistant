from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import ServiceContext, VectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import warnings
warnings.filterwarnings("ignore")

class AiVoiceAssistant:
    def __init__(self, ngrok_url):
        self._qdrant_url = "http://localhost:6333"
        self._client = QdrantClient(url=self._qdrant_url, prefer_grpc=False)
        self._llm = Ollama(model="llama3.1", base_url=ngrok_url, request_timeout=120.0)  # Use ngrok URL here
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self._service_context = ServiceContext.from_defaults(llm=self._llm, embed_model=embed_model)
        self._index = None
        self._create_kb()
        self._create_chat_engine()

    def _create_chat_engine(self):
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        self._chat_engine = self._index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=self._prompt,
        )

    def _create_kb(self):
        try:
            reader = SimpleDirectoryReader(
            input_files=[r"./rag/restaurant_file.txt"]
            )
            documents = reader.load_data()
            vector_store = QdrantVectorStore(client=self._client, collection_name="knowledge_base")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self._index = VectorStoreIndex.from_documents(
                documents, service_context=self._service_context, storage_context=storage_context
            )
            print("Knowledgebase created successfully!")
        except Exception as e:
            print(f"Error while creating knowledgebase: {e}")

    def interact_with_llm(self, customer_query):
        AgentChatResponse = self._chat_engine.chat(customer_query)
        answer = AgentChatResponse.response
        return answer
    
    @property
    def _prompt(self):
        return """
            You are a professional AI Assistant receptionist for Madras Kitchen, one of Chennai's best restaurants. 
            People will call to place orders with you. Ask the questions in square brackets, one at a time, keeping 
            the conversation engaging. Don't ask all questions at once.

            [Ask Name and contact number, what they want to order and end the conversation with greetings!]

            If unsure, admit you don't know. Keep answers concise, under 10 words. Don't chat with yourself.
            """