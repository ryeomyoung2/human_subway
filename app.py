# -*- coding: utf-8 -*-

from flask import Flask, request
from datetime import date
import psycopg2
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "hello"

## 오늘의 사고내역 보내주기
@app.route('/api/saysubway', methods=['POST'])
def saysubway():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    # db연결
    conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
                            dbname="da3iiu1dg1eubl", 
                            user="arbmerojlhxbrf", 
                            password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
                            port="5432")

    # 데이터 조작 인스턴스 생성
    cur = conn.cursor()

    # 오늘 날짜 (YYYY-MM-DD 구하기)
    today = date.today().isoformat() + '%'

    # DB SELECT
    cur.execute(f"SELECT * FROM subdata2 WHERE acctime LIKE '{today}' ")
    result_all = cur.fetchall()

    sbstr=""
    for i in result_all:
        for j in i:
            sbstr = sbstr + j + "\n"

    if(sbstr==""):
        sbstr = "오늘은 지하철 속보가 없습니다"

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

##호선뉴스
@app.route('/api/newslist', methods=['POST'])
def newslist():
    body = request.get_json()
    print(body)
    hosun = (body['action']['params'])['sys_news']

    
    conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
                            dbname="da3iiu1dg1eubl", 
                            user="arbmerojlhxbrf", 
                            password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
                            port="5432")
 
    cur = conn.cursor()

    newhosun = '%' + hosun + '%'
    cur.execute(f"SELECT title, link from newslist WHERE title LIKE '{newhosun}' order by title asc limit 3")
    result_all = cur.fetchall()

    newsstr=""
    for i in result_all:
        for j in i:
            newsstr = newsstr + j + "\n"

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": newsstr
                    }
                }
            ]
        }
    }
    return responseBody

##2호선뉴스
# @app.route('/api/newslist2', methods=['POST'])
# def newslist2():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%2호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# ##3호선뉴스
# @app.route('/api/newslist3', methods=['POST'])
# def newslist3():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%3호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

#     ##4호선뉴스
# @app.route('/api/newslist4', methods=['POST'])
# def newslist4():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%4호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# ##5호선뉴스
# @app.route('/api/newslist5', methods=['POST'])
# def newslist5():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%5호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# ##6호선뉴스
# @app.route('/api/newslist6', methods=['POST'])
# def newslist6():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%6호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# ##7호선뉴스
# @app.route('/api/newslist7', methods=['POST'])
# def newslist7():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%7호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# ##8호선뉴스
# @app.route('/api/newslist8', methods=['POST'])
# def newslist8():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%8호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# ##9호선뉴스
# @app.route('/api/newslist9', methods=['POST'])
# def newslist9():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

    
#     conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
#                             dbname="da3iiu1dg1eubl", 
#                             user="arbmerojlhxbrf", 
#                             password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
#                             port="5432")
 
#     cur = conn.cursor()

#     cur.execute(f"SELECT * from newslist WHERE title LIKE '%9호선%' order by title asc limit 3")
#     result_all = cur.fetchall()

#     sbstr=""
#     for i in result_all:
#         for j in i:
#             sbstr = sbstr + j + "\n"

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": sbstr
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody


@app.route('/api/simpleDelay', methods=['POST'])
def simpleDelay():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    
    # conn = psycopg2.connect(host="ec2-18-207-37-30.compute-1.amazonaws.com", 
    #                         dbname="da3iiu1dg1eubl", 
    #                         user="arbmerojlhxbrf", 
    #                         password="6944d2306202fed548eb3547ca2aaf2cfc420aa21880236efff1ba4f395f35f8", 
    #                         port="5432")
 
    # cur = conn.cursor()

    # cur.execute(f"SELECT * from newslist WHERE title LIKE '%9호선%' order by title asc limit 3")
    # result_all = cur.fetchall()

    # sbstr=""
    # for i in result_all:
    #     for j in i:
    #         sbstr = sbstr + j + "\n"

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "https://info.korail.com/mbs/www/neo/delay/delaylist.jsp"
                    }
                }
            ]
        }
    }
    return responseBody



# 1단계 : 코드 수정
# 2단계 : 스킬 등록 (URL)
# 3단계 : 시나리오에서 등록한 스킬 호출
# 4단계 : 배포

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

## 카카오톡 Calculator 계산기 응답
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json()
    print(body)
    params_df = body['action']['params']
    print(type(params_df))
    opt_operator = params_df['operators']
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



# if __name__ == "__main__":
#     db_create()
#     app.run()


