import logging
import string
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import os
import sys
import socket

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

listen_ip=settings["listen_ip"]
listen_port=settings["neo_listen_Ray"]
ray_ip=settings["central_ip"]
ray_port=settings["neo_send_Ray"]

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
    password = "11"
    # 创建Neo4j数据库驱动
    graph= Graph(uri, auth=(user, password))
    return graph

if __name__ == "__main__":
    # 创建neo4j_driver
    graph = neo_driver()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听
    sock.bind((listen_ip, listen_port))
    sock.listen(1)

    # 接收数据
    while True:
        receive_data = b""
        conn, addr = sock.accept()
        print("neo连接已建立:", addr)
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            # print("----Check----:",chunk)
            receive_data += chunk      
        receive_data = receive_data.decode("utf-8")
        receive_data = eval(receive_data)
        command = receive_data[0]
        conn.close()
        print("neo接收消息成功")
        print("     ---Check---:receive_data:"+receive_data)
        if command == "Upload":
            vector = receive_data[-2]
            tags   = eval(receive_data[-1])
  