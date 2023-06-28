# Classes

from controllers.proxy import Proxy
from controllers.agents import Agents

# Librarys
import requests
import re
from bs4 import BeautifulSoup

class Scrapper:

    def __init__(self, url):

        # set attributes

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

        # invoke methods
        self.check_url()

    
    def set_attributtes(self, money, language):
        self.money = money
        self.cookies["i18n-prefs"]  =  money
        self.language = language
        self.headers['Accept-Language'] = language

    def check_url(self):
        regex = r"https:\/\/www\.amazon\.[a-zA-Z]{2,3}"
        if not re.match(regex, self.url):
            raise Exception("URL is not valid")

    def get_html(self):
        try:
            response = requests.get(self.url, headers = self.headers, proxies = self.proxy, cookies = self.cookies)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            return BeautifulSoup(response.content, 'html.parser')  
        except requests.exceptions.RequestException as e:
            raise Exception("Error de solicitud:", e)
        except requests.exceptions.HTTPError as e:
            raise Exception("Error HTTP:", e)
        except Exception as e:
            raise Exception("Error:", e)
         

    def get_values_html(self, html, values):
        for i in values["products"]:
            attempts = 0
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

                        if(i["name"] == "Peso"):
                            i["value"] = self.sanitize_weight(i["value"])


                    else:
                        attempts += 1
                        if(attempts >= 2):
                            html = self.get_html()
        return values

    def sanitize_weight(self, value):
        regex = re.compile(r"\b(\d+(?:,\d+)?(?:\.\d+)?)\s*(libras|kilogramos|gramos)\b", re.IGNORECASE);
        list_weight = re.findall(regex, value)
        return self.convert_weight(list_weight[0])


    def convert_weight(self, value):
        value_weight = float(value[0].replace(',', '.'))
        weight = value[-1]
        if(weight.lower() == "libras"):
            result = value_weight / 2.2046
        elif(weight.lower() == "gramos"):
            result = value_weight / 1.000
        else:
            result = value_weight
        
        return f"{round(result, 2)} Kilogramos"


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
                        },
                        {
                            "id": "#poExpander > div.a-expander-content.a-expander-partial-collapse-content.a-expander-content-expanded > div > table > tbody > tr.a-spacing-small.po-item_weight > td.a-span3 > span"
                        }
                    ],
                    "value": None
                }
            ]
        }
        
        html = self.get_html()
        return self.get_values_html(html, values)
        
