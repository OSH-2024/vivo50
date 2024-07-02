import os
import re
import cv2
import sys
import torch
import openai
import markdown
import enchant
import json
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

# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
def txt_tagging(file_path, keywords_num=10):
    keywords_num=int(keywords_num)
    print("     ----Check----keywords_num:" + str(keywords_num))
    #torch.cuda.is_available = lambda: False
    #model_name = 'all-MiniLM-L6-v2'
    #model_path = util.download_model(model_name)
    # kw_model = KeyBERT(model='distilbert-base-nli-mean-tokens')
    # kw_model = KeyBERT(model='paraphrase-MiniLM-L6-v2')
    #kw_model = KeyBERT()
    with open(file_path, "r",encoding="utf-8") as f:
        text = f.read()
    # print("     ----Check----text:"+str(text))
    tags = jieba.analyse.extract_tags(text, keywords_num)
    #tags = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), top_n=keywords_num)
    print("     ----Check----tags:"+str(tags))
    return repr(list(tags))

def pdf_tagging(file_path, keywords_num=10):
    pdf2txt(file_path,temp+"pdf2txt.txt")
    print("格式转换成功")
    tags=txt_tagging(temp+"pdf2txt.txt",keywords_num)
    # print("     ----Check----tags:" + str(tags))
    # return repr(list(tags))
    return tags

def md_tagging(file_path, keywords_num=10):
    md2txt(file_path, temp+"md2txt.txt")
    print("格式转换成功")
    tags=txt_tagging(temp+"md2txt.txt",keywords_num)
    # print("     ----Check----tags:" + str(tags))
    return tags

def doc_tagging(file_path, keywords_num=10):
    doc2txt(file_path, temp+"doc2txt.txt")
    print("格式转换成功")
    tags=txt_tagging(temp+"doc2txt.txt",keywords_num)
    # print("     ----Check----tags:" + str(tags))
    return tags

def img_tagging(file_path, keywords_num=10):
    print("     ----Check----keywords_num:"+str(keywords_num))
    return solve(file_path)

def count_and_sort(lst):
    # 统计元素出现的次数
    counter = Counter(lst)
    # 按照统计次数从多到少排序
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return sorted_items

def mp4_tagging(file_path,keywords_num=10,save_path=temp+'img_save'):
    img_num=vedio2img(file_path,save_path,keywords_num)
    tags = []
    final_tags = []
    for i in range(img_num):
        results=img_tagging(save_path+"/"+str(i)+".jpg",keywords_num)
        results=eval(results)
        # print("     ----Check----results:"+str(results))
        for result in results:
            tags.append(result)
    sorted_tags = count_and_sort(tags)
    for item, count in sorted_tags:
        final_tags.append(item)
    print("     ----Check----tags:" + str(list(sorted_tags)[0:keywords_num]))
    print("     ----Check----tags:" + str(list(final_tags)[0:keywords_num]))
    return repr(list(final_tags)[0:keywords_num])

def wav_tagging(file_path,keywords_num=10):
    speech2txt(file_path,temp+"wav2txt.txt")
    tags=txt_tagging(temp+"wav2txt.txt",keywords_num)
    # print("     ----Check----tags:" + str(tags))
    return tags

def mp3_tagging(file_path,keywords_num=10):
    mp32wav(file_path, temp+"mp32wav.wav")
    print("格式转换成功")
    tags=wav_tagging(temp+"mp32wav.wav", keywords_num)
    # print("     ----Check----tags:" + str(tags))
    return tags

def code_tagging(file_path,keywords_num=10):
    code2txt(file_path,temp+"code2txt.txt")
    tags = txt_tagging(temp+"code2txt.txt", keywords_num)
    # print("     ----Check----tags:" + str(tags))
    return tags

def pdf2txt(pdf_path,txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        doc = slate.PDF(pdf_file)
        text = ''.join(doc)
    txt=""
    for lines in str(text).split("\n"):
        for word in lines.split(" "):
            txt=txt+word+" "
    with open(txt_path,"w",encoding="utf-8") as f:
        f.write(txt)

def doc2txt(doc_file, txt_file):
    doc = Document(doc_file)
    with open(txt_file, 'w', encoding='utf-8') as f:
        for paragraph in doc.paragraphs:
            f.write(paragraph.text + '\n')

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

def vedio2img(file_path,save_path,keywords_num=10):
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

def mp32wav(mp3_file, wav_file):
    # 读取MP3文件
    audio = AudioSegment.from_file(mp3_file, format='mp3')
    # 导出为WAV文件
    audio.export(wav_file, format='wav')

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
    keywords=tagging_function(file_path,keywords_num)
    print("打标结束:"+str(keywords))
    return keywords

if __name__ == "__main__":
    # tagging("1.txt",keywords_num=10)
    # tagging("1.doc",keywords_num=10)
    # tagging("1.md",keywords_num=10)
    # tagging("dogs' friend.pdf",keywords_num=10)
    # tagging("dog0.jpg",keywords_num=10)
    # tagging("1.png",keywords_num=10)
    # tagging("1.mp4",keywords_num=10)

    tagging("1.wav",keywords_num=10)
    # tagging("1.mp3",keywords_num=10)
    # tagging("test.py",keywords_num=10)
    pass
