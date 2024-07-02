from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 1536

from llama_index.embeddings.nomic import NomicEmbedding
api_key = "nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
import os
os.environ["NOMIC_API_KEY"]="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
import config
setting=config.args()
settings=setting.set     
split_char=settings["split_char"]
embedding_model = NomicEmbedding(model_name="nomic-embed-text-v1.5",vision_model_name="nomic-embed-vision-v1.5", api_key="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4")
def IndexSearch(query):
    #
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    print("获取所有的文件节点")
    # 获取所有的文件节点
    stored_vector = neo4j_vector.database_query("MATCH (n:File) RETURN n")
    tag_vector = neo4j_vector.database_query("MATCH(n:Tag) return n")
    # embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-large-zh-v1.5", truncate_dim=1024)
    query_vector = embedding_model.get_query_embedding(query)
    tag_similarity = []
    for tag in tag_vector:
        embedding = tag.get('n').get('embedding')
        similarity = embedding_model.similarity(embedding,query_vector)
        tag_similarity.append(similarity)
        print(tag_vector[index].get('n').get('name'))
        print(similarity)
    
    # tag_res = sorted(tag_similarity)
    # for res in tag_res:
    #     index = tag_similarity.index(res)
        print(tag_vector[index].get('n').get('name'))
    print("获取所有的vector")
    # 获取所有的vector
    vector_list = []
    for vector in stored_vector:
        vector_list.append(vector.get('n').get('embedding'))
    print(len(vector_list))
    similarity_res = []
    print("计算余弦相似度")
    # 计算余弦相似度
    for vector in vector_list:
        similarity = embedding_model.similarity(vector, query_vector)
        print(similarity)
        similarity_res.append(similarity)
    print("获取相似度最大的几个文件")
    # 获取相似度最大的几个文件
    # 降序排列
    # print(similarity_res)
    sorted_res = sorted(similarity_res, reverse= True)
    # 判断相关性
    # 初步判断余弦相似度相差在0.03以内进行推荐
    # print("找对应的index")
    difference = 0.03
    # 找对应的index
    retrieve_index = []
    # split_char = 
    # retrieve_files = f""
    for res in  sorted_res:
        max_res = sorted_res[0]
        if((max_res - res) < difference):
            index = similarity_res.index(res)
            retrieve_index.append(index)
            # # 获取结点文件路径
            # stored_vector[index].get('n').get('file_path')
        else:
            break
    print("获取结点文件路径")
    retrieve_files = f""
    for i in range(len(retrieve_index)):
        # 获取结点文件路径
        if i == 0:
            retrieve_files = stored_vector[retrieve_index[0]].get('n').get('file_path')
        else:
            path = stored_vector[retrieve_index[i]].get('n').get('file_path')
            retrieve_files = retrieve_files + split_char + path
    return retrieve_files

if __name__ == "__main__":
    filepath = IndexSearch("一只英国短毛猫，蓝色背景，坐着，看向你")
    #print(filepath)



