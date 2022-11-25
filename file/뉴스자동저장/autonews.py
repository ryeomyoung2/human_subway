import psycopg2
import sys
import requests
import datetime
import time
import re
import schedule

# 네이버 API 뉴스
def naverapi(keyword):
    print("-"*30)
    print("네이버 api 호출")

    # 네이버 검색api 키값
    client_id = 'CmmN2OJp47c60h9IWTRs'
    client_secret = 'mALduPDQEB'

    #검색설정
    search_word = keyword
    encode_type = 'json'
    max_display = 50
    sort = 'date'
    start = 1

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

    #헤더에 아이디와 키 정보 넣기
    headers = {'X-Naver-Client-Id' : client_id,
            'X-Naver-Client-Secret':client_secret
            }

    #HTTP요청 보내기
    response = requests.get(url, headers=headers)
    
    if response.status_code==200:
        print("네이버 api 호출 성공")
        print("-"*30)

        # json형식으로 받기
        result = response.json()

        # key : items
        result_items=result['items']
        return result_items
    else:
        print("네이버 api 호출 실패")
        return ""
        

# html 파싱
def clean_html(x):
    x = re.sub("\&\w*\;","",x)
    x = re.sub("<.*?>","",x)
    return x

# db연결
def dbconn():
    conn = psycopg2.connect(host="ec2-23-21-207-93.compute-1.amazonaws.com", 
                            dbname="d3oubpekvnbupv", 
                            user="grxhirqndvyqvv", 
                            password="6f1afaafe16d245c70666bdb8c831aa876e62b380a1544f5dc832c51f27cece6", 
                            port="5432")
    return conn


# db에 저장하기
def dbinsert():
    # 함수 실행 시간 출력
    now = time
    print("-"*60)
    print("time log :", now.strftime('%Y-%m-%d %H:%M:%S'))

    conn = dbconn()
    cur = conn.cursor()
    
    hosun = ['1호선','2호선','3호선','4호선','5호선','6호선','7호선','8호선','9호선']
    
    for keyword in hosun:
        result_items = naverapi(keyword)

        if result_items!="":
            for item in result_items:
                # 날짜 형식 변환
                pDate = datetime.datetime.strptime(item['pubDate'][5:-6], '%d %b %Y %H:%M:%S')
                pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
            
                # 뉴스제목 디코딩
                title = clean_html(item['title'])
            
                link = item['link']
            
                insertdata = (pDate, title, link)

                # ON CONFLICT : 데이터가 중복되면 INSERT하지않음
                cur.execute("INSERT into newsdata(newsdate, newsname, newslink) VALUES (%s, %s, %s) ON CONFLICT (newsname, newslink) DO NOTHING", insertdata)

                # db commit
            conn.commit()
        else:
            print("api값 확인 필요")
            print("-"*30)



def exit():
    sys.exit()

schedule.every(30).minutes.do(dbinsert)
schedule.every().day.at("23:55").do(exit)

while True:
    schedule.run_pending()
    time.sleep(1)

# dbinsert()