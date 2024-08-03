import requests
from bs4 import BeautifulSoup
import pandas as pd

def ripc_single_page(page):
    url = "https://www.ripc.org/www2/portal/notice/ripc4NoticeList.do"
    headers = {}
    cookies = {
        "JSESSIONID": "0BD993407D620333CA217BE85D896091",
        "_ga": "GA1.1.1766113721.1719206506",
        "_ga_E4VKP0S290": "GS1.1.1719321492.6.1.1719321496.0.0.0"
    }
    payload = {
        'searchType': '',
        'searchQuery': '',
        'inSearchType': 'title',
        'inSearchQuery': '',
        'pagingModel.pageNo': page,
        'pagingModel.rowPerPage': 20,
        'pagingModel.rowSize': 265,
        'pagingModel.blockCount': 10,
        'pagingModel.orderByColumn': 'writeDate',
        'pagingModel.orderByType': 'desc'
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=payload)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tbody tr')
    
    if not rows:
        print('[SYSTEM] 마지막 페이지 도달')
        return 

    cols_list = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 5:
            continue
        title_element = cols[1].find('a')
        title = title_element.text.strip() if title_element else ''
        detail_code = title_element['href'].split("'")[1] if title_element else ''
        register_date = cols[2].text.strip() if len(cols) > 2 else ''
        
        data = {                
            'description' : None,
            'category': None,
            'title': title,
            'url' : f"https://pms.ripc.org/pms/biz/applicant/board/viewBoardDetail.do?selectedBoardSeq={detail_code}&boardCategoryCode=BD40000",
            'provider' : 'RIPC',
            'startDate': None,
            'endDate': None,
            'region': None,
            'organization': None,                
            'registerDate': register_date
        }
        cols_list.append(data)
    
    return pd.DataFrame(cols_list)

def ripc_multi_page(start=1, end=999):
    results = pd.DataFrame()
    page = start
    while page <= end:
        print(f"Fetching page {page}/{end}...")
        result = ripc_single_page(page=page)

        if result is None:
            break
        else:
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return results

# Example usage
if __name__ == "__main__":
    df = ripc_multi_page(start=1, end=5)
    print(df)
