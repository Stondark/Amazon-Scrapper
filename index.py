import random
import requests
import time
import os
from bs4 import BeautifulSoup

def get_randompath(path):
    return random.choice(os.listdir(path))


def get_useragent(path):
    with open(f"./Agents/{path}") as f:
        agent = f.read().split("\n")
        return random.choice(agent)

def get_html(url, headers, proxie, cookies):
    response = requests.get(url, headers = headers, proxies = proxie, cookies = cookies)
    return BeautifulSoup(response.content, 'html.parser')

def get_proxy():
    with open("./Proxy/Proxy.txt") as f:
        proxy = f.read().split("\n")
        return { "http" : random.choice(proxy)}
    
def get_values_html(dic):
    for k, v in dic.items():
        attempts = 0
        while v["value"] is None and attempts < 3:
            v_html = html.select_one(v["selector"])
            if(v_html != None):
                v["value"] = v_html.get_text().strip()
            time.sleep(1)
            attempts += 1

    return dic

url = 'https://www.amazon.com/-/es/gp/product/B07W956JBC/ref=ewc_pr_img_4?smid=A2XZ7JICGUQ1CX&psc=1'
path = get_randompath("./Agents")
proxy = get_proxy()

headers = {
    'User-Agent': get_useragent(path),
    'Accept-Language': "es-ES,es;q=0.9"
}

cookies = {
    "i18n-prefs" : "COP"
}

html = get_html(url, headers, proxy, cookies)

values = {
    "price": {
        "selector": ".a-offscreen",
        "value": None
    },
    "title": {
        "selector": "#productTitle",
        "value": None
    },
    "description": {
        "selector": "#productDescription > p > span",
        "value": None
    }
}
values_html = get_values_html(values)

for k, v in values_html.items():
    print(k.upper()," : ", v["value"])

