import neo4j
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext
from llama_index.core import ServiceContext, StorageContext, Settings
from sentence_transformers import SentenceTransformer
import base64
# import filetype
# from sparkai.core.messages import ImageChatMessage
# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
# import image_process
import tagging

username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-zh-v1.5")

SPARKAI_APP_ID = '147cb3a4'
SPARKAI_APISECRET = 'OWU3NDhkZDhkNDljNTg4YjQ0ZDBlZDZl'
SPARKAI_APIKEY = '76125c539809ba1e0ce8faca3d20feac'

# @ray.remote
# def vector_embed(filepath):
filePath = "/mnt/workspace/temp"
# neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
# documents = SimpleDirectoryReader(filePath).load_data()

# storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context)

# from llama_index.core.retrievers import VectorIndexRetriever, VectorIndexAutoRetriever
# from llama_index.core.query_engine import RetrieverQueryEngine 
neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
# storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
# neo4j_vector
# neo4j_vector.aquery("files about image")
# index = VectorStoreIndex.from_vector_store(vector_store= neo4j_vector, show_progress=True)
# print(index)
# retriever = VectorIndexRetriever(
#     index=index,
#     similarity_top_k=5,
#     embed_model="BAAI/bge-small-zh-v1.5",

# ).retrieve.keywords("image")
# # index.as_retriever
# results = retriever._retrieve("image")
# retriever = VectorIndexAutoRetriever(
#     index=index,
#     similarity_top_k=5,
#     llm="BAAI/bge-small-zh-v1.5"
# )
# retriever._retrieve_from_object()

# RetrieverQueryEngine()
# Neo4jVectorStore.query
# def extract_keywords(filepath):

# def extract_image(filepath):
#     image_content = base64.b64encode(open(filepath, 'rb').read())
#     spark = ChatSparkLLM(
#         app_id = SPARKAI_APP_ID
#         api_key = SPARKAI_APIKEY
#         api_secret = SPARKAI_APISECRET
        
#     )

# def tag(filename, filepath, fileid):
#     ## 获取关键词
#     keywords = tagging.tagging(filepath)
#     vector_embed(filepath)


# if __name__ == "__main__":
    # tag("image-2.png", "temp/image-2.png", 1)
    # SentenceTransformer.
# 使用langchain检索文档
# from langchain.llms import OpenAI
# from langchain.retrievers.self_query.base import SelfQueryRetriever
# from langchain.chains.query_constructor.base import AttributeInfo
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import Neo4jVector


# embeddings = HuggingFaceEmbedding()
# # vectorstore = 
# text = "This is a test document."

# query_result = embeddings.embed_query(text)


# 自定义余弦相似度的方法
from sklearn.metrics.pairwise import cosine_similarity
embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-large-zh-v1.5", truncate_dim=1024)
# model = SentenceTransformer("BAAI/bge-large-zh-v1.5", truncate_dim=1024)
# text = "Files about image"
# query_vector = model.encode(text)
# print(model.get_sentence_embedding_dimension())
print()
text = ["关于云的图片"]
# embeddings.similarity()
query_vector = embeddings._embed(text)
print("\n")
print(len(query_vector[0]))
print("\n")
print(query_vector)
print("\n")
results = neo4j_vector.database_query("MATCH (n:Chunk) RETURN n")
# print(results)
vector_list = []
for v in results:
    vector_list.append(v.get('n').get('embedding'))
sim=[]
for i in vector_list:
    # cosine_similarity
    cos = embeddings.similarity(i,query_vector[0])
    print("\n")
    print(cos)
    sim.append(cos)
    # print(i)
    print("\n")
    print(len(i))
    # print("\n")
    # print(type(vector))
index = sim.index(max(sim))
print("\n")
print(index)
print()
print(results[index])