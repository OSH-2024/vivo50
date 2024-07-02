import os
import sys
import socket
from py2neo import Graph, Node, NodeMatcher
from py2neo import Relationship, NodeMatch
from py2neo.matching  import NodeMatcher

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

from llama_index.embeddings.nomic import NomicEmbedding
api_key = "nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
import os
os.environ["NOMIC_API_KEY"]="nk-Fd--NtdLRVionYfsi4CS35FafKT_ddYP1I5OU1rOzk4"
embedding_model = NomicEmbedding(model_name="nomic-embed-text-v1.5",vision_model_name="nomic-embed-vision-v1.5", api_key=api_key)
listen_ip=settings["listen_ip"]
listen_port=settings["neo_listen_Ray"]
ray_ip=settings["central_ip"]
ray_port=settings["neo_send_Ray"]
split_char=settings["split_char"]

download_path=settings["download_path"]
temp="..\\temp\\"

result_holder=["0"]

def call_ray():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ###########
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ###########
    try:
        # 连接目标主机
        print("尝试连接")
        sock.connect((ray_ip, ray_port))
        # 打开要发送的文件
        sock.sendall("Success".encode("utf-8"))
        print("发送neo4j缓存成功消息")
        if_success = result_holder[0]
    except Exception as e:
        print("发送标签时出现错误:", str(e))
    finally:
        # 关闭套接字
        sock.close()

def neo_driver():
    # Neo4j数据库的连接地址和端口号
    uri = "bolt://localhost:7687"
    # 身份验证信息
    user = "neo4j"
    password = "oshvivo50"
    # 创建Neo4j数据库驱动
    graph= Graph(uri, auth=(user, password))
    return graph

if __name__ == "__main__":
    graph=neo_driver()
    matcher = NodeMatcher(graph)
    # event=threading.Event()
    print("成功创建neo4j的driver")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((listen_ip, listen_port))
        sock.listen(1)
        print("neo等待连接...")

        while(True):
            receive_data = b""
            conn, addr = sock.accept()
            print("neo连接已建立:", addr)
            # 接收消息
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                # print("----Check----:",chunk)
                receive_data += chunk
            receive_data = receive_data.decode("utf-8")
            data_temp=receive_data
            command=data_temp.split(split_char)[0]
            conn.close()
            print("neo接收消息成功")
            print("     ---Check---:receive_data:"+receive_data)
            if command != "Commit":
                with open(temp+"temp.temp", "wb") as file:
                    file.write(receive_data.encode("utf-8"))
                print("存入缓存成功")
                call_ray()
            else:
                with open(temp+"temp.temp", "r") as file:
                    cache_data=file.read()
                print("读取缓存成功")
                cache_command=cache_data.split(split_char)[0]
                fileid=cache_data.split(split_char)[1]
                filename=cache_data.split(split_char)[2]
                filepath=cache_data.split(split_char)[3]
                if cache_command == "Upload":
                    tags=cache_data.split(split_char)[4]
                    tags=eval(tags)
                    print("     ----Check----tags_num:" + str(len(tags)))
                    print("     ----Check----tags:"+str(tags))
                    # 创建结点
                    '''
                    file_node = Node("File",name=filename,fileid=fileid) 
                    graph.create(file_node)                                 #创建文件代表的节点
                    '''
                    # 这里是要改成按照fileid查询的
                    query = "MATCH (n:Chunk{file_name: \""+ filename+ "\", file_path:\"" + filepath+"\" }) SET n:File SET n.file_ID ="+ fileid + " RETURN n"
                    # print(query)
                    sub_graph = graph.run(query).to_subgraph()
                    file_nodes = sub_graph.nodes
                    file_node = list(file_nodes)[0]
                    for tag in tags:
                        matcher = NodeMatcher(graph)    
                        result = matcher.match("Tag").where("_.name=" + "'" + tag + "'").first()
                        # print(type(result))
                        #result = matcher.match("Tag").where("_.name=tag").first()  #使用NodeMatch进行匹配
                        if result:
                            tag_node = result
                        else :
                            embedding = embedding_model.get_text_embedding(tag)
                            tag_node = Node("Tag",name=tag, embedding=embedding)
                            graph.create(tag_node)
                        tmp_rela = Relationship(tag_node, 'IS_TAG', file_node)
                        graph.create(tmp_rela)
                    print("成功在图数据库中建边")
                if cache_command == "Delete":
                    print("尝试删除")
                    try:
                        print("     ----Check----fileid:"+str(fileid))
                        query = "MATCH (n:Chunk{file_name: \""+ filename+ "\", file_path:\"" + filepath+"\" }) SET n:File SET n.file_ID ="+ fileid + " RETURN n"
                        # print(query)
                        sub_graph = graph.run(query).to_subgraph()
                        file_nodes = sub_graph.nodes
                        file_node = list(file_nodes)[0]
                        graph.delete(file_node)
                        print("节点删除成功")
                    except Exception as e:
                        print("节点删除失败:", e)
                    # 使用 Cypher 查询找到孤立节点
                    query = f"MATCH (n:Tag) WHERE NOT ()--(n) RETURN n"
                    result = graph.run(query)
                    # 遍历结果并删除孤立节点
                    for record in result:
                        node = record["n"]
                        print(node)
                        try:
                            graph.delete(node)  # 删除节点及其关系边
                            print("孤立节点删除成功")
                        except Exception as e:
                            print("孤立节点删除失败:", e)
                    print("Delete成功")
    finally:
        sock.close()