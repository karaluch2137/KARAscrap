from flask_restful import Resource
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json
import os


class scrap_thread(Resource):
    def __init__(self, datapath):
        self.datapath = datapath

    def get(self, datatype, board, thread_id):

        if datatype != 'both' and datatype != "json" and datatype != "html":
            return "error: wrong data type (only 'json' or 'html' or 'both' allowed)"

        url = f"https://karachan.org/{board}/res/{thread_id}.html#q{thread_id}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content.decode(), features='html.parser')
                posts = soup.findAll("div", {"class": "post"})
                for i in tqdm(range(len(posts)),
                              desc=f"thread {thread_id}",
                              ncols=90,
                              colour='white',bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}'):
                    post = posts[i]
                    post_id = str(post.find("a", {"class": "quotePost"}).text)
                    #print(post_id)
                    post_info = {}
                    replies = []
                    for sub_post in posts:
                        if str(post_id) in str(sub_post.find('blockquote').text):
                            replies.append(post['id'][1:])
                    this_post = post
                    post_info["id"] = str(post_id)
                    post_info["type"] = str(this_post['class'][1])

                    if post_info["type"] == 'op' or this_post.find('b', {'class': 'opsign'}) is not None:
                        post_info["op"] = True
                    else:
                        post_info["op"] = False

                    if post_info["type"] == 'op':
                        post_info["subject"] = this_post.find('span', {'class': 'subject'}).text
                    else:
                        post_info["subject"] = None

                    post_info["name"] = str(this_post.find('span', {'class': 'name'}).text)

                    if this_post.find('a', {'class': 'useremail'}) is not None:
                        post_info["email"] = this_post.find('a', {'class': 'useremail'})['href']
                    else:
                        post_info["email"] = None

                    if this_post.find('span', {'class': 'posteruid'}) is not None:
                        post_info["posteruid"] = this_post.find('span', {'class': 'posteruid'}).text
                    else:
                        post_info["posteruid"] = None
                    post_info["date"] = str(this_post.find('span', {'class': 'dateTime'}).text)
                    if this_post.find('div', {'class': 'file'}) is not None:
                        post_info["file"] = {}
                        if this_post.find('div', {'class': 'file'}).find('b'):
                            if str(this_post.find('div', {'class': 'file'}).find('b').text) == "Embed":
                                post_info["file"]["filename"] = 'embed'
                                post_info["file"]["url"] = str(this_post.find('iframe')['src'])
                            elif str(this_post.find('div', {'class': 'file'}).find('b').text) == "Spoiler":
                                post_info["file"]["filename"] = 'spoiler'
                                post_info["file"]["url"] = "https://karachan.org/" + str(
                                    this_post.find('div', {'class': 'file'}).find('a')['href'][6:])
                            else:
                                return f"error: Unknown type at post {post_id}"
                        else:
                            post_info["file"]["filename"] = str(this_post.find('span', {'class': 'fileText'}).find('span')['title'])
                            if this_post.find('a', {'class': 'fileThumb'}):
                                post_info["file"]["url"] = "https://karachan.org/" + str(
                                    this_post.find('a', {'class': 'fileThumb'})['href'])[6:]
                            else:
                                post_info["file"]["url"] = "https://karachan.org/" + str(
                                    this_post.find('span', {'class': 'fileText'}).find('a')['href'])[6:]
                    else:
                        post_info["file"] = None
                    post_info["text"] = str(this_post.find('blockquote', {'id': f'm{post_id}'}).text)

                    if this_post.find('b', attrs={"style": "color:red;"}):
                        post_info["banned"] = True
                        post_info["baninfo"] = this_post.find('b', attrs={"style": "color:red;"}).text
                    else:
                        post_info["banned"] = False
                        post_info["baninfo"] = None

                    post_info["replies"] = replies
                    path = f"{self.datapath}/{board}/thread_{thread_id}"
                    if not os.path.isdir(path):
                        os.makedirs(path)

                    if post_info["file"] is not None:
                        if post_info["file"]["filename"] is not "embed":
                            cookies = {'password': 'karascraper', 'regulamin': 'accepted'}
                            url_req = requests.get(post_info["file"]["url"], allow_redirects=True, cookies=cookies)
                            #print(f"img status: {url_req.status_code}")
                            with open(f"{path}/{post_info['file']['filename']}", 'wb') as outfile:
                                outfile.write(url_req.content)
                                outfile.close()

                    if datatype == 'html' or datatype == 'both':
                        with open(f"{path}/{post_id}.html", 'w', encoding="utf8") as outfile:
                            outfile.write(str(this_post.prettify()))
                            outfile.close()
                    if datatype == 'json' or datatype == 'both':
                        with open(f"{path}/{post_id}.json", 'w', encoding="utf8") as outfile:
                            outfile.write(str(json.dumps(post_info, indent=4, ensure_ascii=False).encode('utf8').decode()))
                            outfile.close()
                if board == 'b':
                    threadStats = {"replies": len(posts),
                                   "uniqueIDs": len(set([str(post.find('span', {'class': 'posteruid'}).text) for post in posts])),
                                   "sfr": str(round(len(posts)/len(set([str(post.find('span', {'class': 'posteruid'}).text) for post in posts])), 2))}
                    with open(f"{path}/threadStats.json", 'w', encoding="utf8") as outfile:
                        outfile.write(str(json.dumps(threadStats, indent=4, ensure_ascii=False).encode('utf8').decode()))
                        outfile.close()
                return "success"
            else:
                return "error: bad code"
        except Exception as e:
            return f"error: {e}"
