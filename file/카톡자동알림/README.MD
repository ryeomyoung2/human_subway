# 카카오톡API로 자동 메시지 보내기 프로세스

작성일 : 20221124

카카오톡 '나에게 보내기' 예제

파일을 실행하기 전에 체크해야 할것

1. chromedriver.exe의 버전과 본인의 크롬 버전이 안맞을 수도 있음 (오류가 날 시 새로 설치추천)
2. kakaoToken.py와 kakoRefreshToken.py를 순서대로 실행 -> 토큰 유효기간이 2달 (자세한건 카카오api refreshtoken 구글검색)이므로 아마 2달마다 kakaoToken.py와 kakoRefreshToken.py를 실행하여 토큰을 갱신해줘야 함




---

작성일 : 20221125

어제 되더니 갑자기 안됨 -> 카카오 토큰 문제로 response가 401이뜸
-> 토큰을 매일 갱신해줘야 하는건가?? -> 주말에 확인