import neo4j
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext
from llama_index.core import ServiceContext, StorageContext, Settings
username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-zh-v1.5")

import config
setting=config.args()
settings=setting.set
upload_path=settings["upload_path"]

def index_upload(fileid, filename, tmpfile_path):
    # 生成vector并存储在neo4j中
    try:
        neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
        documents = SimpleDirectoryReader(input_files= [tmpfile_path]).load_data()
        storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
        index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context)

        # 获取在juicefs中的存储路径
        filepath = tmpfile_path.split(upload_path)[1]
        # print(filepath)
        # 添加File标签， FileID， FilePath， FileName属性
        # 可以通过 MATCH(n:File{FileID: id }) 等获取结点
        query = "match(n:Chunk{file_name:'" + filename + "', file_path:'"+ tmpfile_path +"'}) \
                set n:File set n.FileID = '"+ fileid + "' set n.FilePath = '" + filepath \
                + "' set n.FileName = '" + filename \
                +"' return n"
        # query = "match(n) return n"
        # print(query)
        # 执行query语句，从而设置了 FileID，FilePath， FileName
        res = neo4j_vector.database_query(query)
        return True
        # print(len(res[0].get('n').get('embedding')))
    except Exception as e :
        return False

if __name__ == "__main__":
    vector_embed('1',".download.json", "/mnt/workspace/.download.json")
