from bs4 import BeautifulSoup
import urllib.request
from _io import (DEFAULT_BUFFER_SIZE, BlockingIOError, UnsupportedOperation,
                 open, FileIO, BytesIO, StringIO, BufferedReader,
                 BufferedWriter, BufferedRWPair, BufferedRandom,
                 IncrementalNewlineDecoder, TextIOWrapper)
import sys


def spider(place_id):
    place_id = str(place_id)
    url = 'https://store.naver.com/restaurants/detail?id=%s&tab=main' % place_id
    # source_code = requests.get(url)
    source_code = urllib.request.urlopen(url)
    plain_text = source_code.read().decode('utf-8')
    soup = BeautifulSoup(plain_text, 'lxml')

    store_data_context = {}
    menu_arr = []
    # # get name
    # try:
    #
    #     for name in soup.find('strong', {"class": "name"}):
    #         print(name)
    # except:
    #     print("none_addr")

    # # get category
    # try:
    #
    #     for category in soup.find('span', {"class": "category"}):
    #         print(category)
    # except:
    #     print("none_category")

    # blog review num
    try:
        review_num = soup.find('div', {"class": "info_inner"})
        str1 = review_num.getText()
        for s in review_num.find('a', {"class":"link"}):
            if s.isdigit():
                store_data_context["blogReviewNum"] = s    
    except:
        store_data_context["blogReviewNum"] = "none_review_num"
        # print("none_review_num")

    # # get call num
    # try:
    #
    #     for callnum in soup.find('div', {"class": "txt"}):
    #         print(callnum)-
    # except:
    #     print("none_call_num")
    #
    # # get addr
    # try:
    #     count = 0
    #
    #     for taddr in soup.find_all('span', {"class": "addr"}):
    #         print(taddr.getText())
    #         count += 1
    #         if count > 1:
    #             break
    # except:
    #     print("none_addr")

    # get work time
    try:
        for time in soup.find('div', {"class": "list_item list_item_biztime"}):
            ttime = time.getText()
            ttime_open = ttime[3:8]
            ttime_close = ttime[11:16]
            ttime_desc = ''
            if len(ttime) >= 16:
                ttime_desc = ttime[16:]
                store_data_context["ttime_open"] = ttime_open
                store_data_context["ttime_close"] = ttime_close
                store_data_context["ttime_desc"] = ttime_desc
                # print("time: %s" % (ttime_open + ' ' + ttime_close + ' ' + ttime_desc))

            elif len(ttime) >= 3:
                store_data_context["ttime_open"] = ttime_open
                store_data_context["ttime_close"] = ttime_close
                store_data_context["ttime_desc"] = "none_desc"
                # print("etime: %s" % (ttime_open + ' ' + ttime_close))

            else:
                pass
    except:
        store_data_context["ttime_open"] = "none_open"
        store_data_context["ttime_close"] = "none_close"
        store_data_context["ttime_desc"] = "none_desc"
        # print("none+desc")

    # try:
    #     for time in soup.find('span', {"class": "time"}):
    #         print(time.getText())
    # except:
    #     print("none_time")

    # get menu
    try:
        for search in soup.find_all('div', {"class": "list_menu_inner"}):
            tsearch = search.getText()
            if '이미지' in tsearch:
                pass
            else:
                pin_point = tsearch.find('원') + 1
                menu_price = tsearch[0: pin_point]
                menu_name = tsearch[pin_point:]
                menu_arr.append({menu_name: menu_price})
                # print(menu_name + " " + menu_price)
        store_data_context['menu'] = menu_arr

    except:
        pass
        # print("none_menu")


    return store_data_context

