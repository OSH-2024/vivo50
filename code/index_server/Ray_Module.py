import os
import sys
import socket
import tag_server

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

listen_ip=settings["listen_ip"]
listen_port=settings["Ray_listen_neo"]
neo_ip=settings["neo_ip"]
neo_port=settings["Ray_send_neo"]

use_ray=settings["use_ray"]
split_char=settings["split_char"]
keywords_num=settings["keywords_num"]

result_holder = [False]


def ray_control(message):
    command = message.split(split_char)[0]  # 获取处理类型
    if command == "Upload":
        file_name = message.split(split_char)[1]
        file_path = message.split(split_char)[2]
        file_id   = message.split(split_char)[3]
        Upload(file_name, file_path, file_id)
    elif command = "Delete":
    # 获取在juicefs中的位置和文件名，从而删除文件
        file_name = message.split(split_char)[1]
        file_path = message.split(split_char)[2]
        file_id   = message.split(split_char)[3]
        Delete(file_name, file_path, file_id)


def Upload(filename, filepath, fileid):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 是否需要传来keywords
    keywords = tag_server.tag(filename, filepath, fileid)
    split_char = "%$$%@#!#(*%^&%"
    # Upload filename keywords filepath fileid
    # keywords作为结点
    # filename和filepath和fileid用来查询文件结点，用于连边
    send_data = "Upload" + split_char + filename + split_char + filepath + split_char + fileid
    try:
        # 连接目标主机
        print("尝试连接neo4j_handle")
        sock.connect((neo_ip, neo_port))
        # 发送给neo4j_handle
        sock.sendall(send_data.encode("utf-8"))
        print("发送到neo4j_handle成功")
    except Exception as e:
        print("发送标签时出现错误:", str(e))
    finally:
        sock.close()    
    

def Delete(filename, filepath, fileid):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    split_char = "%$$%@#!#(*%^&%"
    # Upload filename keywords filepath fileid
    # keywords作为结点
    # filename和filepath和fileid用来查询文件结点，用于连边
    send_data = "Delete" + split_char + filename + split_char + filepath + split_char + fileid
    try:
        # 连接目标主机
        print("尝试连接neo4j_handle")
        sock.connect((neo_ip, neo_port))
        # 发送给neo4j_handle
        sock.sendall(send_data.encode("utf-8"))
        print("发送到neo4j_handle成功")
    except Exception as e:
        print("发送标签时出现错误:", str(e))          
    finally:
        sock.close()
              

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