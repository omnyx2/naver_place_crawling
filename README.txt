
# ** 중요: 현재 네이버 맵 음식점 검색 요청 URI의 변경으로 툴이 정상으로 작동하지 않습니다.
# 검색 방식을 변경해야하며 검색 방식은 map_crawlew.py의 get_data_via_chorme를에서 받아오는 기본 주소를 변경하여 사용하시면 됩니다.


# 1. 본 프로그램의 사용에 의한 불이익은 책임지지 않습니다.

# 2. Dependencies 설치 목록들
#  + python3 -m pip install --user --upgrade beautifulsoup4
#  + python3 -m pip install --user --upgrade urllib 
#  + python3 -m pip install --user --upgrade selenium 
#  + chromedriver에 자신의 크롬과 같은 버전의 chromedvier를 다운 받아서 넣어준다. 
#  + https://chromedriver.chromium.org/downloads이 사이트에서 다운 받으면 된다


# 3. 본 프로그램의 실행은 excute.py를 실행시키면 된다.
# 4. 이때 실행시키고 싶은 지역의 이름의 목록들을 SearchList에 넣으면 된다.
# 5. 다만 검색함에 있어, 네이버 서버자체가 한 검색어에 대해 약 5000개의 리턴값을 가지므로 이를 충분히 고려하여 검색 지역 단위를 잡아야한다. 이에 따라 데이터의 특성이 충분히 달라질 수 있다.
# 6. 예를 들어 모든 음식점을 알고 싶으면 SearchList는 시 -> 구 -> 동까지 세분화하여 값을 넣어야된다.
# 7. 특징적인 것을 뽑고 싶을때는 시를 검색하여 상위 몇개의 데이터만 뽑으면 될 것이다.
# 8. 그리고 그렇게 뽑힌 데이터는 test_csv에 저장된다.
# 9. 해당 프로그램을 동작함에 있어 필요한 라이브러리는 다음과 같다.

