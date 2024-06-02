import json


# 得到最大id
def get_max_id(data: dict):
    if not data['children']:
        return data['id']
    else:
        children_max = 0
        for children in data['children']:
            children_max = max(children_max, get_max_id(children))
        return max(children_max, data['id'])


# 得到新文件id
def get_file_id(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return get_max_id(data) + 1


# 得到工作文件夹
def get_work_dir(json_file, path, file_name):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 将路径转换为列表形式
    path = path.strip('/').split('/')

    # 遍历路径，找到要添加文件的位置
    if path == ['']:
        current_dir = data
    else:
        current_dir = data
        for folder in path:
            current_dir = next(child for child in current_dir['children']
                               if child['name'] == folder)
    return current_dir


# 判断是否有重名文件
def is_file_exist(json_file, path, file_name):
    current_dir = get_work_dir(json_file, path, file_name)
    if any(file['name'] == file_name for file in current_dir['children']):
        return True  # 存在同名文件，返回 False
    else:
        return False


def add_file_to_json(json_file, path, file_name):
    # 读取JSON文件并解析为Python对象
    with open(json_file, 'r') as f:
        data = json.load(f)
    new_file_id = get_max_id(data) + 1

    # current_dir = get_work_dir(json_file, path, file_name)
    # print(current_dir)
    # 将路径转换为列表形式
    path = path.strip('/').split('/')

    # 遍历路径，找到要添加文件的位置
    if path == ['']:
        current_dir = data
    else:
        current_dir = data
        for folder in path:
            current_dir = next(child for child in current_dir['children']
                               if child['name'] == folder)

    if any(file['name'] == file_name for file in current_dir['children']):
        return False  # 存在同名文件，返回 False
    # 创建新的文件对象并添加到路径中
    new_file = {
        'id': new_file_id,
        'name': file_name,
        'isdir': False,
        'children': []
    }
    # print(new_file)
    current_dir['children'].append(new_file)

    # 将更新后的Python对象转换回JSON格式
    updated_json = json.dumps(data, indent=4)

    # 将更新后的JSON写入原始文件或另存为新文件
    with open(json_file, 'w') as f:
        f.write(updated_json)

    print('add file to json success')
    return True


def add_dir_to_json(json_file, path, folder_name):
    # 读取JSON文件并解析为Python对象
    with open(json_file, 'r') as f:
        data = json.load(f)
    new_file_id = get_max_id(data) + 1
    # 将路径转换为列表形式
    path = path.strip('/').split('/')

    # 遍历路径，找到要添加文件的位置
    if path == ['']:
        current_dir = data
    else:
        current_dir = data
        for folder in path:
            current_dir = next(child for child in current_dir['children']
                               if child['name'] == folder)
    if any(file['name'] == folder_name for file in current_dir['children']):
        return False  # 存在同名文件，返回 False
    # 创建新的文件对象并添加到路径中
    new_file = {
        'id': new_file_id,
        'name': folder_name,
        'isdir': True,
        'children': []
    }
    current_dir['children'].append(new_file)

    # 将更新后的Python对象转换回JSON格式
    updated_json = json.dumps(data, indent=4)

    # 将更新后的JSON写入原始文件或另存为新文件
    with open(json_file, 'w') as f:
        f.write(updated_json)
    return True, new_file_id


def remove_file_from_json(json_file, path, file_name):
    with open(json_file, 'r') as f:
        data = json.load(f)
    path = path.strip('/').split('/')[:-1]
    # 遍历路径，找到要删除文件的位置
    if path == ['']:
        current_dir = data
    else:
        current_dir = data
        for folder in path:
            current_dir = next(child for child in current_dir['children']
                               if child['name'] == folder)
    # 查找要删除的文件并从列表中移除
    file_to_remove = next(child for child in current_dir['children']
                          if child['name'] == file_name)
    current_dir['children'].remove(file_to_remove)

    # 将更新后的Python对象转换回JSON格式
    updated_json = json.dumps(data, indent=4)

    # 将更新后的JSON写入原始文件或另存为新文件
    with open(json_file, 'w') as f:
        f.write(updated_json)


def remove_dir_from_json(json_file, path):
    with open(json_file, 'r') as f:
        data = json.load(f)
    path = path.strip('/').split('/')
    dir_name = path[-1]
    path.pop()
    # 遍历路径，找到要删除文件夹的位置
    if path == ['']:
        current_dir = data
    else:
        current_dir = data
        for folder in path:
            current_dir = next(child for child in current_dir['children']
                               if child['name'] == folder)

    # if current_dir['children']:
    #     return False  # 文件夹不为空，返回 False

    # 查找要删除的文件夹并从列表中移除
    folder_to_remove = next(child for child in current_dir['children']
                            if child['name'] == dir_name)

    # folder_to_remove = current_dir

    current_dir['children'].remove(folder_to_remove)

    # 将更新后的Python对象转换回JSON格式
    updated_json = json.dumps(data, indent=4)

    # 将更新后的JSON写入原始文件或另存为新文件
    with open(json_file, 'w') as f:
        f.write(updated_json)


# def find_all_files(json_file, path):
#     with open(json_file, 'r') as f:
#         data = json.load(f)
#     path = path.strip('/').split('/')


def is_dir_empty(json_file, path):
    with open(json_file, 'r') as f:
        data = json.load(f)
    path = path.strip('/').split('/')
    # 遍历路径，找到要删除文件夹的位置
    if path == ['']:
        current_dir = data
    else:
        current_dir = data
        for folder in path:
            current_dir = next(child for child in current_dir['children']
                               if child['name'] == folder)
    if current_dir['children']:
        return False
    else:
        return True
