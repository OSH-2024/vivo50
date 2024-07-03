import os
import ray
import time
import re
import cv2
import sys
import torch
import openai
import markdown
import enchant
import slate3k as slate
import speech_recognition as sr
from docx import Document
from keybert import KeyBERT
from pydub import AudioSegment
import jieba.analyse
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from collections import Counter

sys.path.append(os.path.dirname(sys.path[0]))
import config
from imgtagging import solve
from speech2txt import beginchange
setting=config.args()
settings=setting.set
spell_checker = enchant.Dict("en_US")
download_path=settings["download_path"]
temp="..\\temp\\"


Stime = time.perf_counter()

# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
@ray.remote
def txt_tagging(file_path, keywords_num=10):
    keywords_num=int(keywords_num)
    print("     ----Check----keywords_num:" + str(keywords_num))
    return text_tag(file_path,keywords_num)

@ray.remote
def pdf_tagging(file_path, keywords_num=10):
    pdf2txt.remote(file_path,"pdf2txt.txt")
    print("格式转换成功")
    return ray.get(txt_tagging.remote("pdf2txt.txt",keywords_num))

@ray.remote
def md_tagging(file_path, keywords_num=10):
    md2txt.remote(file_path, "md2txt.txt")
    print("格式转换成功")
    return ray.get(txt_tagging.remote("md2txt.txt",keywords_num))
@ray.remote
def doc_tagging(file_path, keywords_num=10):
    doc2txt.remote(file_path, "doc2txt.txt")
    print("格式转换成功")
    return ray.get(txt_tagging.remote("doc2txt.txt",keywords_num))

@ray.remote
def img_tagging(file_path, keywords_num=10):
    print("     ----Check----keywords_num:"+str(keywords_num))
    return solve(file_path)

def count_and_sort(lst):
    # 统计元素出现的次数
    counter = Counter(lst)
    # 按照统计次数从多到少排序
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return sorted_items


@ray.remote
def mp4_tagging(file_path,save_path='img_save',keywords_num=10):
    img_num=ray.get(vedio2img.remote(file_path,save_path,keywords_num))
    tags = []
    results_refs = []
    for i in range(img_num):
        results_refs.append(img_tagging.remote(save_path + "/" + str(i) + ".jpg", keywords_num))
    results, _ = ray.wait(results_refs, num_returns=len(results_refs))  # 等待所有子任务完成并获取结果
    for result in results:
        result = eval(ray.get(result))
        for item in result:
            tags.append(item)
    final_tags = []
    sorted_tags = count_and_sort(tags)
    for item, count in sorted_tags:
        final_tags.append(item)
    print("     ----Check----tags:" + str(list(sorted_tags)[0:keywords_num]))
    print("     ----Check----tags:" + str(list(final_tags)[0:keywords_num]))
    return repr(list(final_tags)[0:keywords_num])

@ray.remote
def wav_tagging(file_path,keywords_num=10):
    ray.get(speech2text.remote(file_path,"wav2txt.txt"))
    return ray.get(txt_tagging.remote("wav2txt.txt",keywords_num))

@ray.remote
def mp3_tagging(file_path,keywords_num=10):
    mp32wav.remote(file_path, "mp32wav.wav")
    print("格式转换成功")
    return ray.get(wav_tagging.remote("mp32wav.wav", keywords_num))

@ray.remote
def code_tagging(file_path,keywords_num=10):
    code2txt(file_path,temp+"code2txt.txt")
    tags = txt_tagging(temp+"code2txt.txt", keywords_num)
    # print("     ----Check----tags:" + str(tags))
    return tags

