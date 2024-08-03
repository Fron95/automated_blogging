import requests
from bs4 import BeautifulSoup
import pandas as pd

def tipa_single_page(page):
    url = "https://www.smtech.go.kr/front/ifg/no/notice02_list.do"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "fec3fe3b-123e-4583-b047-6bfe3210ee28=2c405616-8bc6-4d88-abf5-eddc9d619075; JSESSIONID=jrffsBNOSYMMQX49zeetMlsQAmTAzaVSfRvV1fNoeoBHFLPGz77TgtJ1y9Kq6a6O.smwas3_servlet_engine4",
        "Host": "www.smtech.go.kr",
        "Referer": "https://www.smtech.go.kr/front/ifg/no/notice02_intro.do",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    payload = {
        'pageIndex': page
    }

    response = requests.get(url, headers=headers, params=payload)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tbody tr')

    if not rows:
        print('[SYSTEM] 마지막 페이지 도달')
        return 

    cols_list = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        title_element = cols[2].find('a')
        title = title_element.text.strip() if title_element else ''
        detail_code = title_element['href']
        register_date = cols[4].text.strip()
        period_text = cols[3].text.strip()
        
        start_date, end_date = None, None
        if " ~ " in period_text:
            start_date, end_date = period_text.split(" ~ ")

        data = {                
            'description' : None,
            'category': None,
            'title': title,
            'url' : "https://www.smtech.go.kr" + detail_code,
            'provider' : '중소기업기술정보진흥원(TIPA)',
            'startDate': start_date,
            'endDate': end_date,
            'region': None,
            'organization': None,                
            'registerDate': register_date
        }
        cols_list.append(data)

    return pd.DataFrame(cols_list)

def tipa_multi_page(start=1, end=999):
    results = pd.DataFrame()
    page = start
    while page <= end:
        print(f"Fetching page {page}/{end}...")
        result = tipa_single_page(page=page)

        if result is None:
            break
        else:
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return results

