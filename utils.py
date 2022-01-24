import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup
import re
from langdetect import detect
import text2text as t2t
import requests
import hashlib
import random

# APP ID
appID = '20211109000995394'
# 密钥
secretKey = 'b9xwuX_bCSwxaz0EWmG3'
# 百度翻译 API 的 HTTP 接口
apiURL = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

def gettext(list):
    """
    将list数据转换成text字符串，去除非文本数据，去除html标签
    :param list: list
    :return: str
    """
    tokemodel = BeautifulSoup(list)
    return tokemodel.get_text()


def text_process(text):
    """
    去除标点符号，数字
    :param text: str
    :return: str
    """
    letters_only = re.sub("[^a-zA-Z]",  # The pattern to search for
                          " ",  # The pattern to replace it with
                          text)  # The text to search
    return letters_only

def getwords(text):
    """
    将处理好的（去除标点的文本）转化为词列表，将字母大小写改进，全部改为小写
    :param text: str
    :return: list
    """
    text = text.lower()
    words = text.split()
    return words

def lang_detect(text):
    """
    检测语言类型，返回str
    :param text: str
    :return: 语言类型 str
    """
    return detect(text)

def translate(text):
    """
    传送str数据，返回翻译后的str
    :param text: str
    :return: str
    """
    t2t.Transformer.PRETRAINED_TRANSLATOR = "facebook/m2m100_418M"
    lines = text.split('\n')
    from_lang = detect(lines[0])
    tgt_text = ''
    for line in lines:
        tgt_text = tgt_text + t2t.Handler(line, src_lang=from_lang).translate(tgt_lang='en')[0]
    return tgt_text



def baiduAPI_translate(query_str):
    '''
    传入待翻译的字符串和目标语言类型，请求 apiURL，自动检测传入的语言类型获得翻译结果
    :param query_str: 待翻译的字符串
    :param to_lang: 目标语言类型
    :return: 翻译结果字典
    '''
    # 生成随机的 salt 值
    salt = str(random.randint(32768, 65536))
    # 准备计算 sign 值需要的字符串
    pre_sign = appID + query_str + salt + secretKey
    # 计算 md5 生成 sign
    sign = hashlib.md5(pre_sign.encode()).hexdigest()
    # 请求 apiURL 所有需要的参数
    params = {
        'q': query_str,
        'from': 'auto',
        'to': 'en',
        'appid': appID,
        'salt':salt,
        'sign': sign
    }
    try:
        # 直接将 params 和 apiURL 一起传入 requests.get() 函数
        response = requests.get(apiURL, params=params)
        # 获取返回的 json 数据
        result_dict = response.json()
        # 得到的结果正常则 return
        if 'trans_result' in result_dict:
            return result_dict
        else:
            print('Some errors occured:\n', result_dict)
    except Exception as e:
        print('Some errors occured: ', e)


def baiduAPI_translate_main(query_str):
    '''
    解析翻译结果后输出，默认实现英汉互译
    :param query_str: 待翻译的字符串，必填
    :return: 翻译后的字符串
    '''
    if query_str.isspace():
        return ''
    if len(query_str)==0:
        return ''
    result_dict = baiduAPI_translate(query_str)
    # 提取翻译结果字符串，并输出返回
    dst = result_dict['trans_result'][0]['dst']
    return dst






