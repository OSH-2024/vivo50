import os
import ray
import sys
import queue
import socket
from threading import Thread
# from EC_Module import erasure
# from Ray_Module import ray_control

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

listen_ip=settings["listen_ip"]
listen_port = settings["central_listen_web"]
web_ip=settings["web_ip"]
web_port=settings["central_send_web"]

absolute_path=settings["absolute_path"]
upload_path=settings["upload_path"]
storage_path=settings["storage_path"]
use_ray=settings["use_ray"]
split_char=settings["split_char"]
temp="/"


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
                # print(len(content))
                # file.write(content)
                buffer = conn.recv(4096)
                message = message + buffer
                # print('传输中：', message)
                if len(buffer) < 4096:
                    break
                # content_len+=len(buffer)
                # print(content_len)

            # buffer = conn.recv(4096)
            print('收到命令buffer')
            message = message.split(split_char.encode('utf-8'))  # 上传图片时会在转换成utf-8时出错
            # print('命令是：')
            # print('message:', message)

            if message[0] == b'Upload':  # 上传：Upload,file_id,filename,content
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                print(message[1])
                message[2] = message[2].decode('utf-8')
                file_name = os.path.join(upload_path+temp, message[2])
                message[3] = message[3].decode('utf-8')
                content = message[4]

                print('上传的文件内容是')
                print(content)

                with open(os.path.join(file_name), 'wb') as file:
                    # while True:
                    #     print(len(content))
                    #     file.write(content)
                    #     content = conn.recv(4096)
                    #     if len(content) < 4096:
                    #         break
                    #     print('3')
                    file.write(content)

                # while content:
                #     content = conn.recv(4096)
                #     print(content)
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
            if command == 'Upload':
                filepath=message[3]
                content=message[4]
              #  print(message)
                if FileUpload(content, filename, filepath):
                    print('upload success')

            elif command == 'Download':
                filepath=message[3]
                if FileDownload(fileid, filename, filepath):
                    print('download success')

            elif command == 'Delete':
                filepath=message[3]
                if FileDelete(fileid, filename, filepath):
                    print('Delete success')
                # if remove(message[1],message[2]):
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


def FileUpload(filecontent, filename, file_path):  # filepath 要上传的文件存储在中央服务器的地址
    print("开始上传")
    file_name = os.path.join(storage_path,file_path,filename)
 #   print('-----------------------------')
 #   print()
 #   print(file_name)
    with open(file_name, "wb") as file:
        file.write(filecontent)
    print("写入juicefs成功")
    send_message_to_web('Upload success')
    return True


def FileDownload(file_id, filename, file_path):
    sock_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('开始下载')
    try:
        sock_web.connect((web_ip, web_port))
        # 打开要发送的文件
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
    print("开始在JuiceFS中删除文件")
    delete_path = storage_path + filepath
    os.remove(delete_path)
    #print(filepath)
    #print(fileid)
    #print(filename)
    send_message_to_web('Delete success')
    return True

message_queue = queue.Queue()
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Example
# message_queue.put("Delete,D:\PycharmProjects\\NewDFS\\text.txt,0")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\doc.doc,1")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\md.md,2")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\pdf.pdf,3")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\mp3.mp3,4")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\vedio.mp4,5")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\en.wav,6")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\cat.jpg,7")
# message_queue.put("Upload,D:\PycharmProjects\\NewDFS\\sky.png,8")
if __name__ == "__main__":
    if use_ray:
        ray.init()
    listen_thread = Thread(target=listenning)
    handle_thread = Thread(target=handle_web_message)
    listen_thread.start()
    handle_thread.start()
    listen_thread.join()
    handle_thread.join()
