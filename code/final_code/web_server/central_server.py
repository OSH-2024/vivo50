import os
import sys
import socket
import json
import ray
import queue
from threading import Thread
import Ray_Module 
from FileSearch import IndexSearch, ImageSearch, SimilarSearch
from tag_server import index_upload
import change_json

sys.path.append(os.path.dirname(sys.path[0]))   # 将当前脚本的父目录添加到sys.path列表中。sys.path列表用于确定Python在导入模块时搜索的位置
import config                               # 导入config模块的内容
setting=config.args()
settings=setting.set                            # 把config中的内容导入settings
# 上传：Upload,fileid,filename,filepath,content
# 下载：Download,fileid,filename,filepath
# 删除：Delete,fileid,filename,filepath

json_file = settings["json_path"]
json_file2 = settings["json_path2"]
upload_path = settings["upload_path"]
storage_path  = settings["storage_path"]

split_char=settings["split_char"]   # 将settings["split_char"]按照UTF-8编码转换为字节串，并将结果赋值给split_char变量。

def upload_to_central(fileid, filename, file, filepath):      # 把文件上传到中央服务器 fileid:json中的编号  filename:file名字  file:打开的文件对象
    fileid = str(fileid)
    print("upload进程pid是" + str(os.getpid()))      # 打印当前进程的pid
    print("开始上传")
    file_name = os.path.join(storage_path + filepath,filename)  # 这个是正式存入juicefs的path
    tmpfile_path = os.path.join(upload_path + filepath,filename)  # 这个是上传文件的缓冲区路径
    content = file.read()
    print('上传的文件内容是')
    print(content)
    with open(tmpfile_path, 'wb') as file:
        file.write(content)
        print('已写入缓冲区')

    if Ray_Module.Upload(fileid, filename, tmpfile_path) is False:
        print('Ray模块标签存入缓冲区错误')
        return False
    print("所有模块准备完成,开始正式写入:")
    
    if index_upload(fileid, filename, tmpfile_path) is False :
        print('生成向量化索引错误')
        return False
    print("生成向量化索引成功")

    if Ray_Module.Commit() is False:
        print('ray commit error')
        return False
    print("写入Ray模块成功")

    print("开始写入JuiceFS")
 #   print('-----------------------------')
 #   print()
 #   print(file_name)

    with open(file_name, "wb") as file:
        file.write(content)
    print("写入JuiceFS成功")
    
    return True




def download_to_central(fileid, filename, targetpath, filepath):
    print('开始下载')
    content = ''
    # 打开要发送的文件
    file_path = os.path.join(storage_path, filepath)
    with open(file_path, 'rb') as file:
        # 读取文件内容
        content = file.read()
    print("文件发送完成")
    with open(targetpath, 'wb') as f:
        f.write(content)
    print('下载成功')
    return True


def Delete_to_central(fileid, filename, filepath):
    print("开始删除")
    delete_path = storage_path + filepath  # 这个是要删除文件在juicefs的path
    tmpfile_path = upload_path + filepath  # 这个是要删除文件的缓冲区路径,是包括文件名的
    if Ray_Module.Delete(fileid, filename, tmpfile_path) is False:
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
    os.remove(tmpfile_path)
    #print(filepath)
    #print(fileid)
    #print(filename)
    print("在JuiceFS中删除成功")
    return True


def add_new_file(filepath, filename):
    parts = filepath.split('/')
    pathbefore = ""
    pathnow = ""
    for i, part in enumerate(parts):
        pathnow = pathnow + "/" + part
        change_json.add_dir_to_json(json_file2, pathbefore, part)
        if i > 0:
            print(pathbefore)
            print(part)
        pathbefore = pathbefore + "/" + part
        
    fileid = change_json.get_file_id(json_file2)
    change_json.add_file_to_json(json_file2, filepath, filename)
    return True


def postprocess_search(parts):
    print("查询得到的内容是：")
    print(parts)
    data = {
        "id": 1,
        "name": "/",
        "isdir": True,
        "children": []
    }

    # 清空文件内容
    with open(json_file2, "w") as file:
        file.write("")

    # 写入新的 JSON 数据
    with open(json_file2, "w") as file:
        json.dump(data, file, indent=4)
    #to be done
        
    print('成功得到搜索结果')

    for part in parts:
        str_part = part[len(upload_path)+1:]
        print("搜索结果为：")
        print(str_part)
        split_index = str_part.rfind('/') 
        if split_index != -1:
            part1 = str_part[:split_index]  # 切割第一部分
            part2 = str_part[split_index + 1:]  # 切割第二部分
            add_new_file(part1,part2)
            change_json.change_path_id(json_file,json_file2,part1,part2)
        else:
            change_json.add_file_to_json(json_file2, '', str_part)
            change_json.change_path_id(json_file,json_file2,'', str_part)
    
    print('成功写入json文件')
    return True



def Search_to_central(query):      # 向中央服务器传送查询命令
    print("开始查询")
    #content = '11/1.png'+split_char+'22/readme.md'
    # content = '/home/liuchang/upfile/1.png'
    print("查询的内容是:")
    print(query)
    parts = IndexSearch(query)
    return postprocess_search(parts)

def Image_search(file):
    filename = file.filename
    content = file.read()
    print("开始图片查询, 文件名:",filename)
    tmpfile_path = os.path.join(upload_path + '/tmp', filename) # Temp path to hold image file
    with open(tmpfile_path, 'wb') as file:
        file.write(content)
        print('图片已写入缓冲区')
    parts = ImageSearch(tmpfile_path)
    return postprocess_search(parts)

def Similar(fileid):
    print(f"查询相似文件, fileid = {fileid}...")
    parts = SimilarSearch(fileid)
    return postprocess_search(parts)