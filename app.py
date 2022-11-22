# -*- coding: utf-8 -*-

from flask import Flask, request
from datetime import date
import psycopg2
import requests
import json
import re

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

   # 데이터 조작 인스턴스 생성
    cur = conn.cursor()

    # 오늘 날짜 (YYYY-MM-DD 구하기)
    today = date.today().isoformat() + '%'

    # DB SELECT
    cur.execute(f"SELECT * FROM subaccdata WHERE acctime LIKE '{today}' order by acctime ASC")
    result_all = cur.fetchall()

    sbstr=""
    for i in result_all:
        for j in i:
            sbstr = sbstr + j + "\n"
        sbstr = sbstr + "\n"
    sbstr = sbstr[:-2]

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


# 경로 url 변환 함수
def location(searching):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
    headers = {
        "Authorization": "KakaoAK bbc0593ca1fbd88db71ccfdd5421ef1e"
    }
    destination = 'https://map.kakao.com/link/to/' + (requests.get(url, headers = headers).json()['documents'])[0].get('id')
    
    return destination

# 목적지 검색
@app.route('/api/goto', methods=['POST'])
def goto():
    body = request.get_json()
    print(body)
    params_df = (body['action']['params'])['sys_location']
    print(type(params_df))

    answer_text = str(location(params_df))

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

# 뉴스 검색
@app.route('/api/newslist', methods=['POST'])
def newslist():
    body = request.get_json()
    print(body)
    hosun = (body['action']['params'])['sys_news']

    conn = psycopg2.connect(host="ec2-23-21-207-93.compute-1.amazonaws.com", 
                            dbname="d3oubpekvnbupv", 
                            user="grxhirqndvyqvv", 
                            password="6f1afaafe16d245c70666bdb8c831aa876e62b380a1544f5dc832c51f27cece6", 
                            port="5432")

    cur = conn.cursor()

    newhosun = '%' + hosun + '%'
    cur.execute(f"SELECT * from newsdata WHERE newsname LIKE '{newhosun}' order by newsdate desc limit 5")
    result_all = cur.fetchall()

    newsstr = ""

    for i in result_all:
        for j in i:
            newsstr = newsstr + j + '\n'
        newsstr = newsstr + '\n'
    newsstr = newsstr[:-2]

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

# 간편 지연 증명서
@app.route('/api/simpleDelay', methods=['POST'])
def simpleDelay():

    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "http://www.seoulmetro.co.kr/kr/delayProofList.do?menuIdx=543"
                    }
                }
            ]
        }
    }

    return responseBody


@app.route('/api/simpleDelay2', methods=['POST'])
def simpleDelay2():
    body = request.get_json()
    print(body)
    hosun = (body['action']['params'])['sys_hosun']
    hosun2 = hosun
    hosun3 = re.sub(r'[^0-9]', '', hosun2)
    direction = (body['action']['params'])['sys_direction']
    delayTime = (body['action']['params'])['sys_delayTime']
    delayTime2 = delayTime
    delayTime3 = re.sub(r'[^0-9]', '', delayTime2)
    trainTime = (body['action']['params'])['sys_trainTime']
    today = date.today().isoformat()

    if direction == "소요산방면":
        A = direction
        A = "0"
        direction2=A 
    elif direction == "신창방면":
        A = direction
        A = "1"
        direction2=A
    elif direction == "인천방면":
        A = direction
        A = "2"
        direction2=A
    elif direction == "대화방면":
        A = direction
        A = "3"
        direction2=A
    elif direction == "오금방면":
        A = direction
        A = "4"
        direction2=A 
    elif direction == "당고개방면":
        A = direction
        A = "5"
        direction2=A
    elif direction == "오이도방면":
        A = direction
        A = "6"
        direction2=A
    elif direction == "문산방면":
        A = direction
        A = "7"
        direction2=A
    elif direction == "용문방면":
        A = direction
        A = "8"
        direction2=A
    elif direction == "서울방면":
        A = direction
        A = "9"
        direction2=A 
    elif direction == "왕십리방면":
        A = direction
        A = "10"
        direction2=A 
    elif direction == "인천방면":
        A = direction
        A = "11"
        direction2=A 
    elif direction == "상봉/청량리 방면":
        A = direction
        A = "12"
        direction2=A 
    elif direction == "춘천방면":
        A = direction
        A = "13"
        direction2=A 
    elif direction == "판교방면":
        A = direction
        A = "14"
        direction2=A 
    elif direction == "여주방면":
        A = direction
        A = "15"
        direction2=A 
    elif direction == "부천방면":
        A = direction
        A = "16"
        direction2=A 
    elif direction == "일광방면":
        A = direction
        A = "17"
        direction2=A 

    if trainTime == "2":
        A = trainTime
        A = "1_2"
        trainTime2=A
    elif trainTime == "3":
        A = trainTime
        A = "2"
        trainTime2=A
    elif trainTime == "4":
        A = trainTime
        A = "2_3"
        trainTime2=A
    elif trainTime == "5":
        A = trainTime
        A = "3"
        trainTime2=A
   
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "https://info.korail.com/mbs/www/neo/delay/delaylistDetail.jsp?line=" + hosun3 + "&inoutTag="+ direction2 +"&time="+ delayTime3 +"&indate="+ today +"&order="+ trainTime2
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
                        "안녕하세요, 지하철 이슈 알림이입니다."
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


