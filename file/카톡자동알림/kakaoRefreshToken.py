import requests
import json

# 토큰정보 열기
#2.
with open("kakao_code.json","r") as fp:
    ts = json.load(fp)

# 토큰 refresh
url = 'https://kauth.kakao.com/oauth/token'
# 본인 앱의 api키
rest_api_key = 'f0b5de8b4882015099eaca013e4d373f'

data = {
    "grant_type" : "refresh_token",
    "client_id": rest_api_key,
    "refresh_token": ts['refresh_token']
}
response = requests.post(url,data=data)
tokens = response.json()

with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)