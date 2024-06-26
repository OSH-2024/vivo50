import neo4j
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext

import base64
import filetype
from sparkai.core.messages import ImageChatMessage
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler

import image_process
import tagging

username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

SPARKAI_APP_ID = '147cb3a4'
SPARKAI_APISECRET = 'OWU3NDhkZDhkNDljNTg4YjQ0ZDBlZDZl'
SPARKAI_APIKEY = '76125c539809ba1e0ce8faca3d20feac'

@ray.remote
def vector_embed(filepath):
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    documents = SimpleDirectoryReader(input_files= filePath).load_data()

    storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
    index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context)

# def extract_keywords(filepath):

# def extract_image(filepath):
#     image_content = base64.b64encode(open(filepath, 'rb').read())
#     spark = ChatSparkLLM(
#         app_id = SPARKAI_APP_ID
#         api_key = SPARKAI_APIKEY
#         api_secret = SPARKAI_APISECRET
        
#     )

def tag(filename, filepath, fileid):
    ## 获取关键词
    keywords = tagging.tagging(filepath)
    vector_embed(filepath)

    
