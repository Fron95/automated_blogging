import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import httpx
import re

def egbiz_single_page( page:int=1):
    url = 'https://www.egbiz.or.kr/prjCategory/a/m/selectPrjCategoryList.do'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.egbiz.or.kr',
        'Origin': 'https://www.egbiz.or.kr',
        'Referer': 'https://www.egbiz.or.kr/prjCategory/a/m/selectPrjCategoryList.do',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    cookies = {
        'JSESSIONID': 'aaadTfYAKS-It8k-Amv_y',
        '_ga': 'GA1.3.1778146144.1719206682',
        '_gid': 'GA1.3.1463749426.1719206682',
        '_ga_N8M1X7XF22': 'GS1.3.1719225497.2.1.1719225578.0.0.0',
    }

    data = {
        'part': 'category',
        'sclsCd': '',
        'pageIndex': page,
        'pageIndex1': page,
        'categoryId': '',
        'formName': 'listForm',
        'sortDescend': 'reg',
        'searchCondition': 'projectNm',
        'searchKeyword': '',
        'prjStatus': 'apply',
        'prjStatus_radio': 'apply',
    }

    client = httpx.Client(verify=False)
    response = client.post(url, headers=headers, cookies=cookies, data=data)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.select_one('body')
    for script in body.find_all('script'):
        script.decompose()
    tables = body.find_all('table')

    data_list = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols_data = row.find_all('td')
            if len(cols_data) > 1:
                title_element = cols_data[1].find('a')
                title = title_element.text.strip() if title_element else cols_data[1].get_text(strip=True)
                if (title is None) or title == '' : 
                    continue
                
                organization = cols_data[2].get_text(strip=True)
                start_end_date = cols_data[3].get_text(strip=True).split('-')
                startDate = f"{start_end_date[0]}.{start_end_date[1]}.{start_end_date[2]}".strip()
                endDate = f"{start_end_date[-3]}.{start_end_date[-2]}.{start_end_date[-1]}".strip()
                category = table.find('caption').get_text(strip=True)
                status_img = cols_data[4].find('img').get('alt') if cols_data[4].find('img') else ''
                views = cols_data[5].get_text(strip=True)

                data_list.append({
                    'title': title,
                    'description': '',
                    'organization': organization,
                    'category': category,
                    'url': 'https://www.egbiz.or.kr' + title_element.get('href', ''),
                    'provider': '이지비즈',
                    'region': '',
                    'startDate': startDate,
                    'endDate': endDate,
                    'registerDate' : ''
                    # 'status': status_img,
                    # 'views': views
                })

    return pd.DataFrame(data_list)

def egbiz_multi_page( start=1, end=999):
    isContinue = True
    results = pd.DataFrame()
    page = start
    while isContinue and page < end + 1 :
        print(f'[SYSTEM] {page}/{end} 조회 중')
        result = egbiz_single_page(page = page)
        if type(result) == type(None) :
            isContinue = False
        else :
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return pd.DataFrame(results)