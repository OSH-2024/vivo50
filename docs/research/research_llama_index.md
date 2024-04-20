# llama_index

LlamaIndex 是一个将大语言模型（Large Language Models, LLMs，后简称大模型）和外部数据连接在一起的工具。
LlamaIndex的任务是通过查询、检索的方式挖掘外部数据的信息，并将其传递给大模型，因此其主要由3部分组成：
1.	数据连接。首先将数据能读取进来，这样才能挖掘。
2.	索引构建。要查询外部数据，就必须先构建可以查询的索引，llamaIndex将数据存储在Node中，并基于Node构建索引。索引类型包括向量索引、列表索引、树形索引等；
3.	查询接口。有了索引，就必须提供查询索引的接口。通过这些接口用户可以与不同的 大模型进行对话，也能自定义需要的Prompt组合方式。查询接口会完成 检索+对话的功能，即先基于索引进行检索，再将检索结果和之前的输入Prompt进行（自定义）组合形成新的扩充Prompt，对话大模型并拿到结果进行解析。
而我们要做的简单来说
1.	将文件传入Llama index
2.	由llama index解析文件为Node
3.	再从Node构建index
4.	使用Prompt template拼接上用户的query（如要求LLM对文档中提取出来的信息进行打标）以及从索引里面检索得到的文本信息，作为最终的prompt，发送给LLM，通过归纳总结得到最终的response。

# RAG
检索增强生成（Retrieval Augmented Generation），简称 RAG

RAG就是通过检索获取相关的知识并将其融入Prompt，让大模型能够参考相应的知识从而给出合理回答。因此，可以将RAG的核心理解为“检索+生成”，前者主要是利用向量数据库的高效存储和检索能力，召回目标知识；后者则是利用大模型和Prompt工程，将召回的知识合理利用，生成目标答案。

### 思考
经过探索，发现TagGPT 效果不太符合预期，那么用rag+llama index 进行检索增强呢？

由于llama index可以对文件构建索引，从而对文件进行存储，然后借助rag进行检索增强，从而搜索出需要的文件
或者将初步搜索到的文件
llama index处理文件时构造了一个json文件，json文件里貌似包含多模态数据（如图片）的主要内容。
详细信息：
https://blog.csdn.net/cycyc123/article/details/137225998

其他链接：
使用 Neo4j 和 LangChain 集成非结构化知识图增强 QA：
http://t.csdnimg.cn/io5N4
LlamaIndex：轻松构建索引查询本地文档的神器：
https://zhuanlan.zhihu.com/p/638827267
LLM之RAG实战（八）| 使用Neo4j和LlamaIndex实现多模态RAG：
https://zhuanlan.zhihu.com/p/673647340
使用python免费调用Google发布的Gemini双子座大模型API：
https://zhuanlan.zhihu.com/p/673362535
https://zhuanlan.zhihu.com/p/668082024
https://zhuanlan.zhihu.com/p/630832409