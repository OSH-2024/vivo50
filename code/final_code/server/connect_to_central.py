import os
import sys
import socket
import json
import change_json

import Central_Module

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
json_file = settings["json_path"]
json_file2 = settings["json_path2"]
upload_path = settings["upload_path"]

split_char=settings["split_char"].encode("utf-8")   # 将settings["split_char"]按照UTF-8编码转换为字节串，并将结果赋值给split_char变量。

def upload_to_central(fileid, filename, file, filepath):      # 把文件上传到中央服务器 fileid:json中的编号  filename:file名字  file:打开的文件对象
    success = Central_Module.FileUpload(fileid, filename, filepath, file.read())
    print('上传成功' if success else '上传失败')
    return success

def Delete_to_central(fileid, filename, filepath):
    success = Central_Module.FileDelete(fileid, filename, filepath)
    print('删除成功' if success else '删除失败')
    return success


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

def Search_to_central(query):      # 向中央服务器传送查询命令
    content = Central_Module.FileSearch(query)
    if content == b'search error':
        print('搜索失败')
        return False
    print('已接收到central server的回复')

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


    parts = content.split(split_char) 

    for part in parts:
        str_part = part.decode('utf-8')
        str_part = str_part[len(upload_path)+1:]
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
    return True
