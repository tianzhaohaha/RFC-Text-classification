import json

def load_file(filename):
    """
    以字典的形式取出训练集与测试集
    :param filename:
    :return: dict
    """
    with open(filename, 'r', encoding="UTF-8") as f:
        data = json.load(f)
        f.close()
    print("File is successfully loaded" + filename)
    return data

def dump_file(filename, data):
    """
    保存文件为json格式
    :param filename: 文件路径
    :param data: 字典
    :return:
    """
    with open(filename, 'w', encoding="UTF-8") as f:
        json.dump(data,f)
        f.close()
    print("File is successfully saved!"+filename)
    return