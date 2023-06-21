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
            while i["value"] is None and attempts <= 3:
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
                        if(attempts >= 2):
                            html = self.get_html()
                            
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
    scrapp = Scrapper("https://www.amazon.com/-/es/Tommy-Hilfiger-Ultra-Loft-Chaqueta/dp/B07G3BLWYW/?_encoding=UTF8&pd_rd_w=Jjhes&content-id=amzn1.sym.094b8411-30b9-4af6-bed5-15f63238bac9&pf_rd_p=094b8411-30b9-4af6-bed5-15f63238bac9&pf_rd_r=SEGTXH0R44JZPJ71W3Q8&pd_rd_wg=IMwfC&pd_rd_r=3ff526e2-ef8d-40ba-b241-1bd29e5a4d04&ref_=pd_gw_exports_top_sellers_by_gl_rec&th=1&psc=1")
    html = scrapp.scrape_product_info()
    # print(html)
    
asad()



