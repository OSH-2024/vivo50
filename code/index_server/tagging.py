# import os
import neo4j
# import openai
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import ServiceContext, SimpleDirectoryReader, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
# openai.api_key = os.environ["OPENAI_API_KEY"]
username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
PATH = ""
neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
print(neo4j_vector)
# load documents
documents = SimpleDirectoryReader(PATH).load_data()
# print("document/n")
print(documents)
from llama_index.core import StorageContext
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
# print("storage\n")
# print(storage_context)
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context,show_progress=True
# )
# print("index\n")
# print(index)