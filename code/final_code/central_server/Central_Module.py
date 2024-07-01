import os
import ray
import sys
import queue
import socket
from threading import Thread
from Ray_Module import ray_control
from FileSearch import FileSearch
from tag_server import index_upload


sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

listen_ip=settings["listen_ip"]
listen_port = settings["central_listen_web"]
web_ip=settings["web_ip"]
web_port=settings["central_send_web"]

download_path=settings["download_path"]
upload_path=settings["upload_path"]
storage_path=settings["storage_path"]
use_ray=settings["use_ray"]
split_char=settings["split_char"]


def listenning():
    print('listening进程的进程号是：', os.getpid())
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_listen.bind((listen_ip, listen_port))
        sock_listen.listen(1)
        print('central等待连接并接收命令')
        while True:
            print('准备接受下一条命令')
            conn, addr = sock_listen.accept()
            print('central连接已建立: ', addr)

            message = b''
            # content_len=0
            while True:
                buffer = conn.recv(4096)
                message = message + buffer
                # print('传输中：', message)
                if len(buffer) < 4096:
                    break

            print('收到命令buffer')
            message = message.split(split_char.encode('utf-8'))  # 上传图片时会在转换成utf-8时出错

            if message[0] == b'Upload':  # 上传：Upload,fileid,filename,filepath,content
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                message[2] = message[2].decode('utf-8')
                message[3] = message[3].decode('utf-8')
                content = message[4]

                print('上传的文件内容是')
                print(content)
                file_name = os.path.join(upload_path + message[3], message[2])
                with open(os.path.join(file_name), 'wb') as file:
                    file.write(content)

                print('已写入本地')
                message = message[0:5]
                message_queue.put(message)
                print('upload message 已经入队')
                print(message)


            elif message[0] == b'Download':  # 下载：download,file_id,filename 
            # message = 'Download' + str(fileid).encode('utf-8') + split_char + filename.encode('utf-8')+ split_char + str(from_path).encode('utf-8')
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                message[2] = message[2].decode('utf-8')
                message[3] = message[3].decode('utf-8')
                message = message[0:4]
                message_queue.put(message)
                print('download message 已经入队')

            elif message[0] == b'Delete':  # 删除：Delete,file_id,filename 
            # message = 'Delete' + fileid + filename + filepath
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                message[2] = message[2].decode('utf-8')
                message[3] = message[3].decode('utf-8')
                message = message[0:4]
                message_queue.put(message)
                print('Delete message 已经入队')

            elif message[0] == b'Search':  # 删除：Delete,file_id,filename 
            # message = 'Delete' + fileid + filename + filepath
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                message[2] = message[2].decode('utf-8')
                message[3] = message[3].decode('utf-8')
                message = message[0:4]
                message_queue.put(message)
                print('Search message 已经入队')

            else:
                print('未定义消息')
                send_message_to_web('fail')

    # except Exception as e:
    #     print(e)

    # except OSError:
    #     print('socket error')

    finally:
        sock_listen.close()


def handle_web_message():
    print('handle进程的进程号是：', os.getpid())

    while True:
        if message_queue.empty():
            pass
        else:
            print('handle message')
            message = message_queue.get()
            command=message[0]
            fileid=message[1]
            filename=message[2]
            filepath=message[3]
            if command == 'Upload':
                content=message[4]
              #  print(message)
                if FileUpload(fileid, filename, filepath, content):
                    print('upload success')

            elif command == 'Download':
                if FileDownload(fileid, filename, filepath):
                    print('download success')

            elif command == 'Delete':
                if FileDelete(fileid, filename, filepath):
                    print('Delete success')
                # if remove(message[1],message[2]):
            elif command == 'Search':
                query = message[1]
                if FileSearch(query):
                    print('Search success')
            else:
                raise Exception('未定义操作')


def send_message_to_web(message):
    print('send进程的进程号是：', os.getpid())
    sock_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock_web.connect((web_ip, web_port))
        sock_web.sendall(message.encode('utf-8'))

    # except OSError:
    #     print(type(sock_web))

    finally:
        sock_web.close()


def FileUpload(fileid, filename, filepath, filecontent):  # filepath 要上传的文件存储在中央服务器的地址
    print("开始上传")
    file_name = os.path.join(storage_path+filepath,filename)  # 这个是正式存入juicefs的path
    tmpfile_path = os.path.join(upload_path + filepath,filename)  # 这个是上传文件的缓冲区路径
    if ray_control('Upload' + split_char + fileid + split_char + filename + split_char + tmpfile_path) is False:
        print('Ray模块标签存入缓冲区错误')
        send_message_to_web('Upload fail')
        return False
    print("所有模块准备完成,开始正式写入:")
    if ray_control('Commit'+ split_char + fileid + split_char + filename + split_char + tmpfile_path) is False:
        print('ray commit error')
        return False
    print("写入Ray模块成功")

    if index_upload(fileid, filename, tmpfile_path) is False :
        print('生成向量化索引错误')
        return False
    print("生成向量化索引成功")


    print("开始写入JuiceFS")
 #   print('-----------------------------')
 #   print()
 #   print(file_name)

    with open(file_name, "wb") as file:
        file.write(filecontent)
    print("写入JuiceFS成功")
    send_message_to_web('Upload success')
    return True


def FileDownload(fileid, filename, filepath):
    sock_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('开始下载')
    try:
        sock_web.connect((web_ip, web_port))
        # 打开要发送的文件
        file_path = os.path.join(storage_path, filepath)
        with open(file_path, 'rb') as file:
            # 读取文件内容
            data = file.read()
            # 发送文件数据
            sock_web.sendall(data)
        print("文件发送完成")
    # except OSError:
    #     print('socket error')
    finally:
        sock_web.close()
    return True


def FileDelete(fileid, filename, filepath):
    print("开始删除")
    delete_path = storage_path + filepath  # 这个是要删除文件在juicefs的path
    tmpfile_path = upload_path + filepath  # 这个是要删除文件的缓冲区路径,是包括文件名的
    if ray_control('Delete' + split_char + fileid + split_char + filename + split_char + tmpfile_path) is False:
        print('Ray模块标签存入缓冲区错误')
        send_message_to_web('Delete fail')
        return False
    print("所有模块准备完成,开始正式删除:")
    if ray_control('Commit'+ split_char + fileid + split_char + filename + split_char + tmpfile_path) is False:
        print('ray commit error')
        return False
    print("Ray模块删除成功")

    if index_delete(fileid, filename, tmpfile_path) is False :
        print('删除向量化索引错误')
        return False
    print("删除向量化索引成功")



    print("开始在JuiceFS中删除文件")
    os.remove(delete_path)
    os.remove(tmpfile_path)
    #print(filepath)
    #print(fileid)
    #print(filename)
    print("在JuiceFS中删除成功")
    send_message_to_web('Delete success')
    return True

def FileSearch(query):
    print("开始查询")
    # content = '11/1.png'+split_char+'22/readme.md'
    content = FileSearch(query)
    print("查询得到的内容是：")
    print(content)
    send_message_to_web(content)
    return True


message_queue = queue.Queue()

if __name__ == "__main__":
    if use_ray:
        ray.init()
    listen_thread = Thread(target=listenning)
    handle_thread = Thread(target=handle_web_message)
    listen_thread.start()
    handle_thread.start()
    listen_thread.join()
    handle_thread.join()

