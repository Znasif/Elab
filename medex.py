import json
from bs4 import BeautifulSoup
import threading
import requests
from tqdm import tqdm

def get_(ur):
    page = requests.get(ur)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find_all(class_="ac-header")
    f = soup.find_all(class_="col-xs-12 ac-body")
    n = len(e)
    ll = {}
    for x in range(n):
        ll[str(e[x].get_text())] = str(f[x].get_text())
    all_links[ur] = ll


##
THREAD_COUNT = 9
##

with open("medicine.json", "r") as f:
    a = f.read()
    links = json.loads(a)
    all_links = {}
    cnt = 0
    threads = []
    for _, i in enumerate(links):
        for j in tqdm(links[i]):
            t = threading.Thread(target=get_, args=(links[i][j],))
            threads.append(t)
            if len(threads) == THREAD_COUNT:
                for k in threads:
                    k.start()
                for k in threads:
                    k.join()
                threads = []
        with open('med_list.json', 'w+') as fp:
            json.dump(all_links, fp)