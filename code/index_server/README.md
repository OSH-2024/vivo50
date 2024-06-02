# 说明文档
在该模块中进行打标工作，目前的构想是通过web端传来的内容，抽象出文件路径，操作类型等，然后进行相应的操作
## embedding模型 : 暂时尝试BAAI/bge-small-en-v1.5，
llamaindex默认使用openai模型进行embedding处理，所以最好需要本地部署其他模型
此模型貌似只能对英文操作，但是也有相应的中英文版本
- 配置问题: 由于模型较大，所以采用云端存储的方式，
```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```
在设置embed_model过程中，会遇到类似以下问题
```shell
OSError: We couldn't connect to 'https://huggingface.co' to load this file, couldn't find it in the cached files and it looks like BAAI/bge-small-en-v1.5 is not the path to a directory containing a file named config.json.
```
所以根据此[链接](#https://blog.csdn.net/weixin_43431218/article/details/135403324)设置镜像源`export HF_ENDPOINT=https://hf-mirror.com`，把模型下载到本地，解决该问题

- dsw上部署neo4j的问题
我尝试了使用dsw远程访问neo4j，暂时失败，所以尝试在dsw上部署，dsw上没有浏览器，所以从本地下载后上传，并使用
    `sudo apt install openjdk-17-jdk`下载jdk17
但是此时仍然没法通过网页端访问neo4j
尝试远程打开dsw，感觉远程有点复杂，先放个[链接](#https://blog.csdn.net/Zheng113/article/details/135351718)。
- 另一种连接思路：进入bin文件夹，运行`./neo4j`，然后运行`./cypher-shell`，可以终端操作neo4j，设置密码为`oshvivo50`，用户为`neo4j`，然后再次运行tag文件，即可登录。
- 从文件读数据时，SimpleDirectoryReader貌似只能从文件夹读取
### 记录
调用load_data会自动判断文件类型，并且有个初始化id，包括以下内容
> ImageDocument(id_='af11e34b-d33b-4ede-9e97-e41343d3516a', embedding=None, metadata={'file_path': '/mnt/workspace/temp/image-2.png', 'file_name': 'image-2.png', 'file_type': 'image/png', 'file_size': 67148, 'creation_date': '2024-05-28', 'last_modified_date': '2024-05-28'}, excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'], excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'], relationships={}, text='', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n', image=None, image_path='/mnt/workspace/temp/image-2.png', image_url=None, image_mimetype=None, text_embedding=None),

> Document(id_='b0fbd59b-a7f4-4201-ac8f-e04b6baad4f7', embedding=None, metadata={'file_path': '/mnt/workspace/temp/tag.ipynb', 'file_name': 'tag.ipynb', 'file_size': 1799, 'creation_date': '2024-05-27', 'last_modified_date': '2024-05-26'}, excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'], excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'], relationships={}, text='\n\n\nfrom llama_index.core import ServiceContext, SimpleDirectoryReader, StorageContext, Settings\nfrom llama_index.embeddings.huggingface import HuggingFaceEmbedding\n\n\n# ', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), 

以下代码实现在neo4j中存储数据
```python
    documents = SimpleDirectoryReader(filePath).load_data()
    # 需要对文件进行分块和提取元数据操作，分为文本和图片
    #以下将自动进行分块index
    neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
    storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
```

