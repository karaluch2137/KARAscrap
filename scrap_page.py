from flask_restful import Resource
from bs4 import BeautifulSoup
import requests


class scrap_page(Resource):
    def __init__(self, host, port, datapath):
        self.host = host
        self.port = port
        self.datapath = datapath

    def get(self, datatype, board, page_number):
        try:
            r = requests.get(f'https://karachan.org/{board}')
            count_soup = BeautifulSoup(r.content.decode(), features='html.parser')
            pages = count_soup.find("div", {"class": "pages"})
            if 0 < int(page_number) < len(pages.findAll("a")):
                r = requests.get(f'https://karachan.org/{board}/{page_number}.html')
            elif int(page_number) != 0:
                return "error: board page number extends"

            soup = BeautifulSoup(r.content.decode(), features='html.parser')
            threads = soup.findAll("div", {"class": "thread"})
            print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(f'@@@@@@@@@@@@@@@@@@   board {board} {page_number}   @@@@@@@@@@@@@@@@@@@@')
            print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            for thread in threads:
                requests.get(f"http://{self.host}:{self.port}/scrap/thread/{datatype}/{board}/{thread['id'][1:]}")
            print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            return "success"
        except Exception:
            return "error"

