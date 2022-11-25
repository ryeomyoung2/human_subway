"""
자동실행하기 전에 README파일 체크 필수

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import date
import time
import psycopg2
import json
import requests
import schedule


# db연결
def dbconn():
    conn = psycopg2.connect(host="ec2-23-21-207-93.compute-1.amazonaws.com", 
                            dbname="d3oubpekvnbupv", 
                            user="grxhirqndvyqvv", 
                            password="6f1afaafe16d245c70666bdb8c831aa876e62b380a1544f5dc832c51f27cece6", 
                            port="5432")
    return conn

# DB - 오늘날짜의 지하철 이슈 찾아보기
def todaysubaccDB():
    print("-"*30)
    print("DB SELECT")

    today = date.today().isoformat() + '%'
    cur = dbconn().cursor()
    cur.execute(f"SELECT * FROM subaccdata WHERE acctime LIKE '{today}' order by acctime DESC")
    result_all = cur.fetchall()
    sbstr=""
    
    for i in result_all:
        for j in i:
            sbstr =  sbstr + j + "\n"
    
    sbstr = sbstr[:-1]

    
    print("DB SELECT Clear")
    print("-"*30)
    
    return sbstr

# 크롬 드라이버
def set_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument("headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(20)
    return driver

# SELENIUM - 오늘 날짜의 지하철 이슈 찾아보기
def todaysubaccCROW():
    # 크롬 드라이버 호출
    driver = set_chrome_driver()
    time.sleep(4)
    driver.get("https://safecity.seoul.go.kr/acdnt/sbwyIndex.do")
    time.sleep(5)
    parentElement = driver.find_elements(By.XPATH, '//*[@id="dv_as_timeline"]/li')
    subli=[]
    print("크롤링 준비완료")
    

    time.sleep(2)
    for i in parentElement:
        time.sleep(1)
        i.click()
        time.sleep(1)
        a = i.text
        subli.append(a)
        i.click()
        time.sleep(1)

    time.sleep(2)
    driver.quit()
    print("크롤링 완료")
    print("-"*30)
    return subli

# 카카오 API 메시지보내기
def kakaoapi(message):
    print("카톡알림 실행\n")
    with open("kakao_code.json","r") as fp:
        ts = json.load(fp)
        
    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers={"Authorization" : "Bearer " + ts["access_token"]}
    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":message,
            "link":{
                "web_url":"www.naver.com"
            }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code==200:
        print("카톡알림 완료\n")
        print("-"*30)
    else:
        print("카톡알림 실패\n")
        print("-"*30)

# main코드
def main():
    now = time
    print("-"*60)
    print("time log :", now.strftime('%Y-%m-%d %H:%M:%S'))

    dbselect = todaysubaccDB()
    crwaling = todaysubaccCROW()
    
    # 크롤링한 데이터 나누기 - DB에서 가져온 것과 비교하기 위해
    crstr = ""
    for i in crwaling:
        i = i[6:]
        crstr = crstr + i + '\n'
    crstr = crstr[:-1]
    
    # db데이터와 크롤링한 데이터가 다를때
    if (crstr!=dbselect):
        
        # 1. 속보가 없는건지 확인한다
        if (len(crwaling[0]) == 12):
            print("오늘의 속보 없음\n")
            print("-"*30)
        
        # 2. 속보가 있으면 db에 넣어주고 카톡 알림
        else:
            print("새로운 속보 감지")
            conn = dbconn()
            cur = conn.cursor()
            
            for i in crwaling:
                # 크롤링한 데이터 정규화
                subdb = i.split('\n')
                subdb.pop(0)
                cur.execute("INSERT into subaccdata(acctime, content) VALUES (%s, %s) ON CONFLICT (acctime, content) DO NOTHING", subdb)
            conn.commit()
            print("DB INSERT")
            
            # 카카오 메시지 보내기 호출
            kakaoapi(crwaling[0])
    else:
        print("속보 변동 없음")
        print("-"*30)

# 프로그램 테스트시
# (1) 159~164 주석
schedule.every(10).minutes.do(main)
schedule.every().day.at("23:55").do(exit)

while True:
    schedule.run_pending()
    time.sleep(1)

# (2) main() 주석 풀고 실행
# main()