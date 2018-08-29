from bs4 import BeautifulSoup
import urllib
import Queue
import nltk
#as3:/usr/local/lib/python2.7/site-packages# cat sitecustomize.py
# encoding=utf8  
import sys  
from operator import itemgetter
from itertools import groupby, imap
import math
from decimal import *

reload(sys)  
sys.setdefaultencoding('utf8')



f = urllib.urlopen("http://www.ign.com")
soup = BeautifulSoup(f.read(), 'html.parser')
with open("OriginalPage.html", "w") as file:
    file.write(str(soup))

q = Queue.Queue()

for tags in soup.find_all('h3'):
     for links in tags.find_all('a'):
         q.put(links.get('href'))
ctr = 0

while not q.empty():
     url = q.get()
     if("http" != url[:4]):
         url = "http://www.ign.com" + url
     x = urllib.urlopen(url)
     tempSoup = BeautifulSoup(x.read(), 'html.parser')
     L = []
     for links in tempSoup.find_all('a'):
         L.append(links.get('href'))
    #  with open("Links"+str(ctr)+".txt", 'w') as file:
    #      file.write(''.join(L).encode("utf-8"))
     with open("Document"+str(ctr)+".txt", 'w') as file:
         for script in tempSoup(["script", "style"]):
             script.decompose()    # rip it out
         body = tempSoup.find('body')
         page = body.text.encode("utf-8")
         lines = (line.strip() for line in page.splitlines())
         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
         page = '\n'.join(chunk for chunk in chunks if chunk)
         file.write("\n"+page)
        
     print(str(ctr)+"\n")
     ctr = ctr + 1
     if(ctr == 20):
         break

list_i = []


for i in range (0,20):
    tempList = []
    with open("Document"+str(i)+".txt", 'r') as file:
        text = file.read().replace('\n', '')
        tokens = nltk.word_tokenize(text)
        for token in tokens:
            tempList.append(token)
        
        list_i.append(list(set(tempList)))



unique_tokens = []
d = {}
total_count = len(list_i)
for i in range(0,total_count):
    for tokens in list_i[i]:
        unique_tokens.append(tokens)
unique_tokens = list(set(unique_tokens))
for t in unique_tokens:
    count = 0
    for i in range(0,total_count):
        if(t in list_i[i]):        
            count = count + 1
    idf = -(math.log(Decimal(count)/Decimal(total_count)))
    d[t] = idf
    



with open("tokenList.txt", 'w') as file:
    for item in unique_tokens:
        file.write(item+"\t"+str(d[item])+"\n")

