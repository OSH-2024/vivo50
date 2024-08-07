from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core.indices import MultiModalVectorStoreIndex

from sklearn.decomposition import PCA

username = "neo4j"
password = "oshvivo50"
url = "neo4j://localhost"
embed_dim = 768

from llama_index.embeddings.nomic import NomicEmbedding
api_key = "nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
import os
os.environ["NOMIC_API_KEY"]="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
import config
setting=config.args()
settings=setting.set     
split_char=settings["split_char"]
upload_path = settings["upload_path"]
embedding_model = NomicEmbedding(model_name="nomic-embed-text-v1.5",vision_model_name="nomic-embed-vision-v1.5", api_key="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4")
def VectorSearch(query_vector, top_k = 10):
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    print("获取所有的文件节点")
    # 获取所有的文件节点
    stored_nodes = neo4j_vector.database_query("MATCH (n:File) RETURN n")
    print([_['n']['file_path'] for _ in stored_nodes])

    sorted_nodes = sorted(
        stored_nodes,
        reverse = True, 
        key = lambda node : embedding_model.similarity(node['n']['embedding'], query_vector)
    )
    # 去重
    seen = set()
    deduplicated_nodes = []
    for node in sorted_nodes:
        if node['n']['file_path'] not in seen:
            deduplicated_nodes.append(node)
            seen.add(node['n']['file_path'])
    retrieve_index = []
    
    return [node['n']['file_path'] for node in deduplicated_nodes[:top_k]]
    
def IndexSearch(query):
    return VectorSearch(embedding_model.get_query_embedding(query))
def ImageSearch(image_path):
    return VectorSearch(embedding_model.get_image_embedding(image_path))
def SimilarSearch(fileid):
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    node = neo4j_vector.database_query("MATCH (n:File{FileID: \""+ str(fileid)+ "\"}) return n")[0]
    query_vector = node['n']['embedding']
    return VectorSearch(query_vector)

def GetPoints():
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    stored_nodes = neo4j_vector.database_query("MATCH (n:File) RETURN n")
    embeddings = [node['n']['embedding'] for node in stored_nodes]
    pca=PCA(n_components=3)
    pca.fit(embeddings)
    coords = pca.transform(embeddings)
    print(pca.explained_variance_, pca.explained_variance_ratio_)
    return [{'x': coord[0], 'y': coord[1], 'z': coord[2], 'path': node['n']['file_path'][len(upload_path)+1:]}
             for node, coord in zip(stored_nodes, coords)]
if __name__ == "__main__":
    results = IndexSearch("cat")
    print(results)
