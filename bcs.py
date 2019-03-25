import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json

a = [0 for j in range(7000)]
d = {}
b = []
c = [[["বাংলা", 1], ["বাংলা সাহিত্য", 21], ["বাংলা সাহিত্যে প্রথম", 22], ["সমার্থক শব্দ", 41], ["ব্যাকরণ", 42], ["উপসর্গ", 59]], [["সাধারণ বিজ্ঞান", 2], ["মানবদেহ", 23], ["রাসায়নিক সংকেতসমূহ", 24], ["পদার্থ বিজ্ঞান", 33], ["উদ্ভিদ বিজ্ঞান", 34], ["চিকিৎসা ও পুষ্টি বিজ্ঞান", 35], ["দৈনন্দিন বিজ্ঞান", 36], ["পরমানুর ইলেকট্রন বিন্যাস", 37], ["রসায়ন", 38]], [["বাংলাদেশ বিষয়াবলী", 3], ["প্রশাসনিক/সাংবিধানিক প্রধান", 10], ["বাংলাদেশে প্রথম", 11], ["বাঙালী জাতির অভ্যুদয়", 12], ["প্রাক সুলতানী আমল", 13], ["সুলতানী আমল", 14], ["মুঘল আমল", 15], ["উপনিবেশিক শাসন", 16], ["স্বাধীকার আন্দোলন", 17], ["পাকিস্ত্মান আমল- ১৯৪৭", 18], ["৫২-এর ভাষা অন্দোলন", 19], ["৬ দফা ও গণ অভ্যুত্থান", 20], ["বাংলাদেশ বিষয়", 43], ["মুক্তিযুদ্ধ", 49], ["খেলাধুলা বাংলাদেশ", 59], ["বাংলাদেশের সংবিধান", 60], ["বাংলাদেশ অর্থনীতি", 62], ["বঙ্গবন্ধু", 63]], [["আন্তর্জাতিক বিষয়াবলী", 4], ["স্মারনীয় ঘটনাবলী", 25], ["এশিয়ার ইতিহাস", 26], ["এশিয়া মহাদেশ", 30], ["আন্তর্জাতিক", 44], ["আবিঙ্কার", 45], ["আন্তর্জাতিক সংগঠন", 46], ["আন্তর্জাতিক দিবস", 47], ["আন্তর্জাতিক রাজধানী", 48], ["আন্তর্জাতিক রাষ্ট্রপ্রধান", 50], ["খেলাধুলা আন্তর্জাতিক", 61], ["আন্তর্জাতিক মুদ্রা", 69]], [["গাণিতিক বিষয়াবলী", 8], ["পাটিগণিতের সূত্র", 27], ["দৈর্ঘ্য ও জায়গা-জমি পরিমাপ", 28], ["সাধারণ গণিত ও গাণিতিক যুক্তি", 32], ["বীজগণিত", 51], ["জ্যামিতি", 56]], [["ভৌগলিক পরিচিতি ", 29]], [["English",31], ["Grammar", 39], ["Literature", 40], ["Synonym", 52], ["Antonym", 53], ["Analogy", 54], ["Spelling", 55], ["Fill in the gaps", 57], ["Corrections", 58], ["Voice Change", 67], ["Phrases and Idioms", 68]], [["কম্পিউটার ও তথ্য প্রযুক্তি", 64]],[["মানসিক দক্ষতা", 65]], [["নৈতিকতা, মূল্যবোধ ও সুশাসন", 66]]]

for i in range(len(c)):
  d[c[i][0][1]] = c[i][0][0]
  if(len(c[i])-1==0):
    b.append(c[i][0][1])
  for j in range(len(c[i])-1):
    b.append(c[i][j+1][1])
    d[c[i][j+1][1]] = c[i][j+1][0]

#for j in b:
for j in range(21, 22):
  link = {}
  for y in range(7000):
  #for y in range(63, 64):
     #if(a[y]==1):
     #  print("*", end="")
     #  continue
     try:
        url = "https://www.bcsprep.com/questiondetails.php?catid="+str(j)+"&qid="+str(y)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sd = str(soup.find_all(class_='lead')[0].get_text())
        link[y] = {}
        link[y]["question"] = sd
        if(len(link[y]["question"])>4):
          a[y]=1
        link[y]["options"] = []
        e = soup.find_all(class_='radio')
        n = len(e)
        for x in range(n):
            # print(soup.find_all(class_='radio')[x].get_text())
            link[y]["options"].append(str(e[x].get_text()))
        link[y]["answer"] = []
        st = soup.find_all('input', id="answeritem")
        st = str(st)
        var = st.split("value=")[-1][1:-3]
        link[y]["answer"].append(var)
        print(link[y])
     except:
        print("*", end="")
        continue
  with open(d[j]+'.json', 'w+') as fp:
    print(d[j])
    json.dump(link, fp)