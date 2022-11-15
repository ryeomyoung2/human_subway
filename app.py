# -*- coding: utf-8 -*-
from flask import Flask, request
import pandas as pd 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text 
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# 크롤링할 창 열기
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.get("https://safecity.seoul.go.kr/acdnt/sbwyIndex.do")

# 크롤링 변수설정
parentElement = driver.find_elements(By.XPATH, '//*[@id="dv_as_timeline"]/li')

# 사고 정보 리스트
subli=[]

# 사고 정보 리스트에 크롤링해서 정보 넣기 (ul 태그 아래 있는 li 반복 뽑기)
for i in parentElement:
    i.click()
    time.sleep(0.05)
    a = i.text
    subli.append(a)
    i.click()

# 카톡으로 보내줄 문자열
sbstr=""

for item in subli:
    sbstr = sbstr + item + "\n"



## DB 연결 Local
def db_create():
    # 로컬
	# engine = create_engine("postgresql://postgres:1234@localhost:5432/chatbot", echo = False)
		
	# Heroku
    engine = create_engine("postgresql://arbmerojlhxbrf:6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8@ec2-18-207-37-30.compute-1.amazonaws.com:5432/da3iiu1dg1eubl", echo = False)

    engine.connect()
    engine.execute("""
        CREATE TABLE IF NOT EXISTS iris(
            sepal_length FLOAT NOT NULL,
            sepal_width FLOAT NOT NULL,
            pepal_length FLOAT NOT NULL,
            pepal_width FLOAT NOT NULL,
            species VARCHAR(100) NOT NULL
        );"""
    )
    data = pd.read_csv('data/iris.csv')
    print(data)
    data.to_sql(name='iris', con=engine, schema = 'public', if_exists='replace', index=False)

## 메인 로직!! 
def cals(opt_operator, number01, number02):
    if opt_operator == "addition":
        return number01 + number02
    elif opt_operator == "subtraction": 
        return number01 - number02
    elif opt_operator == "multiplication":
        return number01 * number02
    elif opt_operator == "division":
        return number01 / number02

app = Flask(__name__)

@app.route("/")
def index():
    db_create()
    return "DB Created Done !!!!!!!!!!!!!!!"

## 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


## 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

## 카카오톡 Calculator 계산기 응답
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json()
    print(body)
    params_df = body['action']['params']
    print(type(params_df))

    print('-----')
    opt_operator = params_df['operators']
    print('operator:', opt_operator)
    print('-----')
    number01 = json.loads(params_df['sys_number01'])['amount']
    number02 = json.loads(params_df['sys_number02'])['amount']

    print(opt_operator, type(opt_operator), number01, type(number01))

    answer_text = str(cals(opt_operator, number01, number02))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    return responseBody

## Query 조회
@app.route('/api/querySQL', methods=['POST'])
def querySQL():
    
    body = request.get_json()
    params_df = body['action']['params']
    sepal_length_num = str(json.loads(params_df['sepal_length_num'])['amount'])

    print(sepal_length_num, type(sepal_length_num))
    query_str = f'''
        SELECT sepal_length, species FROM iris where sepal_length >= {sepal_length_num}
    '''

    engine = create_engine("postgresql://arbmerojlhxbrf:6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8@ec2-18-207-37-30.compute-1.amazonaws.com:5432/da3iiu1dg1eubl", echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))

    df = pd.DataFrame(query.fetchall())
    nrow_num = str(len(df.index))
    answer_text = nrow_num

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text + "개 입니다."
                    }
                }
            ]
        }
    }
    return responseBody


if __name__ == "__main__":
    db_create()
    app.run()

## 크롤링
@app.route('/api/saysubway', methods=['POST'])
def saysubway():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": sbstr
                    }
                }
            ]
        }
    }
    return responseBody


## DB 연결 Local
def db_create2():
    # 로컬
    # 	
	# Heroku
    engine = create_engine("postgresql://arbmerojlhxbrf:6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8@ec2-18-207-37-30.compute-1.amazonaws.com:5432/da3iiu1dg1eubl", echo = False)

    engine.connect()
    engine.execute("""
        CREATE TABLE IF NOT EXISTS subdata2(
            subacc VARCHAR(20) NOT NULL,
            acctime VARCHAR(30) NOT NULL,
            content VARCHAR(300) NOT NULL
        );"""
    )
    data = pd.read_csv('data/subdata2.csv')
    print(data)
    data.to_sql(name='subdata2', con=engine, schema = 'public', if_exists='replace', index=False)

## DB 출력
@app.route('/api/saysubway2', methods=['POST'])
def saysubway2():
    
    body = request.get_json()
    params_df = body['action']['params']
    content = str(json.loads(params_df['content']))

    print(content, type(content))
    query_str = f'''
        SELECT * FROM subdata2 WHERE acctime = '2022-11-15 06:01' 
    '''
  
    engine = create_engine("postgresql://arbmerojlhxbrf:6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8@ec2-18-207-37-30.compute-1.amazonaws.com:5432/da3iiu1dg1eubl", echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": query_str
                    }
                }
            ]
        }
    }
    return responseBody

if __name__ == "__main__":
    db_create2()
    app.run()


 