from flask_restful import Resource
from bs4 import BeautifulSoup
import requests


class scrap_board(Resource):
    def __init__(self, host, port, datapath):
        self.host = host
        self.port = port
        self.datapath = datapath

    def get(self, datatype, board):
        try:
            r = requests.get(f'https://karachan.org/{board}')
            count_soup = BeautifulSoup(r.content.decode(), features='html.parser')
            pages = count_soup.find("div", {"class": "pages"})
            for i in range(len(pages.findAll("a"))):
                requests.get(f"http://{self.host}:{self.port}/scrap/page/{datatype}/{board}/{i}")
            return "success"
        except Exception:
            return "error"
