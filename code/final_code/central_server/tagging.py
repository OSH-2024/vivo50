import ray
import torch
import os
import cv2
import markdown
import speech_recognition as sr
from docx import Document
from keybert import KeyBERT
from pydub import AudioSegment
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
# from pdfminer.high_level import extract_text


download_path="D:\\PycharmProjects\\NewDFS\\"
temp="temp\\"
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
@ray.remote
def txt_tagging(file_path, keywords_num=10):
    keywords_num=int(keywords_num)
    torch.cuda.is_available = lambda: False
    kw_model = KeyBERT(model='distilbert-base-nli-mean-tokens')
    # kw_model = KeyBERT(model='paraphrase-MiniLM-L6-v2')
    with open(file_path, "r") as f:
        text = f.read()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), top_n=keywords_num)
    return repr(list(keywords))

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
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    # 设置Clarifai的API密钥
    api_key = 'bd56672a34a84a94a103b9847b2a28b2'
    application_id="Vivo50"
    # 验证
    metadata = (("authorization", f"Key {api_key}"),)
    request = service_pb2.PostModelOutputsRequest(
        model_id="general-image-recognition",
        user_app_id=resources_pb2.UserAppIDSet(app_id=application_id),
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes))
            )
        ],
    )
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        print(response)
        raise Exception(f"请求失败,状态码为: {response.status}")
    # for concept in response.outputs[0].data.concepts:
    #     print("%12s: %.2f" % (concept.name, concept.value))
    keywords=[]
    for concept in response.outputs[0].data.concepts[0:keywords_num]:
        keywords.append(str(concept.name))
    return repr(list(keywords[:keywords_num]))

@ray.remote
def mp4_tagging(file_path,save_path='img_save',keywords_num=10):
    img_num=ray.get(vedio2img.remote(file_path,save_path,keywords_num))
    tags=[]
    for i in range(img_num):
        results=ray.get(img_tagging.remote(save_path+"/"+str(i)+".jpg",keywords_num))
        results=eval(results)
        # print("     ----Check----results:"+str(results))
        for result in results:
            if result not in tags:
                tags.append(result)
    return repr(list(tags))

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
def speech2text(filepath,savepath):
    r = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        #得到语音数据
        audio = r.record(source)
    print("进行语音识别")
    text=r.recognize_sphinx(audio)
    print("音频转文字成功")
    with open(savepath,"w") as f:
        f.write(text)

@ray.remote
def mp32wav(mp3_file, wav_file):
    # 读取MP3文件
    audio = AudioSegment.from_file(mp3_file, format='mp3')
    # 导出为WAV文件
    audio.export(wav_file, format='wav')

def tagging(file_path):
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
        "mp4":mp4_tagging
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
    # tagging("text.txt")
    # tagging("doc.doc")
    # tagging("md.md")
    # tagging("pdf.pdf")
    # tagging("cat.jpg")
    # tagging("sky.png")
    # tagging("en.wav")
    # tagging("mp3.mp3")
    # tagging("vedio.mp4")
    pass