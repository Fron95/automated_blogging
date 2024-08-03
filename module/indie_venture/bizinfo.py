import requests
import pandas as pd
import os
from datetime import datetime
def convert_date_format(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d%H:%M:%S')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return date_str


def bizinfo_single_page(page):
    url = "https://www.bizinfo.go.kr/uss/rss/bizinfoApi.do"
    params = {
        'crtfcKey': os.getenv("BIZINFO_API_KEY"),
        'dataType': 'json',
        'searchCnt': '100',
        'pageUnit': '15',
        'pageIndex': str(page)
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    items = data['jsonArray']
    parsed_data = []
    for item in items:
        start_date, end_date = item.get('reqstBeginEndDe', '').split(' ~ ') if ' ~ ' in item.get('reqstBeginEndDe', '') else ('', '')
        parsed_data.append( {
                    'title': item['pblancNm'],
                    'url': "https://www.bizinfo.go.kr" + item['pblancUrl'],
                    'description': item.get('bsnsSumryCn',''),
                    'category': item['pldirSportRealmLclasCodeNm'],
                    'startDate': start_date,
                    'endDate': end_date,
                    'provider' : '기업마당',
                    'organization': item['excInsttNm'],
                    'region': item.get('jrsdInsttNm', ''),
                    'registerDate': item['creatPnttm']
                })
    return pd.DataFrame(parsed_data)

def bizinfo_multi_page(start=1, end=10):
    all_data = pd.DataFrame()
    for page in range(start, end + 1):
        print(f"Fetching page {page}...")
        single_page_data = bizinfo_single_page( page)
        if single_page_data.empty:
            print('[SYSTEM] 마지막 페이지 도달')
            break
        all_data = pd.concat([all_data, single_page_data], ignore_index=True)
    return all_data


