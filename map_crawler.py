from selenium import webdriver
import json
import store_crawler
import csv
import clear_cachef
import os

# """
# return data context, follwing text is the form of context
#
# "id": temp_restaurant_data['id'],
# "rank": temp_restaurant_data['rank'],  !! Notion: it's not nessesary !!
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
# "blogReviewNum" : "블로그 리뷰 수"
# "ttime_open" : "오픈시간"
# "ttime_close : "마감시간"
# "ttime_desc" : "휴일시간"
# "menu" : menu_arr("menu" : "price"
#
# """


# 데이터 타입 context 화
# Datatype formating to context
def store_context_data_naver_map(temp_list_map_data):
    map_data_list = []
    for temp_restaurant_data in temp_list_map_data:
        map_data_list.append({
            "id": temp_restaurant_data['id'],
#            "rank": temp_restaurant_data['rank'],
            "name": temp_restaurant_data['name'],
            "tel": temp_restaurant_data['tel'],
            "category": temp_restaurant_data['category'],
            "address": temp_restaurant_data['address'],
            "roadAddress": temp_restaurant_data['roadAddress'],
            "abbrAddress": temp_restaurant_data['abbrAddress'],
            "display": temp_restaurant_data['display'],
            "coordX": temp_restaurant_data['x'],
            "coordY": temp_restaurant_data['y'],
            "description": temp_restaurant_data['description']}
        )
    return map_data_list


# 네이버 플레이스 데이터를 크롤링하고 네이버 히든 api 데이터와 크롤링 데이터 여러개를 합치는 과정입니다
# Crawling naver place data and integerating a few of context data
# which is from naver hidden api data and naver place crawling data
def integerate_data_naver_map_place(raw_list_map_data):

    map_data_list = store_context_data_naver_map(raw_list_map_data)
    integrate_data_list = []

    try:
        for map_data_context in map_data_list:
            store_data_context = store_crawler.spider(map_data_context['id'][1:])
            map_data_context.update(store_data_context)
            integrate_data_list.append(map_data_context)
            print("▩ ", end='')

        return integrate_data_list

    except Exception as ex:  # ex는 발생한 에러의 이름을 받아오는 변수
        print('에러가 발생 했습니다', ex)  #

        try:
            for map_data_context in map_data_list:
                store_data_context = store_crawler.spider(map_data_context['id'][1:])
                map_data_context.update(store_data_context)
                integrate_data_list.append(map_data_context)
                print("▧ ",end='')
            return integrate_data_list

        except Exception as ex:  # ex는 발생한 에러의 이름을 받아오는 변수
            print('에러가 발생 했습니다', ex)  #
            print('재시도 합니다')

            try:
                for map_data_context in map_data_list:
                    store_data_context = store_crawler.spider(map_data_context['id'][1:])
                    map_data_context.update(store_data_context)
                    integrate_data_list.append(map_data_context)
                    print("▤ ",end='')
                return integrate_data_list

            except Exception as ex:  # ex는 발생한 에러의 이름을 받아오는 변수
                print('에러가 발생 했습니다', ex)
                print("연속적인 에러 발생, cache에 대한 오류로 판단")

                # session을 재 갱신합니다.
                # refreshing session
                try:
                    for map_data_context in map_data_list:
                        store_data_context = store_crawler.spider(map_data_context['id'][1:])
                        map_data_context.update(store_data_context)
                        integrate_data_list.append(map_data_context)
                        print("□ ",end='')
                    return integrate_data_list

                except Exception as ex:  # ex는 발생한 에러의 이름을 받아오는 변수결
                    print('4번의 연속적인 연결 에러가 발생 했습니다', ex)
                    print("우린 다 끝났어 돈때문에 하는거야.")
                    return exit()


def check_integrity(temp_naver_data_list, search_word, raw_search_list, end_stack):
    search = search_word
    search_list = raw_search_list.copy()
    search_list.remove(search)

    # python use pointer to list
    raw_search_list = []

    # 하나제거하고 삭세할 방법 강
    now_i = -1

    try:
        for temp_check_integrity in temp_naver_data_list:
            now_i += 1

        # # abbrAddress none case
        # normalcase
            if temp_check_integrity['abbrAddress'] is None:
                raw_search_list.append(temp_check_integrity)
                continue

            if search in temp_check_integrity['abbrAddress']:
                raw_search_list.append(temp_check_integrity)
                continue

            else:
                for search_list_key in search_list:
                    # print(search_list_key+ " ,, " + temp_check_integrity['abbrAddress'], end="")
                    # print(" ,,", end="")
                    if search_list_key in search_list:
                        # print(end_stack, end="")
                        end_stack += 1
                        break

                    else:
                        raw_search_list.append(temp_check_integrity)
                        print("case1")
                        break

    except Exception as ex:
        print("huuu", ex)

    print("")
    return {'data': raw_search_list, 'end_stack': end_stack}


