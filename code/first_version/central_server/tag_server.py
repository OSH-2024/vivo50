import neo4j
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext

username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def vector_embed(filepath):
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    documents = SimpleDirectoryReader(input_files= filePath).load_data()

    storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
    index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context)
