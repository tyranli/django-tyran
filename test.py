import requests
from bs4 import BeautifulSoup

descripreq = requests.get('https://cn.bing.com/cnhp/life')
descripsoup = BeautifulSoup(descripreq.text,'html.parser')
descrip = descripsoup.select('#hplaSnippet')[0].string
print(descrip)