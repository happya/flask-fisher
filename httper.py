"""
author: yyi
"""
# urllib: not recommend
# requests

# api: http://t.yushu.im/
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # restful requires that the return results are in JSON format
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

