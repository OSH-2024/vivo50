from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core.indices import MultiModalVectorStoreIndex
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
embedding_model = NomicEmbedding(model_name="nomic-embed-text-v1.5",vision_model_name="nomic-embed-vision-v1.5", api_key="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4")
text_store = Neo4jVectorStore(
    username, password, url, embed_dim,
    index_name="text",
)
image_store = Neo4jVectorStore(
    username, password, url, embed_dim,
    index_name="image",
)
index = MultiModalVectorStoreIndex.from_vector_store( 
    vector_store = text_store,
    image_vector_store = image_store,
    embed_model = embedding_model,
    image_embed_model = embedding_model
)
retriever = index.as_retriever(similarity_top_k=10, image_similarity_top_k=20)

print("[FileSearch.py] Initialized retriever. ")
def process_results(results):
    # for result in results:
    #     print(f"Score: {result.score:.4f} - File: {result.metadata['file_path']}")
    return [result.metadata['file_path'] for result in results]
def IndexSearch(query):
    results = retriever.retrieve(query)
    return process_results(results)
def IndexSearchImage(image_path):
    retrieval_results = retriever.image_to_image_retrieve(image_path)
    return process_results(results)

if __name__ == "__main__":
    filepath = IndexSearch("two brown dogs")
    print(filepath)
