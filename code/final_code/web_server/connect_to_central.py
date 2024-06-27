import os
import sys
import socket

sys.path.append(os.path.dirname(sys.path[0]))   # 将当前脚本的父目录添加到sys.path列表中。sys.path列表用于确定Python在导入模块时搜索的位置
import config                               # 导入config模块的内容
setting=config.args()
settings=setting.set                            # 把config中的内容导入settings
# 上传：Upload,fileid,filename,filepath,content
# 下载：Download,fileid,filename,filepath
# 删除：Delete,fileid,filename,filepath

listen_ip = settings["listen_ip"]
listen_port = settings["web_listen_central"]
central_ip = settings["central_ip"]
central_port = settings["web_send_central"]

split_char=settings["split_char"].encode("utf-8")   # 将settings["split_char"]按照UTF-8编码转换为字节串，并将结果赋值给split_char变量。

def upload_to_central(fileid, filename, file, filepath):      # 把文件上传到中央服务器 fileid:json中的编号  filename:file名字  file:打开的文件对象
    print("upload进程pid是" + str(os.getpid()))      # 打印当前进程的pid
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # socket.AF_INET(IPv4地址族)和socket.SOCK_STREAM(TCP传输协议)
    # print('111111111')
    # print()
    sock_central = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # sock_central套接字用于与中心服务器进行通信,建立与中心服务器的连接
    # print('22222222')
    # print()
    try:
        sock_central.connect((central_ip, central_port))  # 将 sock_central 套接字连接到指定的远程主机
        #print('33333333')
        print('已连接到central server')
        content = file.read()                             # 将会返回文件中的全部内容作为一个字符串，并将其赋值给变量 content
        print('content长度:', len(content))
        message = b'' + b'Upload' + split_char + str(fileid).encode(
            'utf-8') + split_char + filename.encode('utf-8') + split_char + str(filepath).encode(
            'utf-8') + split_char + content 
            # 建立一个消息字符串 Upload + 分隔符 + fileid + 分隔符 + filename + 分隔符 + filepath + 分隔符 内容
        # print(message)
        sock_central.sendall(message)         #    使用套接字对象 sock_central 发送一个消息 message 到远程主机
        print('已发送上传命令')
        # sock_central.close()
        sock_listen.bind((listen_ip, listen_port)) # 将套接字绑定到指定的 IP 地址和端口号
        sock_listen.listen(5)                      #  开始监听连接请求，将最大连接数设置为 5
        print('等待central server连接')

        conn, addr = sock_listen.accept()          # 用于接受客户端的连接请求，并返回一个新的套接字对象 conn 和客户端的地址 addr
        print('已连接到central server')
        message = conn.recv(1024)                  # 用于从已建立连接的套接字 conn 接收数据，最大接收的字节数为1024
        print('已接收到central server的回复')
        # sock_listen.close()
        if message == b'Upload success':
            print('上传成功')
            return True
        elif message == b'Upload fail':
            print('上传失败')
            return False
        return False
    except OSError as e: # OSError 是一个表示操作系统级别错误的异常类，它可以在套接字编程中的各种情况下被引发
        print(e)
        print(type(sock_central))
        print(type(sock_listen))
    finally:
        print(type(sock_central))
        print(sock_central)
        print(type(sock_listen))
        sock_central.close()
        sock_listen.close()


def download_to_central(fileid, filename, targetpath, filepath):
    print("download进程pid是" + str(os.getpid()))
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_central = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock_central.connect((central_ip, central_port))
        print('已连接到central server')
        message = b'' + b'Download' + split_char + str(fileid).encode(
            'utf-8') + split_char + filename.encode('utf-8')+ split_char + str(filepath).encode('utf-8')
        print(message)
        sock_central.sendall(message)
        print('已发送下载命令')
        # sock_central.close()

        sock_listen.bind((listen_ip, listen_port))
        sock_listen.listen(5)
        print('等待central server连接')

        conn, addr = sock_listen.accept()
        print('已连接到central server')

        content = b''

        while True:
            buffer = conn.recv(4096)
            content = b'' + content + buffer
            if len(buffer) < 4096:
                break

        if content == b'download error':
            print('下载失败')
            return False
        print('已接收到central server的回复')

        with open(targetpath, 'wb') as f:
            f.write(content)

        print('下载成功')

        return True

        # sock_listen.close()

    except OSError as e:
        print(e)
        print(type(sock_central))
        print(type(sock_listen))
    finally:
        print(type(sock_central))
        print(sock_central)
        print(type(sock_listen))
        sock_central.close()
        sock_listen.close()


def Delete_to_central(fileid, filename, filepath):
    print("delete进程pid是" + str(os.getpid()))
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_central = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock_central.connect((central_ip, central_port))
        print('已连接到central server')
        message = b'' + b'Delete' + split_char + str(fileid).encode(
            'utf-8') + split_char + filename.encode('utf-8') + split_char + str(filepath).encode('utf-8')
        sock_central.sendall(message)
        print('已发送删除命令')
        # sock_central.close()

        sock_listen.bind((listen_ip, listen_port))
        sock_listen.listen(5)
        print('等待central server连接')

        conn, addr = sock_listen.accept()
        print('已连接到central server')
        message = conn.recv(1024)
        print('已接收到central server的回复')
        # sock_listen.close()
        if message == b'Delete success':
            print('删除成功')
            return True
        elif message == b'Delete fail':
            print('删除失败')
            return False
        return False
    except OSError as e:
        print(e)
        print(type(sock_central))
        print(type(sock_listen))
    finally:
        print(type(sock_central))
        print(sock_central)
        print(type(sock_listen))
        sock_central.close()
        sock_listen.close()

