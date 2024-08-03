import requests
from bs4 import BeautifulSoup
import pandas as pd

def nipa_single_page(page):
    url = 'https://www.nipa.kr/home/2-2'
    cookies = {
        'SCOUTER': 'z7eg0dhsmu3da0',
        '_ga': 'GA1.2.688002066.1719206618',
        'JSESSIONID': '2D0DA5066F5F73E16C007C499CFE0029',
        '_gid': 'GA1.2.653414037.1719486007',
        '_gat': '1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nipa.kr/home/2-2?curPage=2',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'curPage': str(page),
    }

    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tbody tr')
    
    if not rows:
        return pd.DataFrame()

    cols_list = []
    for row in rows:
        cols = row.find_all('td')
        title_element = cols[2].find('a')
        title = title_element.text.strip() if title_element else ''
        detail_code = title_element['href']
        register_date = cols[4].text.strip()
        
        data = {                
            'description': None,
            'category': None,
            'title': title,
            'url': "https://www.nipa.kr/" + detail_code,
            'provider': '정보통신산업진흥원(NIPA)',
            'startDate': None,
            'endDate': None,
            'region': None,
            'organization': None,                
            'registerDate': register_date
        }
        cols_list.append(data)
    
    return pd.DataFrame(cols_list)


def nipa_multi_page(start=1, end=999):
    results = pd.DataFrame()
    page = start
    while page <= end:
        print(f"Fetching page {page}/{end}...")
        result = nipa_single_page(page=page)

        if result is None:
            break
        else:
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return results

