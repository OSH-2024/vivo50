import os
import ray
import sys
import queue
import socket
from threading import Thread
import Ray_Module
from FileSearch import IndexSearch
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
storage_path=settings["storage_path"]
use_ray=settings["use_ray"]
split_char=settings["split_char"]

def FileUpload(fileid, filename, filepath, filecontent):  # filepath 要上传的文件存储在中央服务器的地址
    jfs_path = os.path.join(storage_path + filepath,filename)  # 这个是正式存入juicefs的path
    print("开始写入JuiceFS")
    with open(jfs_path, "wb") as file:
        file.write(filecontent)
    print("写入JuiceFS成功")
    print("开始上传")
    if Ray_Module.Upload(fileid, filename, jfs_path) is False:
        print('Ray模块标签存入缓冲区错误')
        return False
    print("所有模块准备完成,开始正式写入:")
    
    if index_upload(fileid, filename, jfs_path) is False :
        print('生成向量化索引错误')
        return False
    print("生成向量化索引成功")

    if Ray_Module.Commit() is False:
        print('ray commit error')
        return False
    print("写入Ray模块成功")

    return True

def FileDelete(fileid, filename, filepath):
    print("开始删除")
    delete_path = storage_path + filepath  # 这个是要删除文件在juicefs的path
    if Ray_Module.Delete(fileid, filename, delete_path) is False:
        print('Ray模块标签存入缓冲区错误')
        return False
    print("所有模块准备完成,开始正式删除:")
    if Ray_Module.Commit() is False:
        print('ray commit error')
        return False
    print("Ray模块删除成功")

    print("删除向量化索引成功")

    print("开始在JuiceFS中删除文件")
    os.remove(delete_path)
    #print(filepath)
    #print(fileid)
    #print(filename)
    print("在JuiceFS中删除成功")
    return True

def FileSearch(query):
    print("开始查询")
    #content = '11/1.png'+split_char+'22/readme.md'
    # content = '/home/liuchang/upfile/1.png'
    print("查询的内容是:")
    print(query)
    content = IndexSearch(query)
    print("查询得到的内容是：")
    print(content)
    return content
