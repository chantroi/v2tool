from deta import Deta
from threading import Thread
import requests
import os
import time

deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")
proxy = "http://127.0.0.1:10808"#.format(os.getenv('PROXY'))

def test_proxy():
    start_time = time.time()
    while True:
        if time.time() - start_time >= 3:
            del os.environ["http_proxy"]
            del os.environ["https_proxy"]
            return False
        try:
            requests.get("https://www.google.com/generate_204", timeout=1)
            return True
        except Exception:
            continue

class Proxy:
    @staticmethod
    def add(config):
        db.put(key="proxy", data=config)
        os.system(f"./lite -p 10808 {config} &")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        return test_proxy()
        
    @staticmethod
    def run():
        config = db.get("proxy")["value"]
        os.system(f"./lite -p 10808 {config} &")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        return test_proxy()

def get_data(filename):
    entry = db.get(filename)
    if entry:
        return entry['urls']
    else:
        raise Exception("Không tìm thấy dữ liệu")