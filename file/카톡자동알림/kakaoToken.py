""" 
authorize_code 얻는법!!! - 참조 링크 (https://novice-engineers.tistory.com/9)

    인터넷에 https://kauth.kakao.com/oauth/authorize?client_id={본인의 RESTAPI키}&redirect_uri={본인의REDIRECT_URI}&response_type=code
    를 타이핑 하면
    https://example.com/oauth?code=임의의 코드
    이런 형식의 사이트로 들어가짐.
    여기서 임의의 코드가 authorize_code값 - 복사해서 아래의 18행 코드에 넣고 실행해주면 됨.
    
"""
import requests
import json

# 토큰 얻기
url = 'https://kauth.kakao.com/oauth/token'
# 본인 앱의 api 키
rest_api_key = 'f0b5de8b4882015099eaca013e4d373f'
# 본인 앱의 redirect_uri
redirect_uri = 'https://example.com/oauth'

# 2행 참조
authorize_code = 'zseeMiLU195R4Ak3PUhjbHsHURTCTnjJJyuCipBA3aBfvzT7l5blsybbdWSm-DqC0TtDawo9dVoAAAGErEhCew'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()

# 토큰을 json 형식으로 저장 (현재 디렉토리)
with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)