@ray.remote
def pdf2txt(pdf_path, txt_path):
    text = extract_text(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as txt:
        txt.write(text)

@ray.remote
def doc2txt(doc_file, txt_file):
    doc = Document(doc_file)
    with open(txt_file, 'w', encoding='utf-8') as f:
        for paragraph in doc.paragraphs:
            f.write(paragraph.text + '\n')

@ray.remote
def md2txt(md_path, txt_path):
    # 读取Markdown文件内容
    with open(md_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    # 将Markdown文本转换为HTML
    html = markdown.markdown(markdown_text)
    # 去除HTML标签，将其转换为纯文本
    text = ''.join(html.strip().split('<'))
    # 将转换后的文本写入txt文件
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(text)

@ray.remote
def vedio2img(file_path,save_path,keywords_num):
    def save_img(img, addr, num):
        naddr = "%s/%d.jpg" % (addr, num)
        ret = cv2.imwrite(naddr, img)
        return ret
    srcFile = file_path
    dstDir = save_path
    if not os.path.isdir(dstDir):
        os.mkdir(dstDir)
    videoCapture = cv2.VideoCapture(srcFile)
    total_frames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    print("视频帧数: ", total_frames)
    isOK, frame = videoCapture.read()
    i = 0
    count=0
    while isOK:
        i = i + 1
        if i % int(total_frames / keywords_num) == 0:
            if not save_img(frame, dstDir, count):
                print("error occur!")
                break
            count+=1
        isOK, frame = videoCapture.read()
    videoCapture.release()
    return count

@ray.remote
def speech2txt(filepath,savepath):
    tmppath = "hahahahaha.txt"
    beginchange(filepath,tmppath)
    # 打开文件并读取内容
    res = ""
    with open(tmppath, "r") as f:
        orderResult = json.load(f)["content"]["orderResult"]
        lattice = json.loads(orderResult)["lattice"]
        json_1bests = [json.loads(item["json_1best"]) for item in lattice]
        #print(json_1bests)
    for s in json_1bests: # sentence (?)
        for w in s['st']['rt'][0]['ws']: # word
            res += w['cw'][0]['w']
            if w['cw'][0]['wp'] == 'g':
                res += '\n'
    with open(savepath, 'w') as file:
        file.write(res)

@ray.remote
def mp32wav(mp3_file, wav_file):
    # 读取MP3文件
    audio = AudioSegment.from_file(mp3_file, format='mp3')
    # 导出为WAV文件
    audio.export(wav_file, format='wav')

@ray.remote
def code2txt(code_file, txt_file):
    with open(code_file, "r", encoding="utf-8") as f:
        content = f.read()
    with open(txt_file,"w") as f:
        f.write(content)
    print("代码转文本成功")

def tagging(file_path,keywords_num=10):
    print("开始打标")
    tagging_function_table={
        "txt":txt_tagging,
        "doc":doc_tagging,
        "md":md_tagging,
        "pdf":pdf_tagging,
        "jpg":img_tagging,
        "png":img_tagging,
        "wav":wav_tagging,
        "mp3":mp3_tagging,
        "mp4":mp4_tagging,
        "c":code_tagging,
        "cpp": code_tagging,
        "java":code_tagging,
        "py":code_tagging,
        "html":code_tagging
    }
    temp=file_path
    _, filename = os.path.split(temp)
    file_ext=filename.split(".")[-1]
    print("     ----Check:ext----:"+str(file_ext))
    print("     ----Check:path----:"+str(file_path))
    tagging_function=tagging_function_table[file_ext]
    ID=tagging_function.remote(file_path)
    keywords=ray.get(ID)
    print("打标结束:"+str(keywords))
    return keywords

if __name__ == "__main__":
    # tagging("1.txt",keywords_num=10)
    # tagging("1.doc",keywords_num=10)
    # tagging("1.md",keywords_num=10)
    # tagging("dogs' friend.pdf",keywords_num=10)
    # tagging("dog0.jpg",keywords_num=10)
    # tagging("1.png",keywords_num=10)
    tagging("1.mp4",keywords_num=10)

    # tagging("1.wav",keywords_num=10)
    # tagging("1.mp3",keywords_num=10)
    # tagging("test.py",keywords_num=10)
    print(f"Finished in {time.perf_counter()-Stime:.2f}")
    pass
