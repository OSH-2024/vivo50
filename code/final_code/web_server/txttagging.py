from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

def text_tag(filepath,keywords_num):
    #星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
    SPARKAI_APP_ID = 'b75e9b1e'
    SPARKAI_API_SECRET = 'N2Y4NjE3ZmJhZTk1MjJiNWZiMGY4YjJh'
    SPARKAI_API_KEY = '763a46ae2c351c22df94e63cbd4e9c1c'
    #星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
    SPARKAI_DOMAIN = 'generalv3.5'
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    with open(filepath, "r") as file:
        Content= file.read()
    messages = [ChatMessage(
        role="user",
        content="Please provide several keywords based on the content of the text, with different keywords separated by comma:"+Content
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    tags = repr(a.generations[0][0].text.split(', '))
    print("     ----Check----tags:"+str(tags))
    return tags