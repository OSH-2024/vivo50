# import os
import neo4j
# import openai
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import ServiceContext, SimpleDirectoryReader, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter

# os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
# openai.api_key = os.environ["OPENAI_API_KEY"]
username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
PATH = "/mnt/workspace/temp"
# 登录neo4j，
neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
# print(neo4j_vector)
# load documents
documents = SimpleDirectoryReader(PATH).load_data()
# print("document/n")
print(documents)
from llama_index.core import StorageContext
# 设置embed大模型
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# 文本索引
Settings.transformations = [SentenceSplitter(chunk_size=1024)]
#为文件创建索引
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=Settings.embed_model,
    transformations=Settings.transformations
)
print(f"index\n",index)
##MultiModalVectorStoreIndex可以储存多模态vector
# storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
# print("storage\n")
# print(storage_context)
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context,show_progress=True
# )
# print("index\n")
# print(index)