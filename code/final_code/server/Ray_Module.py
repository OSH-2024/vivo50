import os
import sys
import socket
import tagging
import tagging_ray

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
    # 解析
    command=message.split(split_char)[0]
    fileid=message.split(split_char)[1]
    filename=message.split(split_char)[2]
    filepath=message.split(split_char)[3]
    print('massage is:')
    print(message)
    if command == "Upload":
        return Upload(fileid,filename,filepath)
    elif command == "Delete":
        return Delete(filename,fileid,filepath)
    elif command == "Commit":
        return Commit()
    else:
        print("Error:Undefined command")

def Upload(fileid,filename,filepath):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ray:
        keywords = tagging_ray.tagging(filepath)
    else:
        keywords = tagging.tagging(filepath,keywords_num)
    send_data="Upload"+split_char+fileid+split_char+filename+split_char+filepath + split_char + keywords
    print("关键字是")
    print(keywords)
    # print("------")
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

    listening(listen_ip, listen_port)
    # print("     ----Check----result_holder:"+str(result_holder))
    if_success=result_holder[0]

    # print("     ----Check----if_success:" + str(if_success))
    return if_success

#'Delete' + split_char + fileid + split_char + filename + split_char + tmpfile_path

def Delete(filename,fileid,filepath):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_data = "Delete" + split_char + fileid + split_char + filename + split_char + filepath
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

    listening(listen_ip, listen_port)
    # print("     ----Check----result_holder:" + str(result_holder))
    if_success = result_holder[0]

    # print("     ----Check----if_success:" + str(if_success))
    return if_success

def Commit():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 连接目标主机
        sock.connect((neo_ip, neo_port))
        # 打开要发送的文件
        sock.sendall("Commit".encode("utf-8"))
        print("发送Commit消息成功")
    except Exception as e:
        print("发送Commit消息时出现错误:", str(e))
    finally:
        # 关闭套接字
        sock.close()
    return True

def listening(listen_ip,listen_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定IP和端口
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
    # event.set()
