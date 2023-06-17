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

def asad():
    scrapp = Scrapper("https://www.amazon.com/-/es/gp/product/B0BZB6WJZJ/ref=ox_sc_act_title_1?smid=A2XZ7JICGUQ1CX&psc=1")
    html = scrapp.get_html()
    
asad()



