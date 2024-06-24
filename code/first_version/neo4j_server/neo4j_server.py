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

