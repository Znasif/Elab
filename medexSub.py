import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
dictionary = {}
dictionaryKey = []
dictionaryValue = []
i = 0
page = requests.get("https://medex.com.bd/brands/25489/a-ben-ds")
soup = BeautifulSoup(page.content, 'html.parser')
for x in range(len(soup.find_all(class_="ac-header"))):
    row = (soup.find_all(class_="ac-header")[x].get_text())
    dictionaryKey.append(row)
for x in range(len(soup.find_all(class_="col-xs-12 ac-body"))):
    row = (soup.find_all(class_="col-xs-12 ac-body")[x].get_text())
    dictionaryValue.append(row)
dictionary[1] = {}
for x in range(len(dictionaryKey)):
    # dictionary[1][dictionaryKey[x]] = {}
    dictionary[1][dictionaryKey[x]] = dictionaryValue[x]
print(dictionary)
# import json
# from bs4 import BeautifulSoup
# from tqdm import tqdm
# import requests
# page = requests.get(
#     "https://medex.com.bd/brands?alpha=z&page=16")
# print(page)
# soup = BeautifulSoup(page.content, 'html.parser')
# for x in range(len(soup.select('a.hoverable-block'))):
#     row = (soup.select('a.hoverable-block')[x])
#     print(row.get('href'))
with open('desc.json', 'w+') as fp:
    json.dump(dictionary, fp)
