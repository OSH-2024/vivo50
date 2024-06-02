# import os
import neo4j
# import openai
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import ServiceContext, SimpleDirectoryReader, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.indices.multi_modal.base import MultiModalVectorStoreIndex
from llama_index.multi_modal_llms.ollama import OllamaMultiModal

# os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
# openai.api_key = os.environ["OPENAI_API_KEY"]
username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
filePath = "/mnt/workspace/temp"
database = ""
#设置embeding模型
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
mm_model = OllamaMultiModal(model= "llava:13b")
# 希望可以对传来的数据进行向量化存储，并提取出元数据方便可视化，但用已知函数只能提取出一些属性
# 后续应该向结点中添加text，relation，
# 并应学习并尝试管道
from llama_index.core.prompts import PromptTemplate

def storeFile(filePath):
    prompt_tmp = ""
    prompt = PromptTemplate(prompt_tmp)
    documents = SimpleDirectoryReader(input_files= filePath).load_data()
    vector_index = MultiModalVectorStoreIndex.from_documents(documents, embed_model= Settings.embed_model)
    query_engine = vector_index.as_query_engine(llm= mm_model)
    query = ""
    response = query_engine.query(query)
    # 获取response，作为file的描述，或者继续把response作为输入提取关键词，
    # 然后添加到file的属性中，把vector一并加入，值得一提的是，得到的结果可能是错的


    # neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim, database, hybrid_search=true)


# def 

# def loadData(filePath):
# documents = SimpleDirectoryReader(filePath).load_data()
# print("\n")
# print(documents)
# print("\n")
#     # 可能需要对文件进行分块和提取元数据操作，分为文本和图片

#     #以下将自动进行分块index

    # 可以尝试自定义节点，以上是调用函数自动分块并存储

# from llama_index.multi_modal_llms import OllamaMultiModal
# mm_model = OllamaMultiModal(model = "llava")

    
