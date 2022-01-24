import requests
import time
import random
import json
from hashlib import md5

from_lang = 'auto'
to_lang = 'en'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path


class Translater:
    id_pools = []
    _cur = 0
    sleep_time = 3

    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def add_key(self, appid, appkey):
        dict = {}
        dict['appid'] = appid
        dict['appkey'] = appkey
        self.id_pools.append(dict)
        self.sleep_time = 3.0 / len(self.id_pools)

    def translate(self, query):
        """
        翻译送入的语句
        :param query: str
        :return: str
        """
        if len(self.id_pools) == 0:
            raise Exception("id_pools cannot be empty!\n")

        error_code = 0
        res_str = ''

        while (error_code != 52000):
            appid = self.id_pools[self._cur]['appid']
            appkey = self.id_pools[self._cur]['appkey']
            res = self.trans(query, appid, appkey)
            error_code = res[0]
            res_str = res[1]
            self._cur = (self._cur + 1) % len(self.id_pools)
            if error_code != 52000:
                time.sleep(self.sleep_time)

        return res_str

    # return [error_code, res_str]
    def trans(self, query, appid, appkey):
        salt = random.randint(32768, 65536)
        sign = self.make_md5(appid + query + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        json_result = r.json()

        result = json.loads(json.dumps(json_result, ensure_ascii=False))  # add ensure_ascii

        error_code = result.get('error_code', 52000)
        if (error_code != 52000):
            return [error_code, '']
        else:
            trans_result = result['trans_result']

            res_str = ""
            for item in trans_result:
                res_str += item['dst']
                res_str += '\n'

            return [error_code, res_str]
