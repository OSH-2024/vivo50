import os
import sys
import socket
import tagging

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

listen_ip=settings["listen_ip"]
listen_port=settings["Ray_listen_neo"]
neo_ip=settings["neo_ip"]
neo_port=settings["Ray_send_neo"]

use_ray=settings["use_ray"]
# message�����б��ʽ
"""
message[0] ����upload������
message[1] ������ļ�,����filename
message[2] �����ļ�·��
message[3] �����ļ�id
"""
def ray_control(message):
    command = message[0]  # ��ȡ��������
    if command == "Upload":
        filename = message[1]
        filepath = message[2]
        fileid   = message[3]
        Upload(filename, filepath, fileid)
    elif command = "Delete":
        filename = message[1]
        fileid   = message[2]
        Delete(filename, fileid)
    elif command = "Search":

def Upload(filename, filepath, fileid):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def Delete(filename, fileid):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    send_data = ["Delete", filename, "None", fileid]
    try:


def Search():

def listening(listen_ip, listen_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        sock.bind((listen_ip, listen_port))
        # ��������
        sock.listen(1)
        print("Rayģ��ȴ�����...")
        # ��������
        conn, addr = sock.accept()
        print("Rayģ�������ѽ���:", addr)
        # ���������ļ��Ŀ��ļ�
        data = conn.recv(4096)
        data=data.decode('utf-8')
        if(data == "Success"):
            result_holder[0]=True
            # print("     ----Check----result_holder:" + str(result_holder))
        # �ر�����
    finally:
        sock.close()        