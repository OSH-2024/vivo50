import os
import sys
import ray
import queue
import change_json
from flask_socketio import SocketIO
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from threading import Thread
from EC_Module import erasure
from Ray_Module import ray_control


sys.path.append(os.path.dirname(sys.path[0]))#模块搜索路径
import config
setting=config.args()
settings=setting.set#得到一个集合，里面是config的值

visit_web_port=settings["visit_web_port"] #5000
absolute_path=settings["absolute_path"] #"D:\\PycharmProjects\\NewDFS\\"
split_char=settings["split_char"].encode("utf-8")

app = Flask(__name__) #初始化一个flask实例
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 禁用缓存
DOWNLOAD_FOLDER = absolute_path+'web_server\\'+'downloadfile'#下载的文件夹的路径
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
socketio = SocketIO(app)#socketio对象，集成到flask中
json_file = absolute_path+'web_server\\static\\test.json'#存储一个json文件的路径


@app.route('/')#根URL映射到index函数上，用于显示网页(index。html)
def index():
    return render_template('index.html')#渲染网页


@app.route('/upload', methods=['GET', 'POST'])#将URL为upload映射到upload_file函数上，支持get，post方法，但是好像没有处理get方法
def upload_file():
    if request.method == 'POST':
        path = request.form.get('path', '')  # 获取表单数据中的path字段 类似请求头"GET /index.html HTTP1.0"，虽然好像不是这样的
        file = request.files['file'] #获取上传的文件
        # print(path)
        if file:#如果不为空
            filename = file.filename#获得文件名
        else:
            # message_forward('文件不能为空！')
            return redirect(url_for('index'))#重定向到首页

        # file_append_JSON(path, file.filename)
        if change_json.is_file_exist(json_file, path, file.filename):#如果文件已存在，则输出错误信息并重定向到首页
            print('文件已存在')
            message_forward('文件已存在！')
            return redirect(url_for('index'))

        id = change_json.get_file_id(json_file)#这里牵涉到别的模块
        content=file.read()
        message = b'' + b'Upload' + split_char + str(id).encode('utf-8') + split_char + filename.encode('utf-8') + split_char + content
        if handle_request(message):
            print('upload to central success')
            message_forward('上传成功！')
        else:
            print('上传失败！')
            return redirect(url_for('index'))

        change_json.add_file_to_json(json_file, path, file.filename)#json文件中存了已经有的文件，所以前面可以从json文件中找文件是否存在

    return redirect(url_for('index'))#重定向到首页


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        is_dir = request.form.get('is-dir', '') #判断表单中的那个东西是不是目录
        if is_dir == 'true':
            print('不能下载文件夹')
            message_forward('不能下载文件夹！')
            return redirect(url_for('index'))
        # path = request.form.get('path', '')

        path = request.form.get('path', '') #从表单中获取文件路径
        filename = os.path.basename(path) #获取文件名
        target_path = os.path.join(app.config['DOWNLOAD_FOLDER'], #拼接得到下载路径
                                   filename)
        element_id = request.form.get('id', '') #获取表单中的id字段
        print('element:', element_id)
        id = int(element_id[7:]) #解析id，获取文件唯一标识
        print('id:',id)
        message = b'' + b'Download' + split_char + str(id).encode('utf-8') + split_char + filename.encode('utf-8')
        if handle_request(message):
            print('download from central success')
            message_forward('download success')
            return send_from_directory(app.config['DOWNLOAD_FOLDER'],
                                       filename,
                                       as_attachment=True)#则下载成功
        else:
            message_forward('下载失败！')
            print('从central server下载失败')
            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_file():
    path = request.form.get('path', '')
    is_dir = request.form.get('is-dir', '')
    element_id = request.form.get('id', '')
    fileid = int(element_id[7:])
    # print(is_dir)
    filename = os.path.basename(path)
    message = b'' + b'Delete' + split_char + str(fileid).encode('utf-8') + split_char + filename.encode('utf-8')
    if is_dir == "false":
        handle_request(message)
        change_json.remove_file_from_json(json_file, path, filename)
        print('删除文件成功')

    else:
        if not change_json.is_dir_empty(json_file, path):
            print('文件夹不为空')
            print('删除文件夹失败')
            return redirect(url_for('index'))

        change_json.remove_dir_from_json(json_file, path)  # 删除文件夹不需要后端删除文件
        print('删除文件夹成功')

    return redirect(url_for('index'))


@app.route('/new_dir', methods=['GET', 'POST'])#新建一个文件夹
def new_dir():
    if request.method == 'POST':
        path = request.form.get('path', '')
        dir_name = request.form.get('dir_name', '')#获得路径以及目录名
        if dir_name == '':
            print('文件夹不能为空')
            return redirect(url_for('index'))#重定向到主页
        change_json.add_dir_to_json(json_file, path, dir_name) # 修改json文件
        message_forward('success')
        message_forward('新建文件夹成功！')
    return redirect(url_for('index'))


@socketio.on('message')#当客户端发送名为message的消息时调用
def message_forward(msg: str):
    socketio.emit('message', msg)#向客户端发送message和msg

def handle_request(message):
            print('收到命令buffer')
            message = message.split(split_char.encode('utf-8'))  # 上传图片时会在转换成utf-8时出错
            # print('命令是：')
            # print('message:', message)

            if message[0] == b'Upload':  # 上传：Upload,file_id,filename,content
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                print(message[1])
                message[2] = message[2].decode('utf-8')
                file_name = os.path.join(absolute_path+temp+'uploadfile', message[2])
                content = message[3]

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
                message[3] = os.path.join(absolute_path+temp+'uploadfile', file_name)
                message = message[0:4]
                message_queue.put(message)
                print('upload message 已经入队')
                print(message)


            elif message[0] == b'Download':  # 下载：download,file_id,filename
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                message[2] = message[2].decode('utf-8')
                message_queue.put(message)
                print('download message 已经入队')

            elif message[0] == b'Delete':  # 删除：Delete,file_id,filename
                message[0] = message[0].decode('utf-8')
                message[1] = message[1].decode('utf-8')
                message[2] = message[2].decode('utf-8')
                message_queue.put(message)
                print('Delete message 已经入队')

            else:
                print('未定义消息')
                send_message_to_web('fail')