def open_chorme():
    # driver = webdriver.Chrome('')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option("prefs", prefs)
   
    chrome_driver_dir = "./chromedriver/chromedriver"
    driver = webdriver.Chrome(chrome_driver_dir, chrome_options=options)
    driver.get('http://www.naver.com')
    driver.implicitly_wait(3)
    driver.get('http://map.naver.com')
    driver.implicitly_wait(3)

    return driver


def close_chorme(driver):
    clear_cachef.clear_cache(driver)
    driver.get_screenshot_as_file('naver_map_json.png')
    driver.quit()


def get_session_naver_map(driver):
    # To access naver map json file some session required which is cookie
    # that can get from accessing naver.com
    # clear_cachef.clear_cache(driver)
    # driver.get('http://www.naver.com')
    # driver.implicitly_wait(3)
    driver.get('http://map.naver.com')


def get_data_via_chorme(search, driver, i):
    # json file contains information about restaurant list
    # at first we only can get html file, In here we should change in to json file.
    # to change json file, we fine element pre
    # pre is the thing use for showing whole line whatever it is,
    # if it is html tag of '{', whatever!
    # however, in our request, json text covered with pre
    # so we'll gonna use pre tag to get json file



    temp_html = driver.get(
        'https://map.naver.com/search2/local.nhn?query=%s+음식점&page=%d' % (search, i))
    temp_text = driver.find_element_by_tag_name("pre").text
    temp_json = json.loads(temp_text)
    driver.get_screenshot_as_file('naver_map_js1oqn.png')
    # now let's refactoring data
    if 'NO_RESULT' == temp_json["result"]['type']:
        restaurant_list_data = []
    else:
        restaurant_list_data = temp_json["result"]["site"]["list"]

    return restaurant_list_data


def init_head_in_csv(csv_file, csv_columns):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()


def write_context_data_in_csv(temp_list_csv_write, csv_file, csv_columns):
    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        try:
            for temp_data_context in temp_list_csv_write:
                writer.writerow(temp_data_context)
                # csv 출력 직전에 한줄한줄 써서 보여주는중
                # print(temp_data_context)

        except IOError:
            print("I/O error", end='')
            print(temp_list_csv_write)
            print("--------------------------------")


def write_in_csv(temp_list_csv_write, mode, csv_file):
    # csv_file = "gwanju_data_crawling.csv"
    csv_columns = ['id', 'rank', 'name', 'tel', 'category',
                   'address', 'roadAddress',
                   'abbrAddress', 'display', 'coordX',
                   'coordY', 'description', 'blogReviewNum',
                   'ttime_open', 'ttime_close', 'ttime_desc', 'menu']
    if mode == 'new':
        init_head_in_csv(csv_file, csv_columns)

    elif mode == 'add':
        write_context_data_in_csv(temp_list_csv_write, csv_file, csv_columns)


def spyder(search_list, filename):
    driver = open_chorme()

    # initialValue to crawling

    end_stack = 0
    data_list = []
    specify_filename = filename.split('.')[0] + '.' + filename.split('.')[1]
    write_in_csv([], 'new', specify_filename)

    for search in search_list:
        i = 0

        # this is for dividing
        # specify_filename = filename.split('.')[0] + '_' + search + '.' + filename.split('.')[1]
        # write_in_csv([], 'new', specify_filename)

        while True:
            if (i % 10) == 0:
                get_session_naver_map(driver)

            try:
                restaurant_list_data = get_data_via_chorme(search, driver, i)

                i += 1

                # if no data in restaurant_list_data:
                if not restaurant_list_data:
                    print('arrive-end')
                    break

                else:
                    # temp_naver_data_list = store_context_data_naver_map(restaurant_list_data)
                    temp_naver_data_list = integerate_data_naver_map_place(restaurant_list_data)
                    # print(temp_naver_data_list)
                    data_list_context = check_integrity(temp_naver_data_list, search, search_list, end_stack)
                    data_list = data_list_context['data']
                    # print(data_list)
                    end_stack = data_list_context['end_stack']

                    if(end_stack>200):
                        end_stack = 0
                        break

                    write_in_csv(data_list, 'add', specify_filename)

            except Exception as ex:  # ex는 발생한 에러의 이름을 받아오는 변수
                print("ERROR! :: ", ex)
                print(end_stack)
                if (end_stack > 10):
                    end_stack = 0
                    break
                pass

    if (driver != None):
        driver.quit()

    # 해당 부분 수정요함, 해당 부분은 열심
    # close_chorme(driver)

    return data_list


