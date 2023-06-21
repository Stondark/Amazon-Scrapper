# Classes

from proxy import Proxy
from agents import Agents

# Librarys
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup

from timeit import default_timer

class Scrapper:

    def __init__(self, url):
        self.url = url
        self.proxy = Proxy().proxy_ip;
        self.agent = Agents().user_agent
        self.money = "COP"
        self.language = "es_US"
        self.cookies = {
            "i18n-prefs" : self.money,
            "lc-main": self.language
        }
        self.headers = {
            'User-Agent': self.agent
        }

    
    def set_attributtes(self, money, language):
        self.money = money
        self.cookies["i18n-prefs"]  =  money
        self.language = language
        self.headers['Accept-Language'] = language

    def get_html(self):
        response = requests.get(self.url, headers = self.headers, proxies = self.proxy, cookies = self.cookies)
        return BeautifulSoup(response.content, 'html.parser')           

    def get_values_html(self, html, values):
        # print(html)
        for i in values["products"]:
            attempts = 0
            # print(i["value"])
            while i["value"] is None and attempts < 3:
                for j in i["selector"]:
                    v_html = html.select_one(j["id"])
                    if(v_html != None):
                        if(v_html.name == 'img'):
                            i["value"] = v_html['src']
                            continue
 
                        i["value"] = v_html.get_text().strip()
                        continue

                    attempts += 1

        return values

    def scrape_product_info(self):
        values = {
            "products": [
                {
                "name": "Producto",
                "selector": [
                    {
                    "id": "#a-offscreen"
                    }
                ],
                "value": None
                },
                {
                "name": "Precio",
                "selector": [
                    {
                    "id": "#productTitle"
                    }
                ],
                "value": None
                },
                {
                "name": "Descripción",
                "selector": [
                    {
                    "id": "#productDescription > p > span"
                    }
                ],
                "value": None
                },
                {
                "name": "Calificación",
                "selector": [
                    {
                    "id": ".a-icon-alt"
                    }
                ],
                "value": None
                },
                {
                "name": "Imagen",
                "selector": [
                    {
                    "id": ".a-dynamic-image"
                    }
                ],
                "value": None
                },
                {
                "name": "Vendedor",
                "selector": [
                    {
                    "id": "#sellerProfileTriggerId"
                    }
                ],
                "value": None
                },
                {
                "name": "Enviado por",
                "selector": [
                    {
                    "id": "#tabular-buybox > div.tabular-buybox-container > div:nth-child(4) > div > span"
                    }
                ],
                "value": None
                },
                    {
                "name": "Peso",
                "selector": [
                    {
                        "id": "#poExpander > div.a-expander-content.a-expander-partial-collapse-content.a-expander-content-expanded > div > table > tbody > tr.a-spacing-small.po-item_weight > td.a-span9 > span"
                    }
                ],
                "value": None
                }
            ]
        }
        
        html = self.get_html()
        info = self.get_values_html(html, values)
        for k in values["products"]:
            print(k["name"].upper(), " : ", k["value"])
    



def asad():
    scrapp = Scrapper("https://www.amazon.com/-/es/gp/product/B0C1JKB652/ref=ewc_pr_img_2?smid=A2XZ7JICGUQ1CX&th=1")
    html = scrapp.scrape_product_info()
    # print(html)
    
asad()



