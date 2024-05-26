import os
import sys
import change_json
import connect_to_central
from flask_socketio import SocketIO
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

sys.path.append(os.path.dirname(sys.path[0]))
import config
setting=config.args()
settings=setting.set

visit_web_port=settings["visit_web_port"]
absolute_path=settings["absolute_path"]

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 禁用缓存
DOWNLOAD_FOLDER = absolute_path+'web_server\\'+'downloadfile'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
socketio = SocketIO(app)
json_file = absolute_path+'web_server\\static\\test.json'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        path = request.form.get('path', '')  # 获取表单数据中的path字段
        file = request.files['file']
        # print(path)
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

        id = change_json.get_file_id(json_file)

        if connect_to_central.upload_to_central(id, filename, file):
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
        filename = os.path.basename(path)
        target_path = os.path.join(app.config['DOWNLOAD_FOLDER'],
                                   filename)
        element_id = request.form.get('id', '')
        print('element:', element_id)
        id = int(element_id[7:])
        print('id:',id)
        if connect_to_central.download_to_central(id, filename, target_path):
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
    if is_dir == "false":
        connect_to_central.Delete_to_central(fileid, filename)
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


@app.route('/new_dir', methods=['GET', 'POST'])
def new_dir():
    if request.method == 'POST':
        path = request.form.get('path', '')
        dir_name = request.form.get('dir_name', '')
        if dir_name == '':
            print('文件夹不能为空')
            return redirect(url_for('index'))
        change_json.add_dir_to_json(json_file, path, dir_name)
        message_forward('success')
        message_forward('新建文件夹成功！')
    return redirect(url_for('index'))


@socketio.on('message')
def message_forward(msg: str):
    socketio.emit('message', msg)


if __name__ == '__main__':
    print("进程pid是"+str(os.getpid()))
    app.run(host='0.0.0.0', port=visit_web_port)
