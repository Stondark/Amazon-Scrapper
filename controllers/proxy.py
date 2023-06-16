import random

class Proxy:
    
    def __init__(self):
        self.path = "./public/Proxy/"
        self.file = "Proxy.txt"
        self.proxy_ip = self.get_proxy_id(self.file)

    def get_proxy_id(self, file):
        with open(f"{self.path}/{file}") as f:
            proxy = f.read().split("\n")
            return { "http" : random.choice(proxy)}
