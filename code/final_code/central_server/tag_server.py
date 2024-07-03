import neo4j
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext
from llama_index.core import ServiceContext, StorageContext, Settings

from llama_index.embeddings.nomic import NomicEmbedding
username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 768
api_key = "nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
import os
os.environ["NOMIC_API_KEY"]="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-zh-v1.5")

import config
setting=config.args()
settings=setting.set

def index_upload(fileid, filename, tmpfile_path):
    # 生成vector并存储在neo4j中
    read_path = tmpfile_path
    read_name = filename
    file_ext=filename.split(".")[-1]
    if file_ext == "wav" or file_ext == "mp3":
        read_path = "/home/liuchang/testfs/central_server/wav2txt.txt"
        read_name = "wav2txt.txt"

    try:
        neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
        documents = SimpleDirectoryReader(input_files= [read_path]).load_data()
        storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
        embedding_model = NomicEmbedding(model_name="nomic-embed-text-v1.5",vision_model_name="nomic-embed-vision-v1.5", api_key=api_key)
        index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context, embed_model= embedding_model)

        # print(filepath)
        # 添加File标签， FileID， FilePath， FileName属性
        # 可以通过 MATCH(n:File{FileID: id }) 等获取结点
        query = "match(n:Chunk{file_name:'" + read_name + "', file_path:'"+ read_path +"'}) \
                set n:File set n.FileID = '"+ fileid + "' set n.FilePath = '" + tmpfile_path \
                + "' set n.FileName = '" + filename \
                +"' return n"
        # query = "match(n) return n"
        print(query)
        # 执行query语句，从而设置了 FileID，FilePath， FileName
        res = neo4j_vector.database_query(query)
        print(res)
        return True
        # print(len(res[0].get('n').get('embedding')))
    except Exception as e :
        print(e)
        return False

# if __name__ == "__main__":
#     vector_embed('1',".download.json", "/mnt/workspace/.download.json")
# query1 = "sunny weather"
# query2 = "Files about weather"
# embedding_model = NomicEmbedding(model_name="nomic-embed-text-v1.5",vision_model_name="nomic-embed-vision-v1.5", api_key=api_key)
# em1 = embedding_model.get_query_embedding(query1)
# em2 = embedding_model.get_query_embedding(query2)
# res = embedding_model.similarity(em1,em2)
# print(res)