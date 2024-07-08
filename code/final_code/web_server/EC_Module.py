from zfec.easyfec import Encoder, Decoder
import random
import base64
import os
import sys
import socket
import json

sys.path.append(os.path.dirname(sys.path[0]))   # 将当前脚本的父目录添加到sys.path列表中。sys.path列表用于确定Python在导入模块时搜索的位置
import config                               # 导入config模块的内容
setting=config.args()
settings=setting.set     
storage_path  = settings["storage_path"]
split_char=settings["split_char"]

# 使用m个数据块的任意k个都可以恢复原来的数据
def EC_upload(k, m, filepath,  content):
	print("开始生成纠删码")
	enc = Encoder(k, m)
	data = content
    
	if len(data) % k != 0:
		padlen = (len(data)//k) - len(data)%k
	else: padlen = 0
   
	byte_array = enc.encode(data)
	print(byte_array)
	
	for i in range(0, m):
		tmp_filepath = filepath + '_' + str(i)
		with open(tmp_filepath, "wb") as file:
			file.write(byte_array[i])
	

	tmp_filepath = filepath + '_' + "len"
	with open(tmp_filepath, "w") as file:
		file.write(str(padlen))
	print("写入纠删码成功")

def EC_delete(k, m, filepath):
	for i in range(0, m):
		tmp_filepath = filepath + '_' + str(i)
		os.remove(tmp_filepath)
	tmp_filepath = filepath + '_' + "len"
	os.remove(tmp_filepath)

def EC_download(k, m, filepath):
	dec = Decoder(k, m)
	tmp_filepath = filepath + '_' + "len"
	padlen = int(0)
	data = ''
	with open(tmp_filepath, 'r') as file:
		data = file.read()
		padlen = int(data)
	data = b''
	tmp_filepath = filepath + '_' + '0'
	with open(tmp_filepath, 'rb') as file:
		data = file.read()
	byte_array1 = data
	tmp_filepath = filepath + '_' + '1'
	with open(tmp_filepath, 'rb') as file:
		data = file.read()
	byte_array2 = data
	tmp_filepath = filepath + '_' + '3'
	with open(tmp_filepath, 'rb') as file:
		data = file.read()
	byte_array3 = data
    # decode, need pass in the blocks + blocknums and padlen
	blocks = (byte_array1 ,byte_array2, byte_array3)
	blocknums = (0, 1, 3)

	decoded = dec.decode(blocks, sharenums=blocknums,padlen=padlen)
	
	return decoded

