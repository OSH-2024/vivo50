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
        # ����Ŀ������
        print("��������")
        sock.connect((ray_ip, ray_port))
        # ��Ҫ���͵��ļ�
        sock.sendall("Success".encode("utf-8"))
        print("����neo4j����ɹ���Ϣ")
        if_success = result_holder[0]
    except Exception as e:
        print("���ͱ�ǩʱ���ִ���:", str(e))
    finally:
        # �ر��׽���
        sock.close()

def neo_driver():
    # Neo4j���ݿ�����ӵ�ַ�Ͷ˿ں�
    uri = "bolt://localhost:7687"
    # �����֤��Ϣ
    user = "neo4j"
    password = "11"
    # ����Neo4j���ݿ�����
    graph= Graph(uri, auth=(user, password))
    return graph

if __name__ == "__main__":
    # ����neo4j_driver
    graph = neo_driver()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ����
    sock.bind((listen_ip, listen_port))
    sock.listen(1)

    # ��������
    while True:
        receive_data = b""
        conn, addr = sock.accept()
        print("neo�����ѽ���:", addr)
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
        print("neo������Ϣ�ɹ�")
        print("     ---Check---:receive_data:"+receive_data)
        if command == "Upload":
            vector = receive_data[-2]
            tags   = eval(receive_data[-1])
  