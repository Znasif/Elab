from selenium import webdriver
from bs4 import BeautifulSoup
import json
import threading
import queue

'''
with open("extras/level4.json", "r") as f:
    a = f.read()
    links = json.loads(a)
    a = list(links.keys())
'''

b = {}
#******************************
THREAD_COUNT = 1
#******************************
def get_(i):
    browser = webdriver.Chrome(executable_path=r'extras/chromedriver')
    browser.get(i)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    q = str(soup.find_all(class_='condition-header')[0].get_text())
    p = str(soup.find_all(class_='also-known-as')[0].get_text())
    r = str(soup.find_all(class_='treatment-may-include')[0].get_text())
    b[q] = [p, r, i]
    browser.quit()
cnt = 0
threads = []
for i in a:
    t = threading.Thread(target=get_, args=(i,))
    threads.append(t)
    if(len(threads)==THREAD_COUNT):
        for j in threads:
            j.start()
        for j in threads:
            j.join()
        threads = []
        cnt+=THREAD_COUNT
        with open("web.json", 'w+') as f:
           json.dump(b, f)
        print(cnt)
