import json
import time
from Translater import Translater

t = Translater()
t.add_key('20211118001002297', 'f7GiqbfxoJWsxaQ0ZtlH')
t.add_key('20211119001003651', 'NSm4EPbGpI7E4SATt_LG')
t.add_key('20211109000995394', 'b9xwuX_bCSwxaz0EWmG3')
t.add_key('20211119001003693', 'ZJAHpYtcIkYA_Vf0d3HR')

try:
    with open('./dataset/test_en.json', 'r') as f:
        target = json.load(f)
except:
    target = []

with open('./dataset/test.json', 'r') as f:
    src = json.load(f)


def save():
    # 写入 JSON 数据
    with open('./dataset/test_en.json', 'w') as f:
        json.dump(target, f, ensure_ascii=False)


def spilt(str, n):
    list = [str[i:i + n] for i in range(0, len(str), n)]
    return list


n = len(target)
MAX_LEN = 4500
i = 0
rest = len(src) - n

for item in src[n:]:
    i = i + 1

    print('第{0}篇文章翻译开始'.format(len(target) + 1))
    item_zh = {}
    content = item['content']
    list = spilt(content, MAX_LEN)
    item_zh['content'] = ""
    #item_zh['label'] = item['label']

    for part in list:
        item_zh['content'] += t.translate(part)
        time.sleep(0.25)

    target.append(item_zh)
    print('第{0}篇文章翻译结束'.format(len(target)))

    if i % 5 == 0:
        save()
        print('文件已保存！当前进度：{0}/{1}'.format(len(target), len(src)))
    if i == rest:
        save()
        print('文件已保存！当前进度：{0}/{1}'.format(len(target), len(src)))
        print('我退出啦')
        break







