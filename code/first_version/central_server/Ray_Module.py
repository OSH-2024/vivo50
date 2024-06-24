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
# message采用列表格式
"""
message[0] 代表upload等类型
message[1] 如果有文件,代表filename
message[2] 代表文件路径
message[3] 代表文件id
"""
def ray_control(message):
    command = message[0]  # 获取处理类型
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
        # 监听连接
        sock.listen(1)
        print("Ray模块等待连接...")
        # 接受连接
        conn, addr = sock.accept()
        print("Ray模块连接已建立:", addr)
        # 创建保存文件的空文件
        data = conn.recv(4096)
        data=data.decode('utf-8')
        if(data == "Success"):
            result_holder[0]=True
            # print("     ----Check----result_holder:" + str(result_holder))
        # 关闭连接
    finally:
        sock.close()        