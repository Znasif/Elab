from selenium import webdriver
from bs4 import BeautifulSoup
import json

a = ['https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e8200', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e81a5', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7ba4', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e8174', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e80ea', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7c97', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7ae3', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7b0b', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e8152', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7a7e', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7c89', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7bce', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7c2c', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7b60', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e80fd', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e816c', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7bf0', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7b37', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7ac5', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7b9e', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e7ace', 'https://symptoms.webmd.com/coresc/landing?condition=091e9c5e808e80d1']

b = {}

for i in a[:3]:
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
    browser.get(i)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    q = str(soup.find_all(class_='condition-header')[0].get_text())
    p = str(soup.find_all(class_='also-known-as')[0].get_text())
    r = str(soup.find_all(class_='treatment-may-include')[0].get_text())
    b[q] = [p, r, i]
    browser.quit()

with open("web.json", 'w+') as f:
   json.dump(b, f)