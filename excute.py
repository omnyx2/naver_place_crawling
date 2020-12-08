


# 실행 방침에 관한것
# 1. 해당 크롤링툴은 2가지 사이트에서 받는 구조이다. 1번째로, 네이버 히든 API로 부터 데이터를 받아오며 2번째로는 히든 API로 부터 받은 ID값을 통해 네이버 플레이스를 조회하고 그 데이터를 받는 방식이다.
# 2. 네이버 히든API로 부터 다음과 같은 데이터를 받는다.

# "id": temp_restaurant_data['id'],
# "rank": temp_restaurant_data['rank'],
# "name": temp_restaurant_data['name'],
# "tel": temp_restaurant_data['tel'],
# "category": temp_restaurant_data['category'],
# "address": temp_restaurant_data['address'],
# "roadAddress": temp_restaurant_data['roadAddress'],
# "abbrAddress": temp_restaurant_data['abbrAddress'],
# "display": temp_restaurant_data['display'],
# "coordX": temp_restaurant_data['x'],
# "coordY": temp_restaurant_data['y'],
# "description": temp_restaurant_data['description']

# 3. 본 프로그램의 실행은 excute.py를 실행시키면 된다.
# 4. 이때 실행시키고 싶은 지역의 이름의 목록들을 SearchList에 넣으면 된다.
# 5. 다만 검색함에 있어, 네이버 서버자체가 한 검색어에 대해 약 5000개의 리턴값을 가지므로 이를 충분히 고려하여 검색 지역 단위를 잡아야한다. 이에 따라 데이터의 특성이 충분히 달라질 수 있다.
# 6. 예를 들어 모든 음식점을 알고 싶으면 SearchList는 시 -> 구 -> 동까지 세분화하여 값을 넣어야된다.
# 7. 특징적인 것을 뽑고 싶을때는 시를 검색하여 상위 몇개의 데이터만 뽑으면 될 것이다.
# 8. 그리고 그렇게 뽑힌 데이터는 test_csv에 저장된다.
# 9. 해당 프로그램을 동작함에 있어 필요한 라이브러리는 다음과 같다.
# beautifulsoup4, selenium, urllib (추가예정))

import map_crawler
import csv

searchlist = []
f = open('SearchList.csv', 'r', encoding='EUC-KR')
rdr = csv.reader(f)
for line in rdr:
    searchlist.append(line[1])
f.close()


map_crawler.spyder(searchlist, "test_csv.csv")

