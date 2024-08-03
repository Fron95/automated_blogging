import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import httpx
import re

def ccei_single_page( page):
    url = "https://ccei.creativekorea.or.kr/seoul/custom/noticeList.json"
    
    payload = {
        'no': '',
        'div_code': '',
        'rnum': '',
        'pn': page,
        'kind': 'all',
        'sPtime': 'all',
        'sMenuType': '',
        'pagePerContents': 8,
        'cmntySeqNum': '',
        'menuSeqNum': '',
        'storyList': '',
        'sdate': '',
        'edate': '',
        'orderByVal': 0,
        'title': '',
        'contents': ''
    }

    response = requests.post(url, data=payload)
    contents = response.json()['result']['list']

    if len(contents) < 1 :
        print('[SYSTEM] 마지막 페이지 도달')
        return

    data_list = []

    for content in contents:
        number1, number2 = content.get('SEQ', ''), content.get('ROWNUM', '')
        content_url=f"https://ccei.creativekorea.or.kr/seoul/custom/notice_view.do?no={number1}&div_code=&rnum={number2}&pn={page}&kind=all&sPtime=now&sMenuType=&pagePerContents=8&cmntySeqNum=&menuSeqNum=&storyList=&sdate=&edate=&orderByVal=1&title=&contents="                          
        if not number1 :
            content_url = ''
        data = {
            'title': content.get('TITLE', ''),
            'description': '',  # description 정보가 JSON에 없으므로 빈 문자열로 설정
            'organization': '',  # organization 정보가 JSON에 없으므로 빈 문자열로 설정
            'category': '',  # category 정보가 JSON에 없으므로 빈 문자열로 설정
            'url': content_url,
            'provider': '창조경제혁신센터',  # provider 정보가 JSON에 없으므로 빈 문자열로 설정
            'region': content.get('COUNTRY_NM', ''),
            'registerDate': content.get('REG_DATE', ''),
            'startDate' : '',
            'endDate': '',  # endDate 정보가 JSON에 없으므로 빈 문자열로 설정
        }
        data_list.append(data)

    return pd.DataFrame(data_list)

def ccei_multi_page( start=1, end=999):
    isContinue = True
    results = pd.DataFrame()
    page = start
    while isContinue and page < end + 1 :
        print(f'[SYSTEM] {page}/{end} 조회 중')
        result = ccei_single_page(page = page)
        if type(result) == type(None) :
            isContinue = False
        else :
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return pd.DataFrame(results)