import os
import sys
import shutil   #用于删除目录
import change_json
import connect_to_central
from flask_socketio import SocketIO
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

visit_web_port=settings["visit_web_port"]
download_path=settings["download_path"]   #存储下载文件的路径
json_path=settings["json_path"]           #存储json文件的路径
storage_path=settings["storage_path"]     #本地挂载文件系统的路径

app = Flask(__name__) 
# app = Flask(__name__) 创建了一个 Flask 应用程序对象。__name__ 是一个特殊的 Python 变量，表示当前模块的名称。通过将其作为参数传递给 Flask 类，可以创建一个应用程序对象。
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 禁用缓存
DOWNLOAD_FOLDER = download_path  # DOWNLOAD_FOLDER 将用于存储下载的文件
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER  # 将下载文件的文件夹路径配置项设置为之前定义的 DOWNLOAD_FOLDER。
socketio = SocketIO(app) # 创建了一个 SocketIO 对象 socketio，用于在 Flask 应用程序中添加实时双向通信功能
json_file = json_path # 定义了一个 JSON 文件的路径 json_file，这个路径指向一个名为 test.json 的静态文件


@app.route('/') # 用于将下面的函数与根路径 '/' 关联起来。当用户访问根路径时，Flask 将会调用被装饰的函数来处理请求
def index():
    return render_template('index.html') #渲染模板文件


@app.route('/upload', methods=['GET', 'POST']) # 将下面的函数与路径 '/upload' 关联起来，并指定支持的请求方法为 GET 和 POST
def upload_file():
    if request.method == 'POST':
        path = request.form.get('path', '')  # 这个path指的是json中的路径,不包括文件名
        file = request.files['file']
        #print('-------------------------')
        #print()
        #print(path)
        if file:
            filename = file.filename
        else:
            # message_forward('文件不能为空！')
            return redirect(url_for('index'))

        # file_append_JSON(path, file.filename)
        if change_json.is_file_exist(json_file, path, file.filename):
            print('文件已存在')
            message_forward('文件已存在！')
            return redirect(url_for('index'))

        fileid = change_json.get_file_id(json_file)

        if connect_to_central.upload_to_central(fileid, filename, file, path):
            print('upload to central success')
            message_forward('上传成功！')
        else:
            print('上传失败！')
            return redirect(url_for('index'))

        change_json.add_file_to_json(json_file, path, file.filename)

    return redirect(url_for('index'))


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        is_dir = request.form.get('is-dir', '')
        if is_dir == 'true':
            print('不能下载文件夹')
            message_forward('不能下载文件夹！')
            return redirect(url_for('index'))
        # path = request.form.get('path', '')

        path = request.form.get('path', '')
        path = path [1:]
       # print('ggggggggggggggggggggggggg')
       # print()
       # print(path)
        filename = os.path.basename(path)
        target_path = os.path.join(app.config['DOWNLOAD_FOLDER'],filename)  # 下载到的目标路径
        element_id = request.form.get('id', '')
        print('element:', element_id)
        fileid = int(element_id[7:])
        print('id:',fileid)
        if connect_to_central.download_to_central(fileid, filename, target_path, path):
            print('download from central success')
            message_forward('download success')
            return send_from_directory(app.config['DOWNLOAD_FOLDER'],
                                       filename,
                                       as_attachment=True)
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
    #print('aaaaaaaaaaaaa')
    #print(path)
    #print(filename)
    if is_dir == "false":
        connect_to_central.Delete_to_central(fileid, filename, path)
        change_json.remove_file_from_json(json_file, path, filename)
        print('删除文件成功')
    else:
        if not change_json.is_dir_empty(json_file, path):
            print('文件夹不为空')
            print('删除文件夹失败')
            return redirect(url_for('index'))
        floder_path = storage_path + path
        print(floder_path)
        os.rmdir(floder_path)
        print('已从JuiceFS中删除目标文件夹')   
        change_json.remove_dir_from_json(json_file, path)  # 删除文件夹不需要后端删除文件
        print('删除文件夹成功')
    return redirect(url_for('index'))


@app.route('/new_dir', methods=['GET', 'POST'])
def new_dir():
    if request.method == 'POST':
        path = request.form.get('path', '')
        dir_name = request.form.get('dir_name', '')
        if dir_name == '':
            print('文件夹不能为空')
            return redirect(url_for('index'))
        change_json.add_dir_to_json(json_file, path, dir_name)
        floder_path = storage_path + '/' + path +dir_name
        #print('------------------')
        #print(floder_path)
        os.makedirs(floder_path)    #直接在juicefs的目录下创建文件夹
        message_forward('success')
        message_forward('新建文件夹成功！')
    return redirect(url_for('index'))


@socketio.on('message')
def message_forward(msg: str):
    socketio.emit('message', msg)


if __name__ == '__main__':
    print("进程pid是"+str(os.getpid()))
    app.run(host='0.0.0.0', port=visit_web_port)

