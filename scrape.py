import requests
from bs4 import BeautifulSoup
import csv
import logging
from csv import writer
import datetime


URL = "https://kun.uz/news/category/jahon"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

quotes = []  # a list to store quotes

table = soup.find('div', attrs={'id': 'news-list'})

for row in table.findAll('div',
                         attrs={'class': 'col-md-4 mb-25 l-item'}):
    URL1 = "https://kun.uz" + row.div.a['href']
    quote1 = {}
    r1 = requests.get(URL1)
    soup1 = BeautifulSoup(r1.content, 'html5lib')
    table1 = soup1.find('div', attrs={'class': 'single-layout__center'})
    for row1 in table1.findAll('div', attrs={'class': 'single-content'}):
        quote1["source_url"] = URL1
        quote1["access_datetime"]=datetime.datetime.now()
        quote1["content"] = row1.p.text
        quote1["words"]=quote1["content"].split()
        quote1["words"]=[word.strip('.,!;()[]') for word in quote1["words"]]
        unique_words = []
        for word in quote1["words"]:
            if word not in unique_words:
                unique_words.append(word)
        unique_words.sort()
        quote1["unique_words"]=unique_words
        dic=dict()
        for word in quote1["words"]:
            if word in dic:
                dic[word]=dic[word]+1
            else:
                dic[word]=1
            #print('Frequency of ', word , 'is :', quote1["words"].count(word))
            quote1["word_frequency"]=dic
    quotes.append(quote1)

#print(type(unique_words))

#print(quotes)

with open('tahrirchi.csv', 'w', encoding='utf8', newline='') as f:
    w = csv.DictWriter(f, ['source_url', 'access_datetime', 'content', 'words', 'unique_words', 'word_frequency'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)