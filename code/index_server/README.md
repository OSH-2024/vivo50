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
所以根据此[链接](#https://blog.csdn.net/weixin_43431218/article/details/135403324)设置镜像源，把模型下载到本地，解决该问题