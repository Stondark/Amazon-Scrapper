# Classes

from proxy import Proxy
from agents import Agents

# Librarys
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup

class Scrapper:

    def __init__(self, url):
        self.url = url
        self.proxy = Proxy().proxy_ip;
        self.agent = Agents().user_agent
        self.money = "COP"
        self.cookies = {
            "i18n-prefs" : self.money
        }
        self.language = "es-ES,es;q=0.9"
        self.headers = {
            'User-Agent': self.agent,
            'Accept-Language': self.language
        }

    def get_html(self):
        response = requests.get(self.url, proxies = self.proxy, cookies = self.cookies)
        return BeautifulSoup(response.content, 'html.parser')           

scrapp = Scrapper("https://www.amazon.com/-/es/gp/product/B0BZB6WJZJ/ref=ox_sc_act_title_1?smid=A2XZ7JICGUQ1CX&psc=1")
print(scrapp.get_html())


