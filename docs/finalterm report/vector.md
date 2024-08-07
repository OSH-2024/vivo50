## 向量化存储和检索
### 向量化存储
在上传文件时，利用`llamaindex`和`embedding模型`把文件向量化，构造出一个包含向量和文件信息的文件结点，存储在`neo4j`中，在该过程中主要涉及到文件向量化

- `embedding模型`的选择：在对文件向量化的过程中，考虑到文件类型的多样性，当前embedding模型对多模态数据的支持还处在发展阶段，我们使用了`NomicEmbedding模型`, 该模型支持对文本和图片的向量化，对于音频类文件，我们首先转化为了文本，再进行向量化存储，对于视频类文件，我们采用截帧的方式获取视频中的图片，对图片构建向量。之后利用`llamaindex`与`neo4j`结合，构建出文件结点
### 向量化检索
在对文件的检索中，我们尝试了多种方式
- 其一，由于我们在上传文件的过程中仍采用了关键词模式，即文件结点和关键词结点构成了一个图，所以，可以通过查看图来查找文件
- 其二，我们探索了语义化搜索文件的实现方式。我们可以通过自然语言的方式检索文件。通过图数据库得到各文件的向量，并把语言转化为向量后，计算余弦相似度，取相似度高的结点，通过结点获取文件路径，即可得到所需文件，经测试，有较好效果
- 其三，我们添加了以图片搜索图片等文件的功能，上传图片后，通过比较该图片与其他文件的向量相似度可以得到最相近的图片，经测试，可以支持对图片主体如上传图片中包含宠物，可以检索到有宠物的图片，也可以支持图片风格等的检索，如上传毕加索的作品，可以检索出文件系统中其他毕加索的图片作品。
