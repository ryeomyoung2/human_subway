# human-cal-db-ryeom49


11/15
주피터노트북 postgresql 연동 후 테이블 생성 및 뉴스데이터 insert

from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from datetime import datetime
import json

url = 'C:/Users/h/Desktop/chatbot/'
driver = webdriver.Chrome(url + 'chromedriver.exe')





conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
                        dbname="da3iiu1dg1eubl", 
                        user="arbmerojlhxbrf", 
                        password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
                        port="5432")


cur = conn.cursor()




header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=2호선'

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, 'html.parser')

news_lis = soup.select('#main_pack > section > div > div.group_news > ul > li')


newsday = datetime.today().strftime('%Y%m%d%H%M%S')
filename = '네이버뉴스' + newsday + '.txt'

newslist = []
        
for li in news_lis:
    news_day = li.find('span', class_='info').text.strip()
    title = li.find('a', class_='news_tit')['title']
    a_href = li.find('a', class_='news_tit')['href']

    AAA=news_day,title,a_href
    newslist.append(AAA)

   