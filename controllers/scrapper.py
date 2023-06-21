# Classes

from proxy import Proxy
from agents import Agents

# Librarys
import requests
import re
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
        for i in values["products"]:
            attempts = 0
            # print(i["value"])
            while i["value"] is None and attempts < 5:
                for j in i["selector"]:

                    if(i["name"] == "Peso"):
                        keyword_regex = re.compile(r'\b(libras|kilogramos|gramos)\b', re.IGNORECASE)
                        v_html = html.find(string = keyword_regex)
                    else: 
                        v_html = html.select_one(j["id"])

                    if(v_html != None):                
                        if(v_html.name == 'img'):
                            i["value"] = str(v_html['src'])
                        else:
                            i["value"] = v_html.get_text().strip()
                    else:
                        attempts += 1
                        print(attempts, i["name"])

        return values

    def scrape_product_info(self):
        values = {
            "products": [
                {
                "name": "Producto",
                "selector": [
                    {
                    "id": "#productTitle"
                    }
                ],
                "value": None
                },
                {
                "name": "Precio",
                "selector": [
                    {
                    "id": ".a-offscreen"
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
                    },
                    {
                        "id": "#landingImage"
                    }
                ],
                "value": None
                },
                {
                "name": "Vendedor",
                "selector": [
                    {
                        "id": "#sellerProfileTriggerId"
                    },
                    {
                        "id": "#tabular-buybox > div.tabular-buybox-container > div:nth-child(6) > div > span"
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
                    },
                    {
                        "id": "#productDetails_detailBullets_sections1 > tbody > tr:nth-child(11) > td"
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
    scrapp = Scrapper("https://www.amazon.com/-/es/PlayStation-PS5-Console-Ragnar%C3%B6k-Bundle-5/dp/B0BHC395WW/ref=sr_1_2?crid=3MBCFBJRA4EC1&keywords=playstation+5&qid=1680851108&sprefix=play%2Caps%2C169&sr=8-2")
    html = scrapp.scrape_product_info()
    # print(html)
    
asad()



