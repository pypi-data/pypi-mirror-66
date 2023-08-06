from time import time
import requests
from json import loads, dumps

HEADERS = {
    'User-Agent': 'Cloud Var Python Client'
}


class Var:
    def __init__(self, var_name):
        self.url = "http://api.wonderbits.cn/var"
        self.var_name = var_name    # instance variable unique to each instance
        self.session = requests.Session()
        self.session.headers = HEADERS
        self.time = 0

    def update(self, value):
        r = self.session.post(self.url, json={
            'name': self.var_name, 'value': value})
        self.time += r.elapsed.microseconds

    def get(self, rank=1):
        if rank < 1:
            raise Exception("位置从1开始")
        response = self.session.get(
            self.url, params={"name": self.var_name, "index": rank-1})
        self.time += response.elapsed.microseconds
        res = response.json()
        if res["code"] == 0:
            return loads(res["data"])
        else:
            return res["msg"]

    def history(self):
        response = self.session.get(
            self.url + "/history", params={"name": self.var_name})
        res = response.json()
        if res["code"] == 0:
            if len(res["data"]) == 0:
                return []
            return res["data"]
        else:
            return res["msg"]

    def __repr__(self):
        return str(self.get())


if __name__ == "__main__":
    test = [
        1235, 123.234, 'text', (123, 123), [1232, 123], {
            'k1': 123,
            'k2': 'value'
        }
    ]
    s = time()
    x = Var('x')
    for i in range(10):
        for v in test:
            x.update(v)
            data = x.get()
            print(data, type(data))

    print(time() - s)
    print(x.history())
